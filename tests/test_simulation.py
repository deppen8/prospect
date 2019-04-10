# import pytest
import prospect


def test_returns_SimSession(a_simulation):
    assert isinstance(a_simulation, prospect.SimSession)


def test_has_desired_attributes(a_simulation):
    for a in ["engine", "session"]:
        assert hasattr(a_simulation, a)
