__all__ = [
    "ContextVisitor",
    "Visitor",
    "VisitorMeta",
]

import contextlib

from . import dispatcher


class VisitorMeta(dispatcher.DispatcherMeta):
    pass


class Visitor(dispatcher.Dispatcher, metaclass=VisitorMeta):
    @dispatcher.Hook(object)
    def dispatch_object(self, instance):
        return instance


class ContextVisitor(Visitor):
    @dispatcher.Hook(object)
    @contextlib.contextmanager
    def dispatch_object(self, instance):
        yield super().__call__(instance=instance)
