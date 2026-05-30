# test_sizedrecord_fmt.py

from polyheader import PolyHeader


def test_polyheader():
    with open("polys.bin", "rb") as fd:
        ph = PolyHeader(fd.read(PolyHeader._size))
    assert ph.code == 4660
    assert ph.min.x == 0.5
    assert ph.min.y == 0.5
    assert ph.max.x == 7.0
    assert ph.max.y == 9.2
    assert ph.num_polys == 3
