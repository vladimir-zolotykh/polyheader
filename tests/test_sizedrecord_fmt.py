# test_sizedrecord_fmt.py

from polyheader import PolyHeader, SizedRecord


def test_sizedrecord_fmt():
    points = []

    with open("polys.bin", "rb") as fd:
        ph = PolyHeader(fd.read(PolyHeader._size))

        for _ in range(ph.num_polys):
            rec = SizedRecord.from_file(fd)
            points.extend(rec.iter_as("<dd"))

    assert points == [
        (1.0, 2.5),
        (3.5, 4.0),
        (2.5, 1.5),
        (7.0, 1.2),
        (5.1, 3.0),
        (0.5, 7.5),
        (0.8, 9.0),
        (3.4, 6.3),
        (1.2, 0.5),
        (4.6, 9.2),
    ]
