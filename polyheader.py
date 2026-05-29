#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
import struct


class Field:
    def __init__(self, name: str, fmt_or_type: str | FieldMeta, offset: int):
        self.fmt_or_type = fmt_or_type
        self.offset = offset

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if isinstance(self.fmt_or_type, str):
            fmt: str = self.fmt_or_type
            return struct.unpack_from(fmt, instance.view, self.offset)
        elif isinstance(self.fmt_or_type, FieldMeta):
            view: FieldMeta = self.fmt_or_type
            a = self.offset
            z = self.offset + view._size
            return view(instance.view[a:z])


class FieldMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        offset = 0
        fields = []
        for name, val in clsdict.items():
            if name.startswith("__") and name.endswith("__"):
                continue
            if isinstance(val, str):
                fmt: str = val
                field = Field(name, fmt, offset)
                clsdict[name] = field
                fields.append(name)
                offset += struct.calcsize(fmt)
            elif isinstance(val, FieldMeta):
                view: FieldMeta = val
                clsdict[name] = Field(name, view, offset)
                fields.append(name)
                offset += view._size
        clsdict["_size"] = offset
        clsdict["_fields"] = fields
        return super().__new__(mcls, clsname, bases, clsdict)


class View(metaclass=FieldMeta):
    def __init__(self, bytesdata):
        self.view = memoryview(bytesdata)


class Point(View):
    x = "<d"
    y = "<d"


class PolyHeader(View):
    code = "<i"
    min = Point
    max = Point
    num_polys = "<i"


if __name__ == "__main__":
    with open("polys.bin", "rb") as fd:
        ph = PolyHeader(fd.read(PolyHeader._size))
        print(ph.code)
        print(ph.min.x)
