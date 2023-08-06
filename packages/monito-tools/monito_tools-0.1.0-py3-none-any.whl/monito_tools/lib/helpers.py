import functools


def memoize(fn=None, **kwargs):
    """
    Caching wrapper that makes a function store
    previous arguments-return pairs in a dict
    and returns the appropriate value if the combination of
    arguments has been seen previously
    """
    if fn is None:
        return lambda _fn: memoize(_fn, **kwargs)
    return functools.lru_cache(**kwargs)(fn)
