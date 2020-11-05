from time import sleep

import pytest


@pytest.fixture
def slow_fixture():
    sleep(0.2)


@pytest.mark.parametrize("x", range(20))
def test_foo(x, slow_fixture):
    pass
