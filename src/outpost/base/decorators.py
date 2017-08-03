from functools import wraps

from django.db.models.signals import (
    post_save,
    pre_save,
    post_delete,
)


def signal_connect(cls):
    """
    Class decorator that automatically connects pre_save / post_save signals on
    a model class to its pre_save() / post_save() methods.
    """
    def connect(signal, func):
        cls.func = staticmethod(func)

        @wraps(func)
        def wrapper(sender, *args, **kwargs):
            return func(kwargs.get('instance'), *args, **kwargs)

        signal.connect(wrapper, sender=cls)
        return wrapper

    if hasattr(cls, 'pre_save'):
        cls.pre_save = connect(pre_save, cls.pre_save)

    if hasattr(cls, 'post_save'):
        cls.post_save = connect(post_save, cls.post_save)

    if hasattr(cls, 'post_delete'):
        cls.post_delete = connect(post_save, cls.post_delete)

    return cls


def signal_skip(func):
    @wraps(func)
    def _decorator(sender, instance, **kwargs):
        if hasattr(instance, 'skip_signal'):
            return None
        instance.skip_signal = True
        return func(sender, instance, **kwargs)
    return _decorator
