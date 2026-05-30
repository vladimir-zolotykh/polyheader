#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import BinaryIO, Any
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
            # return struct.unpack_from(fmt, instance.view, self.offset)
            tup = struct.unpack_from(fmt, instance.view, self.offset)
            if len(tup) == 1:
                return tup[0]
            else:
                return tup
            return struct.unpack_from(fmt, instance.view, self.offset)
        elif isinstance(self.fmt_or_type, FieldMeta):
            view: FieldMeta = self.fmt_or_type
            a = self.offset
            z = self.offset + view._size
            return view(instance.view[a:z])


class FieldMeta(type):
    _size = 0

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

    def as_tuple(self) -> tuple[Any, ...]:
        return tuple((getattr(self, name) for name in self._fields))

    def as_csv(self) -> str:
        return ", ".join((f"{f}={getattr(self, f)!r}" for f in self._fields))


class SizedRecord:
    def __init__(self, bytesdata: bytes | memoryview):
        self.view = memoryview(bytesdata)

    @classmethod
    def from_file(cls, fd: BinaryIO):
        (nbytes,) = struct.unpack("<i", fd.read(struct.calcsize("<i")))
        return cls(fd.read(nbytes - 4))

    def iter_as(self, fmt_or_type: str or FieldMeta):
        if isinstance(fmt_or_type, str):
            for off in range(0, len(self.view), struct.calcsize(fmt_or_type)):
                z = off + struct.calcsize(fmt_or_type)
                yield struct.unpack_from(fmt_or_type, self.view[off:z])
        elif isinstance(fmt_or_type, FieldMeta):
            for off in range(0, len(self.view), fmt_or_type._size):
                z = off + fmt_or_type._size
                yield fmt_or_type(self.view[off:z])


def as_tuple(view: FieldMeta) -> tuple[Any, ...]:
    if hasattr(view, "_fields"):
        return tuple((as_tuple(getattr(view, name)) for name in view._fields))
    else:
        return str(view)


class Point(View):
    x = "<d"
    y = "<d"


class PolyHeader(View):
    code = "<i"
    min = Point
    max = Point
    num_polys = "<i"


if __name__ == "__main__":
    with open("polys.bin", "rb") as fd1, open("polys.bin", "rb") as fd2:
        ph = PolyHeader(fd1.read(PolyHeader._size))
        print(as_tuple(ph))
        points = []
        for _ in range(ph.num_polys):
            rec = SizedRecord.from_file(fd1)
            points.extend(rec.iter_as("<dd"))
        print(points)
        ph = PolyHeader(fd2.read(PolyHeader._size))
        print(as_tuple(ph))
        points = []
        for _ in range(ph.num_polys):
            rec = SizedRecord.from_file(fd2)
            for pp in rec.iter_as(Point):
                points.append(tuple((pp.x, pp.y)))
        print(points)
