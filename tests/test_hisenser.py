from pytest import fixture

from hisenser import *


@fixture(scope="session")
def hisense() -> Client:
    with Client("192.168.1.60", foolish=True, secured=True) as hisense:
        yield hisense


def test_attach(hisense: Client):
    hisense.attach()
