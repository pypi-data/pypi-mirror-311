#!/usr/bin/env python3
# coding=utf-8

import sys
import argparse
import functools
import inspect
from typing import Callable, get_args, Optional
import importlib


class _MyArgParser(argparse.ArgumentParser):
    def error(self, message):
        print(message)
        print("----------------------------------")
        print()
        self.print_help()
        sys.exit(1)


class EasyArg:
    """
    Used to generate subparsers for target functions by decorating `@instance.command()`
    Then, call `instance.parse` to run corresponding function based on CLI command
    """

    def __init__(self, description: str = ""):
        """
        Last Update: @2024-11-23 14:35:26
        ---------------------------------
        Initialize:
            - argparse.ArgumentParser & its subparsers
            - functions holder
        """
        self.parser = _MyArgParser(description=description)
        self.subparsers = self.parser.add_subparsers(dest='command', help='Execute functions from CLI commands directly')
        self.functions = {}

    def command(self):
        """
        Last Update: @2024-11-23 14:37:03
        ---------------------------------
        A function decorator, used to generate a subparser and arguments based on the function signature
        """
        def decorator(func: Callable):
            # @ Prepare
            cmd_name = func.__name__
            parser = self.subparsers.add_parser(cmd_name, help=func.__doc__)  # @ exp | Add a subparser with command the same as function name

            # @ Main | Add arguments with proper attributes
            sig = inspect.signature(func)
            for param_name, param in sig.parameters.items():
                # @ Retrieve-type | From annotations, take the first type for the compound types, e.g. get `str`` for `typing.Union[str, float]`
                annotation = param.annotation
                annotations = get_args(annotation)
                if annotations:
                    annotation = annotations[0]

                # @ Get-Attribute
                required = param.default == inspect._empty
                default = None if required else param.default

                # @ Add-Argument | Only support intrinsic types: int, float, str & bool
                if annotation == inspect.Parameter.empty:
                    raise TypeError(f"Parameter '{param_name}' in function '{func.__name__}' missing type hint")
                elif annotation in (int, float, str):
                    parser.add_argument(f"--{param_name}", type=annotation, required=required, default=default, help=f"type={annotation.__name__}, {required=}, {default=}")
                elif annotation == bool:
                    parser.add_argument(f"--{param_name}", action="store_true", required=required, default=default, help=f"type={annotation.__name__}, {required=}, {default=}")
                else:
                    raise TypeError(f"easyarg only supports types: int, float, str & bool, now is {annotation}")

            # @ Post
            self.functions[cmd_name] = func

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper
        return decorator

    def parse(self, args: Optional[list[str]] = None):
        """
        Last Update: @2024-11-23 14:40:31
        ---------------------------------
        Parse arguments and call corresponding function
        """
        args = self.parser.parse_args(args)
        kwargs = {key: value for key, value in vars(args).items() if key != 'command' and value is not None}

        if args.command is None:
            self.parser.print_help()
            return

        func = self.functions[args.command]
        func(**kwargs)
