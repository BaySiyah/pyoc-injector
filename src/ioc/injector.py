import functools
import inspect

from ioc.static import get, exists


def inject(_init_func):
    @functools.wraps(_init_func)
    def inner(cls, *args, **kwds):
        ioc = kwds.pop("__from_ioc__", None)

        if ioc is None:
            return _init_func(cls, *args, **kwds)

        signature = inspect.signature(_init_func)
        args = [x for x in args]
        kwds = kwds.copy()
        for p in signature.parameters.values():
            if p.name == "self" or not exists(p.annotation):
                continue
            elif p.kind == p.POSITIONAL_ONLY:
                args.append(get(p.annotation))
            elif p.kind == p.KEYWORD_ONLY or p.kind == p.POSITIONAL_OR_KEYWORD:
                kwds[p.name] = get(p.annotation)
        return _init_func(cls, *tuple(args), **kwds)

    return inner
