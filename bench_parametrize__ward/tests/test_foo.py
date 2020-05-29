from ward import test, each


@test('foo{x}')
def _(x=each(*range(500))):
    pass
