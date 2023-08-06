__all__ = [
    "Dispatcher",
    "DispatcherMeta",
    "Hook",
]

import collections
import functools
import inspect
import types


class Hook(object):
    def __init__(self, *typeids):
        for typeid in typeids:
            if not callable(typeid):
                raise ValueError(typeid)
        self.__typeids = typeids
        return super().__init__()

    def __iter__(self):
        yield from self.__typeids

    def __repr__(self):
        names = []
        for typeid in self.__typeids:
            name = typeid.__qualname__
            module = typeid.__module__
            if module not in ("builtins",):
                name = f"{module}.{name}"
            names.append(name)
        return f"<{', '.join(names)}>"

    def __call__(self, call):
        class ConcreteHook(Hook):
            def __call__(self, dispatcher, instance):
                return call(self=dispatcher, instance=instance)

        return ConcreteHook(*tuple(self))


class DispatcherMeta(type):
    __hooks__ = {}

    def __new__(metacls, name, bases, ns):
        hooks = {}
        ishook = lambda member: isinstance(member, Hook)

        for basecls in reversed(bases):
            members = inspect.getmembers(basecls, predicate=ishook)
            for (_, hook) in members:
                hooks.update(dict.fromkeys(hook, hook))

        conflicts = collections.defaultdict(list)
        for (key, value) in tuple(ns.items()):
            if not ishook(value):
                continue
            hook = value
            for typeid in hook:
                hooks[typeid] = hook
                conflicts[typeid].append(key)
            ns[key] = hook

        for (typeid, keys) in conflicts.items():
            if len(keys) > 1:
                raise ValueError(f"dispatch conflict: {keys!r}")

        ns["__hooks__"] = types.MappingProxyType(hooks)

        return super().__new__(metacls, name, bases, ns)

    @functools.lru_cache(maxsize=None)
    def dispatch(cls, typeid=object):
        hook = cls.__hooks__.get(typeid)
        if hook is not None:
            return hook
        for (checker, hook) in cls.__hooks__.items():
            if not isinstance(checker, type) and checker(typeid):
                return hook
        return None


class Dispatcher(metaclass=DispatcherMeta):
    def __call__(self, instance):
        for typeid in instance.__class__.__mro__:
            hook = self.__class__.dispatch(typeid=typeid)
            if hook is not None:
                break
        if hook is None:
            hook = self.__class__.dispatch()
        return hook(dispatcher=self, instance=instance)

    @Hook(object)
    def dispatch_object(self, instance):
        raise NotImplementedError()
