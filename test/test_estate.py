
__author__ = 'simon.ballu@gmail.com'


from monopoly.Estate import EstateFactory, Estate, StationEstate, DiceEstate
import pytest


def test_estate_factory():
    estates = EstateFactory.get_default_estates()

    assert len(estates) == 28
    assert len([e for e in estates if isinstance(e, StationEstate)]) == 4
    assert len([e for e in estates if isinstance(e, DiceEstate)]) == 2