#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPDX-License-Identifier: MIT License
Copyright (c) 2023 Savoir-faire Linux

Used to build a package with msbuild
"""

import fileinput
import re
import os

from ..dev_env.host_config import config
from ..utils.logger import log
from ..utils.process import sh_exec


class MsbBuilder:
    def __init__(self, vs_env):
        self.vs_env = vs_env
        self.msbuild = self.vs_env.msbuild_path
        self.set_msbuild_configuration()

    def set_msbuild_configuration(self, use_env="false", config_str="Release"):
        self.msbuild_args = self.vs_env.get_ms_build_args(
            config_str=config_str, use_env=use_env
        )

    def build(self, pkg_name, proj_path, sdk_version, toolset, use_env):
        log.debug(
            f"Building: {os.path.basename(proj_path)}({pkg_name})"
            f" with sdk: {self.vs_env.sdk_version}"
            f" and toolset {self.vs_env.toolset_default}"
        )

        self.set_msbuild_configuration(use_env=use_env)

        # force debug format to none for jenkins (concurrent access to pdb files
        # causes build failures)
        if config.is_jenkins:
            self.replace_vs_prop(proj_path, "DebugInformationFormat", "None")

        # force chosen sdk, toolset
        self.replace_vs_prop(proj_path, "WindowsTargetPlatformVersion", sdk_version)
        self.replace_vs_prop(proj_path, "PlatformToolset", toolset)

        args = []
        args.extend(self.msbuild_args)
        args.append(proj_path)

        result = sh_exec.cmd(self.msbuild, args)
        if result[0] == 0:
            return True
        log.error(f"Build failed when building {pkg_name}")
        return False

    @staticmethod
    def replace_vs_prop(filename, prop, val):
        p = re.compile(r"(?s)<" + prop + r"\s?.*?>(.*?)<\/" + prop + r">")
        val = r"<" + prop + r">" + val + r"</" + prop + r">"
        with fileinput.FileInput(filename, inplace=True) as file:
            for line in file:
                print(re.sub(p, val, line), end="")
