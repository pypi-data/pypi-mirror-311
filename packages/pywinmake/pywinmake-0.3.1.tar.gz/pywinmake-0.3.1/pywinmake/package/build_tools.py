#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPDX-License-Identifier: MIT License
Copyright (c) 2023 Savoir-faire Linux

Helpers for building packages using pywinmake.
"""

import argparse
from enum import Enum
from pathlib import Path
import os
import hashlib
import sys


# An enum for the different operations that can be performed on a package.
class Operation(Enum):
    CLEAN = 0
    FETCH = 1
    PATCH = 2
    BUILD = 3
    RESOLVE = 4

    def __str__(self):
        return self.name.lower()

    @staticmethod
    def from_string(s):
        return Operation[s.upper()]


# A structure to hold all the absolute paths used by the build system.
# Helps isolate a package directory from the rest of the system.
class Paths:
    def __init__(self, base_dir=None, root_names=[]):
        self.base_dir = None
        self.contrib_dir = None

        if base_dir is None:
            # Start at the calling script's directory.
            calling_script_path = os.path.abspath(sys.modules['__main__'].__file__)
            base_dir = Path(calling_script_path).parent

            # Climb up the directory tree until we find the project dir or hit root.
            while base_dir.name not in root_names:
                base_dir = base_dir.parent
                if base_dir == base_dir.parent:
                    raise RuntimeError("Could not find project dir.")

            self.base_dir = os.path.abspath(base_dir)
        else:
            self.base_dir = os.path.abspath(base_dir)

        if not self.base_dir or not os.path.isdir(self.base_dir):
            raise RuntimeError("Could not find project dir.")

        self.contrib_dir = os.path.join(self.base_dir, "contrib")

def get_default_parsed_args(parser=None):
    # <script> [-h] [-l {1-5}] [-q] [-v {0-2}] [-i] {clean,fetch,build,resolve} [<pkg>]
    # Example command line:
    #   python <script> -iq -v2 resolve all
    # Args include:
    #  Logging:
    #   -l1-5, --log-level=1-5 (default: 4) CRITICAL, ERROR, WARNING, INFO, DEBUG
    #   -q, --quiet suppress stdout/stderr (default: False)
    #   -v0-2, --verbose=0-2 (default: 1) (0: quiet, 1: normal, 2: debug script exec)
    #   -i, --indent indent log output (default: False)
    #   -h, --help show this help message and exit
    #   -o, --outdir install prefix (default: None)
    #  Operation subcommands (at least one required):
    #   {clean,fetch, patch, build, resolve}

    if parser is None:
        parser = argparse.ArgumentParser(description="Build contrib-style packages")

    parser.add_argument(
        "-l",
        "--log-level",
        type=int,
        default=4,
        choices=[1, 2, 3, 4, 5],
        help="Set the logging level",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress command output"
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=1,
        choices=[0, 1, 2],
        help="Set the verbosity level",
    )
    parser.add_argument("-i", "--indent", action="store_true", help="Indent log output")
    parser.add_argument(
        "-o",
        "--outdir",
        default=None,
        help="Install prefix (default: None)",
    )

    # Subcommands (mutually exclusive, first one is accepted)
    # e.g. python main.py resolve or python main.py clean fetch build
    # e.g. python main.py fetch build
    subparsers = parser.add_subparsers(dest="subcommand")
    subparsers.add_parser("clean", help="Clean contribs")
    subparsers.add_parser("fetch", help="Fetch contribs")
    subparsers.add_parser("patch", help="Patch contribs")
    subparsers.add_parser("build", help="Build contribs")
    subparsers.add_parser("resolve", help="Resolve contribs")

    # If no subcommand is specified, default to resolve
    parser.set_defaults(subcommand="resolve")
    # In the case of no subcommand, the package is specified with --pkg
    # e.g. python main.py --pkg zlib
    parser.add_argument(
        "-p",
        "--pkg",
        default="all",
        help="Package to operate on (default: all)",
    )

    def add_extra_options(parser):
        # Recursive operation on dependencies
        # (operations other than clean and resolve)
        parser.add_argument(
            "-r",
            "--recurse",
            action="store_true",
            help="Recursively operate on dependencies",
        )
        # Force operation on package
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            help="Force operation on package"
        )

    # Default package argument (same for all subcommands)
    add_extra_options(parser)

    # Subcommand optional package argument (same for all subcommands)
    # All is the default if no package is specified.
    for subcommand in subparsers.choices:
        subparsers.choices[subcommand].add_argument(
            "pkg", nargs="?", default="all", help="Package to operate on (default: all)"
        )
        # Add the extra options to each subcommand
        add_extra_options(subparsers.choices[subcommand])

    parsed_args = parser.parse_args()

    # Tweak the logging level and verbosity based on the command line args.
    parsed_args.log_level=((6 - parsed_args.log_level) * 10)
    parsed_args.verbose=(parsed_args.verbosity >= 1)

    # if the operation is RESOLVE, then it's recursive
    parsed_args.recurse=(parsed_args.subcommand == "resolve")

    return parsed_args

def get_md5_for_path(path):
    hash = None
    hasher = hashlib.md5()
    for root, _, files in os.walk(path, topdown=True):
        for name in files:
            fileName = os.path.join(root, name)
            with open(str(fileName), "rb") as aFile:
                buf = aFile.read()
                hasher.update(buf)
                hash = hasher.hexdigest()
    return hash