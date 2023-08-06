import contextlib as _contextlib

from . import dispatcher as _dispatcher


class VisitorMeta(_dispatcher.DispatcherMeta):
    pass


class Visitor(_dispatcher.Dispatcher, metaclass=VisitorMeta):
    @_dispatcher.Hook(object)
    @_contextlib.contextmanager
    def dispatch_object(self, instance):
        yield instance
