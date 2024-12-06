#!/usr/bin/env python3
# coding=utf-8

try:
    import easyarg
except:
    print("Install this package first")
    raise

ea = easyarg.EasyArg()


@ea.command()
def add(x: int, y: int = 0) -> int:
    """Add two numbers"""
    print(f"{x + y=}")


@ea.command()
def mul(a: float | str, B: float, c: float = 1.0) -> float:
    """Multiply numbers"""
    print(f"{(a * B * c)=}")


if __name__ == "__main__":
    ea.parse()
