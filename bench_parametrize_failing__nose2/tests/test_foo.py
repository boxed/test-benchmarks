from nose2.tools import params


@params(*range(500))
def test_foo(x):
    assert False
