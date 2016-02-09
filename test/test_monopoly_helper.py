__author__ = 'simon.ballu@gmail.com'

from monopoly.helper import resolve_text

def test_resolve_text():
    assert resolve_text("&1 suce des carottes", "Sonic") == "Sonic suce des carottes"
    assert resolve_text("&1, &2, &3", "caca", "prout", "cul") == "caca, prout, cul"
    assert resolve_text("gruik gruik", "caca", "prout", "cul") == "gruik gruik"
    assert resolve_text("&1, &2, &3") == "&1, &2, &3"