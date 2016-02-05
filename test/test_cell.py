__author__ = 'simon.ballu@gmail.com'


from monopoly.Cell import CellFactory
import pytest


def test_cell_factory():
    cells = CellFactory.get_default_cells()

    assert len(cells) == 40
