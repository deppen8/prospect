
# import pytest
import surveysim


def test_returns_SimSession(a_simulation):
    assert isinstance(a_simulation, surveysim.SimSession)


def test_has_engine_attribute(a_simulation):
    assert hasattr(a_simulation, 'engine')


def test_has_session_attribute(a_simulation):
    assert hasattr(a_simulation, 'session')
