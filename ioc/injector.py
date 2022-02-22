import functools
import inspect

from ioc.static import get, exists


def inject(_init_func):
    @functools.wraps(_init_func)
    def inner(cls, *args, **kwds):
        ioc = kwds.pop("__from_ioc__", None)

        # create class with given arguments and keywords
        if ioc is None:
            return _init_func(cls, *args, **kwds)

        signature = inspect.signature(_init_func)
        cls_args = []
        cls_kwds = {}
        for p in signature.parameters.values():
            if p.name == "self":
                continue
            elif p.kind == p.POSITIONAL_ONLY:
                if exists(p.annotation):
                    cls_args.append(get(p.annotation))
            elif p.kind == p.KEYWORD_ONLY or p.kind == p.POSITIONAL_OR_KEYWORD:
                if exists(p.annotation):
                    cls_kwds[p.name] = get(p.annotation)
        return _init_func(cls, *tuple(cls_args), *args, **cls_kwds, **kwds)

    return inner
