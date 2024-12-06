#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPDX-License-Identifier: MIT License
Copyright (c) 2023 Savoir-faire Linux

Used to apply patches to a package
"""

import os

from ..utils.logger import log
from ..utils.process import sh_exec


class Patcher:
    def __init__(self, src_dir, buildsrc_dir):
        self.src_dir = src_dir
        self.buildsrc_dir = buildsrc_dir
        self.patch_args = ["-flp1", "-i"]
        self.git_apply_args = [
            "apply",
            "--reject",
            "--ignore-whitespace",
            "--whitespace=fix",
        ]
        self.src_bash_path = self.__get_bash_path(self.src_dir)

    def apply_all(self, pkg):
        if not pkg.patches and not pkg.win_patches:
            return True
        elif not os.path.exists(pkg.buildsrc_dir):
            # Warn if the package has patches, but no build directory.
            log.warning(
                f"Package {pkg.name} has patches, but no build directory."
                f" Did you forget to fetch it?"
            )
            return False
        log.info(f"Patching {pkg.name}")
        tmp_dir = os.getcwd()
        pkg_build_path = os.path.join(self.buildsrc_dir, pkg.name)
        if not os.path.exists(pkg_build_path):
            os.makedirs(pkg_build_path)
        os.chdir(pkg_build_path)

        # 1. git patches (LF)
        for p in pkg.patches:
            patch_path = self.src_bash_path + "/" + pkg.name + "/" + p
            result = self.__apply(patch_path)
            if result[0]:
                log.error(f"Couldn't apply patch {patch_path}")
                return False

        # 2. windows git patches (CR/LF)
        for wp in pkg.win_patches:
            patch_path = self.src_dir + "\\" + pkg.name + "\\" + wp
            result = self.__apply_windows(patch_path)
            if result[0]:
                log.error(f"Couldn't apply patch {patch_path} (Windows)")
                return False

        # Done
        os.chdir(tmp_dir)
        return True

    def __apply(self, patch_path):
        log.info(f"Applying linux patch {patch_path}")
        args = []
        args.extend(self.patch_args)
        args.append(patch_path)
        return sh_exec.bash("patch", args)

    def __apply_windows(self, patch_path):
        log.info(f"Applying windows patch {patch_path}")
        args = []
        args.extend(self.git_apply_args)
        args.append(patch_path)
        return sh_exec.cmd("git", args)

    @staticmethod
    def __get_bash_path(path):
        """Returns the path based on which bash is being used"""
        driveless_path = path.replace(os.path.sep, "/")[3:]
        drive_letter = os.path.splitdrive(path)[0][0].lower()
        wsl_drive_path = "/mnt/" + drive_letter + "/"
        no_echo = "&> /dev/null"
        result = sh_exec.bash("pwd", ["|", "grep", wsl_drive_path, no_echo])
        if result[0] == 0:
            # using wsl
            return wsl_drive_path + driveless_path
        # using git bash
        return "/" + drive_letter + "/" + driveless_path
