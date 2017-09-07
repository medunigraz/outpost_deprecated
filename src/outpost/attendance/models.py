from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django_fsm import (
    FSMField,
    transition,
)


class Terminal(models.Model):
    campusonline = models.ForeignKey(
        'geo.Room',
        null=True,
        blank=True,
        related_name='+'
    )
    enabled = models.BooleanField(
        default=False
    )
    online = models.BooleanField(
        default=False
    )
    hostname = models.CharField(
        max_length=128
    )
    config = JSONField()


class Lecturer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    campusonline = models.IntegerField()

    def __str__(self):
        return '{s.user}'.format(s=self)


class Student(models.Model):
    matriculation = models.PositiveIntegerField()
    campusonline = models.IntegerField()

    def __str__(self):
        return '{s.matriculation}'.format(s=self)


class Card(models.Model):
    serial = models.CharField(max_length=32)
    student = models.ForeignKey('Student')
    enabled = models.BooleanField(default=True)


class Holding(models.Model):
    state = FSMField(default='pending')
    campusonline = models.IntegerField()
    room = models.ForeignKey(
        'geo.Room'
    )
    lecturer = models.ForeignKey('Lecturer')
    initiated = models.DateTimeField(null=True, blank=True)
    finished = models.DateTimeField(null=True, blank=True)

    @transition(field=state, source='pending', target='running')
    def start(self):
        for e in Entry.objects.filter(room=self.room, holding=None):
            e.assign(holding)
            e.save()
        self.initiated = timezone.now()

    @transition(field=state, source='running', target='finished')
    def end(self):
        for e in Entry.objects.filter(holding=self):
            e.complete()
            e.save()
        self.finished = timezone.now()

    @transition(field=state, source='pending', target='canceled')
    def cancel(self):
        for e in Entry.objects.filter(holding=self):
            e.pullout()
            e.save()


class Entry(models.Model):
    student = models.ForeignKey('Student')
    room = models.ForeignKey('geo.Room', null=True, blank=True)
    holding = models.ForeignKey('Holding', null=True, blank=True)
    registered = models.DateTimeField(auto_now_add=True)
    assigned = models.DateTimeField(null=True, blank=True)
    quit = models.DateTimeField(null=True, blank=True)
    completed = models.DateTimeField(null=True, blank=True)
    state = FSMField(default='registered')

    @transition(field=state, source='registered', target='canceled')
    def cancel(self):
        return

    @transition(field=state, source='registered', target='assigned')
    def assign(self, holding):
        self.holding = holding
        self.assigned = timezone.now()

    @transition(field=state, source='assigned', target='canceled')
    def pullout(self):
        self.quit = timezone.now()

    @transition(field=state, source='assigned', target='left')
    def leave(self):
        self.quit = timezone.now()

    @transition(field=state, source=('assigned', 'left'), target='complete')
    def complete(self):
        self.completed = timezone.now()
        # TODO: Find out if next planed holding has same student in it
        if False:
            Entry.objects.create(
                student=self.student,
                room=self.room
            )
