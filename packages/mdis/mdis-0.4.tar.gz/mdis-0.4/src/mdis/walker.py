__all__ = [
    "Walker",
    "WalkerMeta",
]

import dataclasses

from . import dispatcher


class WalkerMeta(dispatcher.DispatcherMeta):
    pass


class Walker(dispatcher.Dispatcher, metaclass=WalkerMeta):
    @dispatcher.Hook(tuple, list, set, frozenset)
    def dispatch_sequence(self, instance):
        for item in instance:
            yield item
            yield from self(item)

    @dispatcher.Hook(dict)
    def dispatch_mapping(self, instance):
        for (key, value) in instance.items():
            yield (key, value)
            yield from self((key, value))

    @dispatcher.Hook(dataclasses.is_dataclass)
    def dispatch_dataclass(self, instance):
        for field in dataclasses.fields(instance):
            key = field.name
            value = getattr(instance, key)
            yield (key, value)
            yield from self((key, value))

    @dispatcher.Hook(object)
    def dispatch_object(self, instance):
        yield from ()
