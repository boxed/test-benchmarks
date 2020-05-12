from nose2.tools import params


@params(*range(5000))
def test_foo(x):
    pass
