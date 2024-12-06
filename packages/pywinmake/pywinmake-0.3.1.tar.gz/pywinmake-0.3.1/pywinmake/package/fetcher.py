#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPDX-License-Identifier: MIT License
Copyright (c) 2023 Savoir-faire Linux

Used to download packages using either wget or Invoke-WebRequest,
and extract them to a build directory.
"""

import glob
import os
import re
import shutil
import tarfile
import zipfile

from ..utils.logger import log
from ..utils.process import sh_exec


class Fetcher:
    def __init__(self, fetch_dir, buildsrc_dir):
        self.fetch_dir = fetch_dir
        self.buildsrc_dir = buildsrc_dir
        self.wget_args = [
            "--retry-connrefused",
            "--waitretry=1",
            "--read-timeout=20",
            "--timeout=15",
            "--tries=4",
        ]

    def fetch_pkg(self, pkg, force=False):
        """
        Fetches a package from a URL and extracts it to the build directory.
        Additionally, we will prepend the package name to the tarball file.
        This helps identify the package when removing old tarballs during a clean.
        """
        version_replace = re.compile(re.escape("__VERSION__"))
        full_url = version_replace.sub(pkg.version, pkg.url)
        if not full_url:
            log.error(f"Could not find a url for {pkg.name}")
            return False
        archive_name = full_url[full_url.rfind("/") + 1 :]
        # Prepend the package name to the archive name.
        archive_path = os.path.join(self.fetch_dir, pkg.name + "_" + archive_name)
        # Create the directory if it doesn't exist.
        os.makedirs(os.path.dirname(archive_path), exist_ok=True)
        if not os.path.exists(archive_path):
            log.info(f"Fetching {pkg.name} from {full_url}")
            args = [full_url, "-O", archive_path]
            args.extend(self.wget_args)
            dl_result = sh_exec.cmd("wget", args)
            if dl_result[0] != 0:
                log.warning("wget failure. Using powershell Invoke-WebRequest instead")
                args = ["-Uri", full_url, "-OutFile", archive_path]
                dl_result = sh_exec.ps1("Invoke-WebRequest", args)
                if dl_result[0] != 0:
                    log.error("Failed to download " + full_url)
                    return False
            return self.extract_archive(pkg, archive_name, archive_path)
        else:
            log.warning(
                f"{archive_name} already exists in the tarball/archive directory"
            )
            extracted = self.extract_archive(pkg, archive_name, archive_path)
            if not extracted and force:
                log.info("Removing old tarball for " + archive_name)
                sh_exec.cmd("del", ["/s", "/q", archive_name])
                return self.fetch_pkg(pkg.name, pkg.version, pkg.url, False)
            elif not extracted:
                log.error(f"Failed to extract {archive_name}")
                return False
            else:
                return True

    def extract_archive(self, pkg, name, path):
        is_tar = False
        if tarfile.is_tarfile(path):
            is_tar = True
        elif not zipfile.is_zipfile(path):
            log.error(f"Unsupported archive format {path}")
            return False
        try:
            with tarfile.open(
                path, "r", encoding="utf8", errors="ignore"
            ) if is_tar else zipfile.ZipFile(path, "r") as archive:
                cmn_prefix = os.path.commonprefix(
                    archive.getnames() if is_tar else archive.namelist()
                )
                # If there is no common prefix, then the archive is flat.
                flat_archive = cmn_prefix is None or cmn_prefix == ""
                log.warn("Found flat archive") if flat_archive else None
                if not flat_archive:
                    dirty_path = os.path.join(self.buildsrc_dir, cmn_prefix)
                    self.clean_artifacts(pkg.buildsrc_dir, dirty_path)
                log.info("Extracting " + name + " to " + pkg.buildsrc_dir)
                target = self.buildsrc_dir if not flat_archive else pkg.buildsrc_dir
                long_path_prefix = "\\\\?\\"
                archive.extractall(long_path_prefix + target)
                # If the archive is not flat, move the files to the build directory.
                if not flat_archive:
                    log.info("Moving " + cmn_prefix + " to " + pkg.buildsrc_dir)
                    src_dir = os.path.join(target, cmn_prefix)
                    dst_dir = long_path_prefix + os.path.abspath(pkg.buildsrc_dir)
                    shutil.move(src_dir, dst_dir)
            return True
        except Exception as e:
            log.error("Error extracting {}: {}".format(name, e))
            return False

    @staticmethod
    def clean_artifacts(pkg_buildsrc_dir, dirty_path):
        if os.path.exists(pkg_buildsrc_dir):
            log.info("Removing old package " + pkg_buildsrc_dir)
            sh_exec.cmd("rmdir", ["/s", "/q", pkg_buildsrc_dir])
        elif os.path.exists(dirty_path):
            log.info("Removing partial decompression " + dirty_path)
            sh_exec.cmd("rmdir", ["/s", "/q", dirty_path])

    def clean_pkg(self, pkg):
        clean_tarballs = self.clean_pkg_tarball(pkg)
        clean_build = self.clean_pkg_build(pkg)
        return clean_tarballs and clean_build

    def clean_pkg_tarball(self, pkg):
        return self.clean_tarballs(pkg.name)

    def clean_tarballs(self, pkg_name=None):
        extensions = ["*.tar.*", "*.tgz.*", "*.zip"]
        files_to_delete = []
        for ext in extensions:
            tb_prefix = "" if pkg_name is None else pkg_name + "_"
            files_to_delete.extend(
                glob.glob(os.path.join(self.fetch_dir, tb_prefix + ext))
            )
        if len(files_to_delete) > 0:
            for file_path in files_to_delete:
                log.info("Removing tarball " + file_path)
                ret = sh_exec.cmd("del", ["/s", "/q", file_path])
                if ret[0]:
                    log.error("Failed to clean tarball")
                    return False
        return True

    def clean_pkg_build(self, pkg):
        if os.path.exists(pkg.buildsrc_dir):
            log.info("Removing build source " + pkg.buildsrc_dir)
            ret = sh_exec.cmd("rmdir", ["/s", "/q", pkg.buildsrc_dir])
            if ret[0]:
                log.error("Failed to clean build directory")
                return False
        # Also remove the build file and source version files.
        version_files = [pkg.build_version_file, pkg.src_version_file, pkg.patch_file]
        for file_path in version_files:
            if os.path.exists(file_path):
                log.info("Removing version file " + file_path)
                ret = sh_exec.cmd("del", ["/s", "/q", file_path])
                if ret[0]:
                    log.error("Failed to clean version file")
                    return False
        return True

    def clean_builds(self):
        if not os.path.exists(self.buildsrc_dir):
            return True
        # Clean build directory.
        log.debug(f"Removing all build files from {self.buildsrc_dir}")
        ret = sh_exec.cmd("rmdir", ["/s", "/q", self.buildsrc_dir])
        if ret[0]:
            log.error("Failed to clean build directory")
            return False
        return True

    def clean_all(self):
        return self.clean_tarballs() and self.clean_builds()
