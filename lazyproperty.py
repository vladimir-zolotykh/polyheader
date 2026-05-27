#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Callable
import math


class LazyProperty:
    def __init__(self, func: Callable):
        self._func = func
        self.varname = f"var_{func.__name__}"

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        try:
            val = instance.__dict__[self.varname]
            print(f"returning {self.varname}")
            return val
        except KeyError:
            val = self._func(instance)
            instance.__dict__[self.varname] = val
            return val


class Circle:
    def __init__(self, radius):
        self._radius = radius

    @LazyProperty
    def area(self):
        print("calculating area")
        return math.pi * self._radius**2

    @LazyProperty
    def circumference(self):
        print("calculating circumference")
        return 2 * math.pi * self._radius


if __name__ == "__main__":
    c = Circle(12.2)
    for _ in range(5):
        print(c.area)
        print(c.circumference)
