#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Callable
import math


class LazyProperty:
    def __init__(self, func: Callable):
        self._func = func
        self.varname = f"var_{func.__name__}"

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner=None):
        if self is None:
            return self
        if hasattr(instance, self.varname):
            val = getattr(instance, self.varname)
            print(f"returning {self.varname}")
            return val
        val = self._func(instance)
        setattr(instance, self.varname, val)
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
