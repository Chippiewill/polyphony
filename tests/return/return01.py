from polyphony import testbench
from polyphony.typing import Axi, List, int32, int128


def return01(x: Axi[int32], y: List) -> Axi[int32]:
    z = x
    for v in y:
        z += v
    return z


@testbench
def test():
    l = [1, 2, 3, 4, 6, 7, 8, 9, 10, 55, 88] * 10
    assert 1 == return01(0, l)
    l2 = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11]
    assert 2 == return01(1, l2)
test()
