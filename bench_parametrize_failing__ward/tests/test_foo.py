from ward import test, each


@test('foo')
def _(x=each(*range(500))):
    assert False
