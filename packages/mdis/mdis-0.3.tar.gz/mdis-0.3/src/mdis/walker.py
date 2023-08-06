from . import dispatcher as _dispatcher


class WalkerMeta(_dispatcher.DispatcherMeta):
    pass


class Walker(_dispatcher.Dispatcher, metaclass=WalkerMeta):
    @_dispatcher.Hook(tuple, list, set, frozenset)
    def dispatch_sequence(self, instance):
        for item in instance:
            yield item
            yield from self(item)

    @_dispatcher.Hook(dict)
    def dispatch_mapping(self, instance):
        for (key, value) in instance.items():
            yield (key, value)
            yield from self((key, value))

    @_dispatcher.Hook(object)
    def dispatch_object(self, instance):
        yield from ()
