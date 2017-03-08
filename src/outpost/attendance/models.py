from django.db import models
from django_fsm import (
    FSMField,
    transition,
)


class Student(models.Model):
    matriculation = models.PositiveIntegerField(primary_key=True)

    def __str__(self):
        return '{s.matriculation}'.format(s=self)


class Holding(models.Model):
    state = FSMField(default='pending')
    campusonline = models.IntegerField()

    @transition(field=state, source='pending', target='running')
    def start(self):
        pass

    @transition(field=state, source='running', target='finished')
    def end(self):
        pass

    @transition(field=state, source='pending', target='canceled')
    def cancel(self):
        pass


class Entry(models.Model):
    student = models.ForeignKey('Student')
    holding = models.ForeignKey('Holding', null=True, blank=True)
    registered = models.DateTimeField(auto_now_add=True)
    assigned = models.DateTimeField(null=True, blank=True)
    quit = models.DateTimeField(null=True, blank=True)
    complete = models.DateTimeField(null=True, blank=True)
    state = FSMField(default='registered')

    @transition(field=state, source='registered', target='canceled')
    def cancel(self):
        pass

    @transition(field=state, source='registered', target='assigned')
    def assign(self, holding):
        # TODO: Various checks to see it holding is correct.
        self.holding = holding

    @transition(field=state, source='assigned', target='canceled')
    def pullout(self):
        pass

    @transition(field=state, source='assigned', target='left')
    def leave(self):
        pass

    @transition(field=state, source=('assigned', 'left'), target='complete')
    def complete(self):
        pass
