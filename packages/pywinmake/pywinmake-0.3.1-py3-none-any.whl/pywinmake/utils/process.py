#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPDX-License-Identifier: MIT License
Copyright (c) 2023 Savoir-faire Linux

A helper class and functions for running scripts using various Windows shells.
Shell options are:
    - cmd.exe
    - powershell.exe
    - bash.exe (Git Bash or Windows Subsystem for Linux)
"""

import json
import os
import shlex
import shutil
import subprocess
import sys

from .logger import log
from ..dev_env.host_config import config


class ScriptType:
    ps1 = 0
    cmd = 1
    sh = 2


def shellquote(s, windows=False):
    if not windows:
        return "'" + s.replace("'", "'''") + "'"
    else:
        return '"' + s + '"'


class ShExecutor:
    def __init__(self):
        sys_path = (r"\Sysnative", r"\system32")[config.python_is_64bit]
        full_sys_path = os.path.expandvars("%systemroot%") + sys_path

        # powershell
        self.ps_path = os.path.join(
            full_sys_path, "WindowsPowerShell", "v1.0", "powershell.exe"
        )
        if not os.path.exists(self.ps_path):
            log.error("Powershell not found at %s." % self.ps_path)
            sys.exit(1)

        # bash
        if not os.environ.get("JENKINS_URL"):
            self.sh_path = os.path.join(full_sys_path, "bash.exe")
        else:
            self.sh_path = os.path.join("C:", "Program Files", "Git", "git-bash.exe")

        if not os.path.exists(self.sh_path):
            log.warning(f"Bash not found at {self.sh_path}.")
            self.sh_path = shutil.which("bash.exe")
            if not os.path.exists(self.sh_path):
                log.error("No bash found")
                sys.exit(1)
            else:
                self.sh_path = shellquote(self.sh_path, windows=True)
                log.debug(f"Using alternate bash found at {self.sh_path}")

        # system env vars (if nothing else is specified)
        self.base_env_vars = os.environ.copy()

        # extra env vars
        self.extra_env_vars = {}

        self.stdout = sys.stdout
        self.debug_cmd = False

    def append_extra_env_vars(self, env_vars):
        """Append extra env vars to the current environment"""
        self.extra_env_vars.update(env_vars)

    def set_quiet_mode(self, quiet=False):
        """Mute stdout if quiet is True"""
        self.stdout = (sys.stdout, subprocess.PIPE)[quiet]

    def set_debug_cmd(self, debug=False):
        """Print the command being executed if debug is True"""
        self.debug_cmd = debug

    def exec_script(self, script_type=ScriptType.cmd, script=None, args=[], silent=False):
        if script_type is ScriptType.cmd:
            cmd = [script]
            if not args:
                cmd = shlex.split(script)
        elif script_type is ScriptType.ps1:
            cmd = [self.ps_path, "-ExecutionPolicy", "ByPass", script]
        elif script_type is ScriptType.sh:
            cmd = [self.sh_path, "-c ", '"' + script]
        if args:
            cmd.extend(args)
        if script_type is ScriptType.sh:
            cmd[-1] = cmd[-1] + '"'
            cmd = " ".join(cmd)
        run_env = (
            self.extra_env_vars
            if self.extra_env_vars
            else self.base_env_vars
            if self.base_env_vars
            else None
        )
        if self.debug_cmd:
            print(cmd if script_type is ScriptType.sh else " ".join(cmd))
        if silent:
            stdout = subprocess.DEVNULL
            stderr = subprocess.DEVNULL
        else:
            stdout = self.stdout
            stderr = subprocess.STDOUT
        p = subprocess.Popen(
            cmd,
            shell=True,
            stdout=stdout,
            stderr=stderr,
            env=run_env,
        )
        rtrn, perr = p.communicate()
        rcode = p.returncode
        data = None
        if perr:
            data = json.dumps(perr.decode("utf-8", "ignore"))
        else:
            data = rtrn
        return rcode, data

    def cmd(self, script=None, args=[], silent=False):
        return self.exec_script(ScriptType.cmd, script, args, silent)

    def ps1(self, script=None, args=[], silent=False):
        return self.exec_script(ScriptType.ps1, script, args, silent)

    def bash(self, script=None, args=[], silent=False):
        return self.exec_script(ScriptType.sh, script, args, silent)


sh_exec = ShExecutor()
