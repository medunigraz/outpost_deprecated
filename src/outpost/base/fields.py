import hashlib

from django.db import models
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from django.dispatch import Signal
from django.utils.encoding import force_text


def _hash_field_name(name):
    return '{name}_markup_type'.format(name=name)


def _filter_fields(include, exclude):
    def _filter(field):
        if exclude:
            if field.name in exclude:
                return False
        if include:
            if field.name in include:
                return True
        return True
    return _filter


def _get_hash(algorithm, obj, fields):
    bucket = hashlib.new(algorithm)
    for f in fields:
        bucket.update(force_text(f.value_from_object(obj)).encode('utf-8'))
    return bucket.digest()


foreign_data_changed = Signal(providing_args=['instance', 'field'])


class ForeignDataWrapperDescriptor(ForwardManyToOneDescriptor):

    def __init__(self, field, algorithm, filter_instance):
        super(ForeignDataWrapperDescriptor, self).__init_(field)
        self.hash_field_name = _hash_field_name(self.field.name)
        self.algorithm = algorithm
        self.filter_instance = filter_instance

    def __get__(self, instance, cls=None):
        rel = super(ForeignDataWrapperDescriptor, self).__get__(instance, cls)

        def _is_dirty(obj):
            hashsum_old = getattr(obj, self.hash_field_name, None)
            fields = filter(self.filter_instance, obj._meta.fields)
            hashsum_new = _get_hash(self.algorithm, fields)
            return hashsum_old != hashsum_new

        setattr(rel, 'is_dirty', _is_dirty)
        return rel


class ForeignDataWrapperKey(models.ForeignKey):

    def __init__(self, to, fields=None, exclude=None, algorithm='sha256',
                 *args, **kwargs):
        self.fields = fields
        self.exclude = exclude
        self.algorithm = algorithm
        self.blank = kwargs.get('blank', False)
        self.null = kwargs.get('null', False)
        kwargs['related_name'] = '+'
        super(ForeignDataWrapperKey, self).__init__(to, *args, **kwargs)

    def contribute_to_class(self, cls, name):
        if not cls._meta.abstract:
            hash_field = models.BinaryField(
                editable=False,
                blank=self.blank,
                null=self.null
            )
            hash_field.creation_counter = self.creation_counter + 1
            cls.add_to_class(_hash_field_name(name), hash_field)
        super(ForeignDataWrapperKey, self).contribute_to_class(cls, name)

        setattr(
            cls,
            self.name,
            ForeignDataWrapperDescriptor(
                self,
                name,
                self.algorithm,
                _filter_fields(self.fields, self.exclude)
            )
        )

    def pre_save(self, model_instance, add):
        val = super(ForeignDataWrapperKey, self).pre_save(model_instance, add)
        if val is not None:
            filter_instance = _filter_fields(self.fields, self.exclude)
            fields = filter(filter_instance, val._meta.fields)
            hashsum = _get_hash(self.algorithm, fields)
        else:
            hashsum = None
        if getattr(model_instance, _hash_field_name(self.attname)) != hashsum:
            foreign_data_changed.send(
                sender=self.__class__,
                instance=model_instance,
                field=self.attname
            )
        setattr(model_instance, _hash_field_name(self.attname), hashsum)
        return val
