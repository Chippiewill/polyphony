from polyphony import testbench
from polyphony.typing import Axi, List, int32, int128


def return01(z: Axi[int32], xs: Axi[list]) -> Axi[int32]:
    r = z
    for x in xs:
        r += x
    return r


@testbench
def test():
    l = [1, 2, 3, 4, 5]
    assert 2 == return01(3, l)
    l = [1, 2, 3, 4, 5, 6]
    assert 2 == return01(4, l)
test()
