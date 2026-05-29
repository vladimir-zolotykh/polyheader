#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import struct


class Field:
    def __init__(self, name: str, fmt: str, offset: int):
        self.fmt = fmt
        self.offset = offset

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return struct.unpack_from(self.fmt, instance.view, self.offset)


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
        clsdict["_size"] = offset
        clsdict["_fields"] = fields
        return super().__new__(mcls, clsname, bases, clsdict)


class View(metaclass=FieldMeta):
    def __init__(self, bytesdata):
        self.view = memoryview(bytesdata)


class PolyHeader(View):
    code = "<i"
    min_x = "d"
    min_y = "d"
    max_x = "d"
    max_y = "d"
    num_polys = "i"


if __name__ == "__main__":
    with open("polys.bin", "rb") as fd:
        ph = PolyHeader(fd.read(PolyHeader._size))
        print(ph._fields)
        print(ph._size)
        print(ph.code)
