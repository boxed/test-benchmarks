from time import sleep

import pytest


@pytest.fixture(scope='session')
def slow_fixture():
    sleep(2)


@pytest.mark.parametrize("x", range(500))
def test_foo(x, slow_fixture):
    pass
