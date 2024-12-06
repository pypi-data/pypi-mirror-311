"""cubicweb-fluid-design-system application package


"""

import inspect


def monkeypatch_default_value(func, arg, value):
    # work on the underlying function object if func is a method, that's
    # where '__defaults__' is actually stored.
    if inspect.ismethod(func):
        func = func.__func__
    getfullargspec = inspect.getfullargspec
    argspec = getfullargspec(func)
    # ArgSpec.args contains regular and named parameters, only keep the latter
    named_args = argspec.args[-len(argspec.defaults) :]
    idx = named_args.index(arg)
    # generate and inject a new '__defaults__' tuple with the new default value
    new_defaults = func.__defaults__[:idx] + (value,) + func.__defaults__[idx + 1 :]
    func.__defaults__ = new_defaults
