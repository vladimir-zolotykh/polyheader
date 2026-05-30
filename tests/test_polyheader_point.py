import struct

from polyheader import Point, PolyHeader, as_tuple


def test_point_size():
    assert Point._size == struct.calcsize("<dd")


def test_polyheader_size():
    expected = struct.calcsize("<i") + Point._size + Point._size + struct.calcsize("<i")
    assert PolyHeader._size == expected


def test_point_fields():
    data = struct.pack("<dd", 1.25, 2.5)

    p = Point(data)

    assert p.x == 1.25
    assert p.y == 2.5


def test_point_as_tuple():
    data = struct.pack("<dd", 10.0, 20.0)

    p = Point(data)

    assert p.as_tuple() == (10.0, 20.0)


def test_point_as_csv():
    data = struct.pack("<dd", 1.0, 2.0)

    p = Point(data)

    assert p.as_csv() == "x=1.0, y=2.0"


def test_polyheader_fields():
    data = struct.pack(
        "<i4d i",
        123,
        1.0,
        2.0,  # min
        10.0,
        20.0,  # max
        7,
    )

    ph = PolyHeader(data)

    assert ph.code == 123

    assert ph.min.x == 1.0
    assert ph.min.y == 2.0

    assert ph.max.x == 10.0
    assert ph.max.y == 20.0

    assert ph.num_polys == 7


def test_polyheader_as_tuple():
    data = struct.pack(
        "<i4d i",
        99,
        1.0,
        2.0,
        3.0,
        4.0,
        5,
    )

    ph = PolyHeader(data)

    assert as_tuple(ph) == (
        99,
        (1.0, 2.0),
        (3.0, 4.0),
        5,
    )


def test_polyheader_as_tuple_method():
    data = struct.pack(
        "<i4d i",
        42,
        11.0,
        12.0,
        21.0,
        22.0,
        9,
    )

    ph = PolyHeader(data)
    assert as_tuple(ph) == (42, as_tuple(ph.min), as_tuple(ph.max), 9)


def test_class_attribute_returns_descriptor():
    from polyheader import Field

    assert isinstance(Point.x, Field)
    assert isinstance(Point.y, Field)
    assert isinstance(PolyHeader.code, Field)


def test_memoryview_input():
    data = memoryview(struct.pack("<dd", 5.0, 6.0))

    p = Point(data)

    assert p.x == 5.0
    assert p.y == 6.0


def test_polyheader_nested_offsets():
    assert PolyHeader.code.offset == 0
    assert PolyHeader.min.offset == struct.calcsize("<i")

    assert PolyHeader.max.offset == struct.calcsize("<i") + Point._size

    assert PolyHeader.num_polys.offset == struct.calcsize("<i") + Point._size * 2
