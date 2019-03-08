import logging

from django.conf import settings
from django.contrib.postgres.fields import (
    DateTimeRangeField,
    JSONField,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_fsm import (
    FSMField,
    transition,
)
from model_utils.models import TimeStampedModel

from ..base.decorators import signal_connect
from ..base.fields import ChoiceArrayField
from ..base.models import NetworkedDeviceMixin
from .plugins import TerminalBehaviour

logger = logging.getLogger(__name__)


class Terminal(NetworkedDeviceMixin, models.Model):
    rooms = models.ManyToManyField(
        'campusonline.Room',
        db_constraint=False,
        related_name='terminals'
    )
    config = JSONField(
        null=True
    )
    behaviour = ChoiceArrayField(
        base_field=models.CharField(
            max_length=256,
            choices=[(p.qualified(), p.name) for p in TerminalBehaviour.manager().get_plugins()]
        ),
        default=list
    )

    class Meta:
        ordering = (
            'id',
        )
        permissions = (
            ('view_terminal', _('View Terminal')),
        )

    @property
    def plugins(self):
        pm = TerminalBehaviour.manager(lambda p: p.qualified() in self.behaviour)
        return pm

    def __str__(self):
        return self.hostname


@signal_connect
class Entry(models.Model):
    terminal = models.ForeignKey(
        'Terminal'
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    student = models.ForeignKey(
        'campusonline.Student',
        models.DO_NOTHING,
        db_constraint=False,
        related_name='+'
    )
    room = models.ForeignKey(
        'campusonline.Room',
        models.DO_NOTHING,
        db_constraint=False,
        related_name='+'
    )
    status = JSONField(default=list)

    class Meta:
        get_latest_by = 'created'
        permissions = (
            ('view_entry', _('View Entry')),
        )

    def post_save(self, *args, **kwargs):
        if getattr(self, '_post_save', False):
            return
        setattr(self, '_post_save', True)
        if kwargs.get('created', False):
            hook = self.terminal.plugins.hook.create
        else:
            hook = self.terminal.plugins.hook.update
        self.status = hook(entry=self)
        self.save()
        setattr(self, '_post_save', False)

    def __str__(s):
        return f'{s.student} [{s.created}: {s.terminal}]'


class CampusOnlineHolding(models.Model):
    state = FSMField(default='pending')
    course_group_term = models.ForeignKey(
        'campusonline.CourseGroupTerm',
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    room = models.ForeignKey(
        'campusonline.Room',
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    lecturer = models.ForeignKey(
        'campusonline.Person',
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    initiated = models.DateTimeField(
        null=True,
        blank=True
    )
    finished = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        get_latest_by = 'initiated'
        permissions = (
            ('view_campusonlineholding', _('View CAMPUSonline Holding')),
        )

    @transition(field=state, source='pending', target='running')
    def start(self):
        self.initiated = timezone.now()
        coes = CampusOnlineEntry.objects.filter(
            incoming__room=self.room,
            holding=None,
            state='created'
        )
        for coe in coes:
            coe.assign(self)
            coe.save()

    @transition(field=state, source='running', target='finished')
    def end(self):
        coes = CampusOnlineEntry.objects.filter(
            holding=self,
            state__in=('assigned', 'left')
        )
        for coe in coes:
            coe.complete()
            coe.save()
        self.finished = timezone.now()

    @transition(field=state, source=('running', 'pending'), target='canceled')
    def cancel(self):
        query = {
            'holding': self,
            'state__in': (
                'assigned',
                'left',
            )
        }
        for coe in CampusOnlineEntry.objects.filter(**query):
            coe.pullout()
            coe.save()

    def __str__(s):
        return f'{s.course_group_term} [{s.lecturer}, {s.room}: {s.state}]'


class CampusOnlineEntry(models.Model):
    incoming = models.ForeignKey(
        'Entry',
        models.CASCADE,
        related_name='+'
    )
    outgoing = models.ForeignKey(
        'Entry',
        models.CASCADE,
        null=True,
        blank=True,
        related_name='+'
    )
    assigned = models.DateTimeField(
        null=True,
        blank=True
    )
    ended = models.DateTimeField(
        null=True,
        blank=True
    )
    holding = models.ForeignKey(
        'CampusOnlineHolding',
        models.CASCADE,
        null=True,
        blank=True
    )
    state = FSMField(
        default='created'
    )

    class Meta:
        ordering = (
            'incoming__created',
            'assigned',
            'ended',
        )
        permissions = (
            ('view_campusonlineentry', _('View CAMPUSonline Entry')),
        )

    def __str__(s):
        return f'{s.incoming}: {s.state}'

    @transition(field=state, source='created', target='canceled')
    def cancel(self, entry=None):
        logger.debug(f'Canceling {self}')
        self.ended = timezone.now()
        self.outgoing = entry

    @transition(field=state, source='created', target='assigned')
    def assign(self, holding):
        logger.debug(f'Assigning {self} to {holding}')
        self.holding = holding
        self.assigned = timezone.now()

    @transition(field=state, source=('assigned', 'left'), target='canceled')
    def pullout(self):
        logger.debug(f'Pulling {self} out')
        self.assigned = None
        self.ended = timezone.now()

    @transition(field=state, source='assigned', target='left')
    def leave(self, entry=None):
        logger.debug(f'{self} leaving')
        self.ended = timezone.now()
        self.outgoing = entry

    @transition(field=state, source=('assigned', 'left'), target='complete')
    def complete(self, entry=None):
        from django.db import connection
        logger.debug(f'{self} completing')
        query = '''
        INSERT INTO campusonline.stud_lv_anw (
            buchung_nr,
            stud_nr,
            grp_nr,
            termin_nr,
            anm_begin,
            anm_ende
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            );
        '''
        self.ended = timezone.now()
        if entry:
            self.outgoing = entry
        data = [
            self.id,
            self.incoming.student.id,
            self.holding.course_group_term.coursegroup.id,
            self.holding.course_group_term.term,
            self.assigned,
            self.ended,
        ]
        logger.debug(f'{self} writing to CAMPUSonline')
        with connection.cursor() as cursor:
            cursor.execute(query, data)
        # TODO: Find out if next planed holding has same student in it
        if False:
            CampusOnlineEntry.objects.create()


class Statistics(models.Model):
    name = models.CharField(max_length=256)
    active = DateTimeRangeField(
        null=True,
        blank=True
    )
    terminals = models.ManyToManyField(
        'Terminal'
    )

    class Meta:
        ordering = (
            'id',
        )
        permissions = (
            ('view_statistics', _('View Statistics')),
        )

    def __str__(s):
        return f'{s.name} ({s.terminals.count()} Terminals / {s.active})'


class StatisticsEntry(models.Model):
    statistics = models.ForeignKey(
        'Statistics',
        models.CASCADE,
        related_name='entries'
    )
    incoming = models.ForeignKey(
        'Entry',
        models.CASCADE,
        related_name='+'
    )
    outgoing = models.ForeignKey(
        'Entry',
        models.CASCADE,
        null=True,
        blank=True,
        related_name='+'
    )
    state = FSMField(
        default='created'
    )

    class Meta:
        unique_together = (
            ('statistics', 'incoming'),
        )
        ordering = (
            'incoming__created',
        )
        get_latest_by = 'incoming__created'

    @transition(field=state, source='created', target='completed')
    def complete(self, entry=None):
        self.outgoing = entry

    def __str__(s):
        return f'{s.statistics}: {s.incoming}/{s.outgoing}'
