from django.db import models
from django.utils.translation import gettext_lazy as _

from outpost.base.decorators import signal_connect


class System(models.Model):
    name = models.CharField(
        max_length=128
    )
    home_template = models.CharField(
        max_length=256,
        default='/home/{username}'
    )
    same_group_id = models.BooleanField(
        default=True
    )
    same_group_name = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name


class Host(models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=64
    )
    system = models.ForeignKey(
        'System',
        blank=True,
        null=True
    )

    class Meta:
        permissions = (
            ('view_host', _('View host')),
        )

    def __str__(self):
        return self.name


@signal_connect
class SystemUser(models.Model):
    system = models.ForeignKey('System')
    user = models.ForeignKey('User')
    shell = models.CharField(
        max_length=256,
        default='/bin/bash'
    )
    groups = models.ManyToManyField(
        'Group',
        blank=True
    )
    sudo = models.BooleanField(
        default=False
    )

    def post_save(self, *args, **kwargs):
        for group in self.groups.all():
            if group not in self.system.group_set.all():
                self.system.group_set.add(group)

    def __str__(self):
        return f'{self.user.person.username}@{self.system} (self.user)'


class User(models.Model):
    person = models.OneToOneField(
        'campusonline.Person',
        db_constraint=False
    )
    systems = models.ManyToManyField(
        'System',
        through='SystemUser',
        blank=True
    )

    @property
    def username(self):
        return self.person.username

    @property
    def email(self):
        return self.person.email

    def __str__(self):
        return f'{self.person} ({self.pk})'


class Group(models.Model):
    name = models.CharField(
        max_length=31
    )
    systems = models.ManyToManyField(
        'System',
        blank=True
    )

    def __str__(self):
        return f'{self.name} ({self.pk})'
