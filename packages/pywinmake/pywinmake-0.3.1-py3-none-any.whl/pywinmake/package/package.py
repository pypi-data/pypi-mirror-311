#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPDX-License-Identifier: MIT License
Copyright (c) 2023 Savoir-faire Linux

VLC-style contrib package description.
"""

import json
import os

from ..utils.logger import log
from .build_tools import get_md5_for_path

PKG_FILE_NAME = "package.json"

"""
A helper class to track and manage a VLC-style contrib package's version
and build information.
A package can be defined with a json like this:
    {
        "name": "mylibrary",
        "version": "76a5006623539a58262d33458a5605be096b3a10",
        "url": "https://git.example.com/gorblok/mylibrary/archive/__VERSION__.tar.gz",
        "deps": ["mydep"],
        "use_cmake" : true,
        "defines": ["SEGFAULTS=0", "MY_CMAKE_DEFINE=true"],
        "patches": ["some_patch.patch"],
        "win_patches": ["some_windows_line_ending_patch.patch"],
        "project_paths": ["mylibrary-static.vcxproj"],
        "with_env" : "10.0.18362.0",
        "custom_scripts": { "pre_build": [], "build": [], "post_build": [] }
    }
"""


class Package:
    """
    A class to hold version and build information extracted from a
    package's JSON versioning file.
    """

    def __init__(self, pkg_name=None, src_dir=None, buildsrc_dir=None):
        """
        Initializes a package from a package.json file.

        :param pkg_name: The name of the package to build.
        :param src_dir: The directory containing the package's source rules.
        :param buildsrc_dir: The base directory to contain the package sources.
        """
        self.info = self.__load_info(src_dir, pkg_name)
        if self.info is None:
            log.critical(f"No package info for {pkg_name} in {src_dir}")
            return

        single_pkg = pkg_name is None
        if single_pkg:
            pkg_name = self.info.get("name")

        self.name = pkg_name
        self.src_dir = os.path.join(src_dir, pkg_name)

        if single_pkg:
            # If we are building a single package, we use the buildsrc_dir
            self.buildsrc_dir = buildsrc_dir
        else:
            self.buildsrc_dir = os.path.join(buildsrc_dir, self.info.get("name"))

        self.version = self.info.get("version")
        self.url = self.info.get("url")
        self.deps = self.info.get("deps", [])
        self.use_cmake = self.info.get("use_cmake", False)
        self.defines = self.info.get("defines", [])
        self.patches = self.info.get("patches", [])
        self.win_patches = self.info.get("win_patches", [])
        self.project_paths = self.info.get("project_paths", [])
        self.with_env = self.info.get("with_env", True)
        self.custom_scripts = self.info.get("custom_scripts", {})

        # Version files used to track the package's last built version,
        # and the last source fetched. The files are named .<pkg_name> within
        # contrib native (source build) directory.
        # src MD5           -> build_version_file
        # src version str   -> src_version_file
        self.build_version_file = os.path.join(buildsrc_dir, "." + pkg_name + ".build")
        self.src_version_file = os.path.join(buildsrc_dir, "." + pkg_name + ".src")
        self.patch_file = os.path.join(buildsrc_dir, "." + pkg_name + ".patch")

        # Derived versioning properties.
        self.build_version = self.get_version_from_file(self.build_version_file)
        self.src_version = self.get_version_from_file(self.src_version_file)
        self.is_patched = os.path.exists(self.patch_file)
        self.src_md5 = get_md5_for_path(self.src_dir)

        self.resolve_versioning()

    @staticmethod
    def __load_info(src_dir, pkg_name=None):
        if pkg_name is None:
            pkg_json_file = os.path.join(src_dir, PKG_FILE_NAME)
        else:
            pkg_json_file = os.path.join(src_dir, pkg_name, PKG_FILE_NAME)
        log.debug(f"Loading package info from {pkg_json_file}")
        if not os.path.exists(pkg_json_file):
            return None
        with open(pkg_json_file, encoding="utf8", errors="ignore") as json_file:
            return json.load(json_file)

    def get_version_from_file(self, version_file):
        if not os.path.exists(version_file):
            return None
        with open(version_file, "r") as f:
            return f.readline().strip()

    def resolve_versioning(self):
        self.src_uptodate = self.version == self.src_version
        self.is_patched = os.path.exists(self.patch_file)
        self.ver_uptodate = (
            self.src_md5 is not None and self.src_md5 == self.build_version
        )
        self.build_uptodate = self.src_uptodate and self.ver_uptodate

    def track_src_fetch(self):
        # Update the source version file with the current source version.
        with open(self.src_version_file, "w+", encoding="utf8", errors="ignore") as f:
            f.write(self.version)

    def track_src_build(self):
        # Update the build version file with the current source md5.
        self.src_md5 = get_md5_for_path(self.src_dir)
        with open(self.build_version_file, "w+", encoding="utf8", errors="ignore") as f:
            f.write(self.src_md5)

    def track_src_patch(self):
        # Touch the patch file to indicate that the package has been patched.
        if os.path.exists(self.patch_file):
            os.utime(self.patch_file, None)
        else:
            open(self.patch_file, 'a').close()
