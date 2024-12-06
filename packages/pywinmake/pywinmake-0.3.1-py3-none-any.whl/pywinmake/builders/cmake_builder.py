#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPDX-License-Identifier: MIT License
Copyright (c) 2023 Savoir-faire Linux

Used to configure/build with CMake.
"""

import os
from ..utils.logger import log
from ..utils.process import sh_exec


class CMakeBuilder:
    def __init__(self, vs_env) -> None:
        self.vs_env = vs_env

    def build(self, pkg):
        cmake_dir = self._find_root_cmake_dir(pkg)
        build_dir = os.path.join(cmake_dir, 'build')
        log.info(f"Building with CMake in directory: {build_dir}")

        args = [
            '--build', build_dir,
            '--config', 'Release'
        ]

        result = sh_exec.cmd('cmake', args)
        if not result[0]:
            return True

        log.error("Error building with CMake")
        log.error(f"CMake output: {result[1]}")
        log.debug(f"CMake command: cmake {' '.join(args)}")
        return False

    def configure(self, pkg):
        cmake_dir = self._find_root_cmake_dir(pkg)
        log.info("Configuring with CMake in directory: " + cmake_dir)
        args = [
            '-G', self.vs_env.cmake_generator,
            '-A', self.vs_env.arch,
            '-S', cmake_dir,
            '-B', os.path.join(cmake_dir, 'build')
        ]
        args.extend(['-D' + define for define in pkg.defines])

        result = sh_exec.cmd('cmake', args)
        if not result[0]:
            return True

        log.error("Error configuring with CMake")
        log.error(f"CMake output: {result[1]}")
        log.debug(f"CMake command: cmake {' '.join(args)}")
        return False

    def _find_root_cmake_dir(self, pkg):
        """Find the root CMake directory for a package"""
        for root, dirs, files in os.walk(pkg.buildsrc_dir):
            if 'CMakeLists.txt' in files:
                return root
        return None
