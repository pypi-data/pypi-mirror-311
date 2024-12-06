#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPDX-License-Identifier: MIT License
Copyright (c) 2023 Savoir-faire Linux

Uses all the builders to complete a full build of a package.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional
from contextlib import contextmanager
import os
import shutil

from ..utils.logger import log
from ..utils.process import sh_exec
from ..dev_env.vs_env import VSEnv
from .cmake_builder import CMakeBuilder
from .msb_builder import MsbBuilder
from ..models import BuildResult, BuildStatus

@dataclass
class BuildContext:
    """Holds all build-related configuration and state"""
    base_dir: Path
    install_dir: Optional[Path]
    vs_env: Optional[VSEnv] = None
    cmake_builder: Optional[CMakeBuilder] = None
    msb_builder: Optional[MsbBuilder] = None
    vs_env_init_cb: Optional[Callable] = None

    def __post_init__(self):
        # Convert string paths to Path objects if needed
        if isinstance(self.base_dir, str):
            self.base_dir = Path(self.base_dir)
        if self.install_dir and isinstance(self.install_dir, str):
            self.install_dir = Path(self.install_dir)

        if self.install_dir:
            self._setup_install_dirs()

    def _setup_install_dirs(self):
        """Create standard installation directories if they don't exist"""
        for subdir in ['bin', 'lib', 'include']:
            (self.install_dir / subdir).mkdir(parents=True, exist_ok=True)

@contextmanager
def working_directory(path: Path):
    """Context manager for changing working directory"""
    prev_dir = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_dir)

class MetaBuilder:
    def __init__(self, base_dir: Path | str, install_dir: Optional[Path | str] = None):
        # Convert to Path objects if needed
        base_dir = Path(base_dir) if isinstance(base_dir, str) else base_dir
        install_dir = Path(install_dir) if isinstance(install_dir, str) else install_dir
        self.ctx = BuildContext(base_dir, install_dir)

    def set_vs_env_init_cb(self, callback: Callable) -> None:
        self.ctx.vs_env_init_cb = callback

    def _initialize_vs_env(self) -> bool:
        """Initialize Visual Studio environment if not already done"""
        if self.ctx.vs_env is not None:
            return True

        self.ctx.vs_env = VSEnv()
        if not self.ctx.vs_env.validated:
            log.error("No valid Visual Studio environment found")
            return False

        self.ctx.cmake_builder = CMakeBuilder(self.ctx.vs_env)
        self.ctx.msb_builder = MsbBuilder(self.ctx.vs_env)

        if self.ctx.vs_env_init_cb:
            self.ctx.vs_env_init_cb()

        # Set up environment variables
        sh_exec.append_extra_env_vars({
            "CMAKE_GENERATOR": f'"{self.ctx.vs_env.cmake_generator}"',
            **self.ctx.vs_env.vars
        })
        return True

    def _copy_files(self, src_dir: Path, dst_dir: Path, extensions: List[str]) -> None:
        """Copy files with specified extensions, flattening directory structure"""
        dst_dir.mkdir(parents=True, exist_ok=True)

        for file_path in src_dir.rglob('*'):
            if file_path.suffix in extensions:
                shutil.copy2(file_path, dst_dir / file_path.name)
                log.debug(f"Copied: {file_path} to {dst_dir / file_path.name}")

    def install(self, pkg) -> BuildResult:
        """Install package artifacts to installation directory"""
        if not self.ctx.install_dir:
            return BuildResult.failure("No install directory specified")

        try:
            scan_dir = Path(pkg.buildsrc_dir)

            # Copy headers
            for include_dir in scan_dir.rglob('include'):
                dst = self.ctx.install_dir / 'include'
                self._copy_files(include_dir, dst, ['.h', '.hpp'])

            # Copy libraries and binaries
            self._copy_files(scan_dir, self.ctx.install_dir / 'lib', ['.lib'])
            self._copy_files(scan_dir, self.ctx.install_dir / 'bin', ['.dll', '.exe'])

            return BuildResult.success(f"Successfully installed {pkg.name}")
        except Exception as e:
            return BuildResult.failure(f"Installation failed: {str(e)}", e)

    def build(self, pkg) -> BuildResult:
        """Execute build process for a package"""
        try:
            if not self._initialize_vs_env():
                return BuildResult.failure("Failed to initialize VS environment")

            target_dir = Path(pkg.buildsrc_dir if os.path.exists(pkg.buildsrc_dir) else os.getcwd())

            with working_directory(target_dir):
                build_steps = [
                    (True, lambda: self._run_scripts(pkg, "pre_build"), "Pre-build scripts"),
                    (pkg.use_cmake, lambda: self._cmake_configure(pkg), "CMake configuration"),
                    (pkg.use_cmake, lambda: self._cmake_build(pkg), "CMake build"),
                    (True, lambda: self._run_scripts(pkg, "build"), "Custom build scripts"),
                    (bool(pkg.project_paths), lambda: self._msbuild(pkg), "MSBuild"),
                    (True, lambda: self._run_scripts(pkg, "post_build"), "Post-build scripts"),
                ]

                for condition, step, description in build_steps:
                    if condition:
                        result = step()
                        if result.status != BuildStatus.COMPLETED:
                            return BuildResult.failure(f"Failed during {description}: {result.message}")

                if self.ctx.install_dir:
                    return self.install(pkg)

                return BuildResult.success(f"Successfully built {pkg.name}")

        except Exception as e:
            return BuildResult.failure(f"Build failed: {str(e)}", e)

    def _run_scripts(self, pkg, stage: str) -> BuildResult:
        """Execute custom scripts for a given build stage"""
        scripts = pkg.custom_scripts.get(stage, [])
        for script in scripts:
            result = sh_exec.cmd(script)
            if result[0] != 0:
                return BuildResult.failure(f"Script failed: {script}")
        return BuildResult.success(f"Completed {stage} scripts")

    def _msbuild(self, pkg) -> BuildResult:
        """Execute MSBuild for all project paths"""
        for project_path in pkg.project_paths:
            full_path = Path(pkg.buildsrc_dir) / project_path
            if not self.ctx.msb_builder.build(
                pkg.name,
                str(full_path),
                self.ctx.vs_env.sdk_version,
                self.ctx.vs_env.toolset_default,
                pkg.with_env
            ):
                return BuildResult.failure(f"MSBuild failed for {project_path}")
        return BuildResult.success("MSBuild completed successfully")

    def _cmake_configure(self, pkg) -> BuildResult:
        """Configure project with CMake"""
        if not self.ctx.cmake_builder.configure(pkg):
            return BuildResult.failure("CMake configuration failed")
        return BuildResult.success("CMake configuration completed")

    def _cmake_build(self, pkg) -> BuildResult:
        """Build project with CMake"""
        if not self.ctx.cmake_builder.build(pkg):
            return BuildResult.failure("CMake build failed")
        return BuildResult.success("CMake build completed")
