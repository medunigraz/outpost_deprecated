from django.contrib.gis.db import models

from outpost.base.fields import ForeignDataWrapperKey


class TestModel(models.Model):
    name = models.TextField()
    campusonline = ForeignDataWrapperKey(
        'campusonline.Building',
        on_delete=models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )

    def __str__(self):
        if not self.campusonline:
            return self.name or 'Building'
        return '{s.name} [CO: {s.campusonline}]'.format(s=self)
