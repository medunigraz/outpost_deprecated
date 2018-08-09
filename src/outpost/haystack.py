from xapian_backend import (
    XapianEngine,
    XapianSearchBackend,
)


class SearchBackend(XapianSearchBackend):

    def update(self, index, iterable, commit=True):
        return super().update(index, iterable)

    def remove(self, obj, commit=True):
        return super().remove(obj)


class Engine(XapianEngine):
    backend = SearchBackend
