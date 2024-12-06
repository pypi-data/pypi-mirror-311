#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPDX-License-Identifier: MIT License
Copyright (c) 2023 Savoir-faire Linux

Run some actual tests on the pywinmake package, using the test/winmake.py script.
"""

import subprocess
import unittest
import os
import sys
from pathlib import Path
import shutil

def install_for_testing():
    """Install pywinmake in editable mode for testing"""
    print("Installing pywinmake for testing")
    root_dir = Path(__file__).parent.parent
    try:
        # Install in editable mode with pip
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-e', str(root_dir)
        ], check=True, capture_output=True, text=True)
        print("Successfully installed pywinmake for testing")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install pywinmake: {e.stdout}\n{e.stderr}")
        sys.exit(1)

class PyWinMakeTests(unittest.TestCase):
    """
    Test the pywinmake package.
    """
    @classmethod
    def setUpClass(cls):
        """Set up the test environment once before all tests"""
        install_for_testing()

        cls.this_dir = Path(__file__).parent
        cls.install_dir = cls.this_dir / 'install'

        # Base command setup
        cls.args = ['-l5', '-v2', '-o', str(cls.install_dir)]
        cls.base_command = [sys.executable, str(cls.this_dir / 'winmake.py')]
        cls.base_command.extend(cls.args)

        # Clean before starting
        subprocess.run(cls.base_command + ['clean'], check=True)

        # Clean the install directory and all its contents
        shutil.rmtree(cls.install_dir, ignore_errors=True)

    def test_0_resolve_package(self):
        """pjproject has several dependencies, so it's a good test package"""
        result = subprocess.run(self.base_command + ['resolve', 'pjproject', '-f'],
                                stdout=subprocess.PIPE)
        self.assertEqual(result.returncode, 0)
        # Make sure there is at least 1 *.lib file in the lib directory
        lib_dir = os.path.join(self.this_dir, 'install', 'lib')
        self.assertGreater(len(os.listdir(lib_dir)), 0)

    def test_1_resolve_package_with_different_name(self):
        """msgpack-c has a different package name than the directory name"""
        result = subprocess.run(self.base_command + ['resolve', 'msgpack', '-f'],
                                stdout=subprocess.PIPE)
        self.assertEqual(result.returncode, 0)
        # Make sure that msgpack.hpp is in the include directory
        # Up one directory, then into the install/include directory
        include_dir = os.path.join(self.this_dir, 'install', 'include')
        self.assertIn('msgpack.hpp', os.listdir(include_dir))

    def test_2_build_portaudio_with_missing_state(self):
        """Here we mess with the state file to see we can avoid applying patches multiple times"""
        result = subprocess.run(self.base_command + ['resolve', 'portaudio'],
                                stdout=subprocess.PIPE)
        self.assertEqual(result.returncode, 0)
        # Delete the build target file so we can force a rebuild
        build_dir = os.path.join(self.this_dir, 'contrib', 'build')
        target_file = os.path.join(build_dir, '.portaudio.build')
        self.assertTrue(os.path.exists(target_file))
        os.remove(target_file)
        # Build it again
        result = subprocess.run(self.base_command + ['resolve', 'portaudio'],
                                stdout=subprocess.PIPE)
        self.assertEqual(result.returncode, 0)

    def test_3_build_something_with_cmake(self):
        """Build a simple package that has no dependencies"""
        result = subprocess.run(self.base_command + ['resolve', 'libgit2'],
                                stdout=subprocess.PIPE)
        self.assertEqual(result.returncode, 0)

    def test_4_build_opendht(self):
        """Build opendht, which is complex and has a CMakeLists.txt file"""
        result = subprocess.run(self.base_command + ['resolve', 'opendht'],
                                stdout=subprocess.PIPE)
        self.assertEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()