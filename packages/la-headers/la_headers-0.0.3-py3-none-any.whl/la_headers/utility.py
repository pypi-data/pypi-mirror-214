from typing import Callable

from packaging.version import Version


def find_best_option(version: str, options: tuple) -> str | None:
    for v, o in options:
        if Version(version) >= Version(v):
            return o
    return None


def find_best_function(version: str, options: tuple) -> Callable | None:
    for v, o in options:
        if Version(version) >= Version(v):
            return o
    return None
