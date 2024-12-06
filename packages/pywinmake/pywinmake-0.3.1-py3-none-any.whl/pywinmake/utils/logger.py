#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPDX-License-Identifier: MIT License
Copyright (c) 2023 Savoir-faire Linux

A wrapper around the logging module to provide a more useful logging format.
"""

import logging
import traceback


root_logger = logging.getLogger(__name__)


class CustomAdapter(logging.LoggerAdapter):
    @staticmethod
    def indent():
        indentation_level = len(traceback.extract_stack())
        return indentation_level - 4 - 2  # Remove logging infrastructure frames

    def set_indent(self, do_indent):
        self.do_indent = do_indent

    def process(self, msg, kwargs):
        indent = self.indent() if self.do_indent else 0
        return "{i}{m}".format(i=" " * (indent), m=msg), kwargs


class Logger:
    def __init__(self):
        self.impl = None
        self.init()

    def init(self, lvl=logging.DEBUG, verbose=False, do_indent=False):
        format = ""
        if verbose:
            # NOTE: we can add in funcName/filename if we want.
            format = "[ %(levelname)-7s %(created).2f %(filename)16s:%(lineno)4s ] "
        fmt = format + "%(message)s"
        # Try to use coloredlogs if it's available.
        try:
            import coloredlogs

            coloredlogs.install(
                level=lvl,
                logger=root_logger,
                fmt=fmt,
                level_styles={
                    "debug": {"color": "blue"},
                    "info": {"color": "green"},
                    "warn": {"color": "yellow"},
                    "error": {"color": "red"},
                    "critical": {"color": "red", "bold": True},
                },
                field_styles={
                    "asctime": {"color": "magenta"},
                    "created": {"color": "magenta"},
                    "levelname": {"color": "cyan"},
                    "funcName": {"color": "black", "bold": True},
                    "lineno": {"color": "black", "bold": True},
                },
            )
        except ImportError:
            root_logger.setLevel(lvl)
            logging.basicConfig(level=lvl, format=fmt)

        if self.impl is not None:
            self.impl.set_indent(do_indent)
            return self.impl

        self.impl = CustomAdapter(logging.getLogger(__name__), {})
        self.impl.set_indent(do_indent)


logger = Logger()
log = logger.impl
