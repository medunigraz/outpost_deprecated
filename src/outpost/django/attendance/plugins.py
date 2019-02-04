import logging

import pluggy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..base.plugins import Plugin

logger = logging.getLogger(__name__)


class TerminalBehaviourPlugin(Plugin):
    pass


class TerminalBehaviour(object):

    name = f'{__name__}.TerminalBehaviour'
    base = TerminalBehaviourPlugin
    hookspec = pluggy.HookspecMarker(name)
    hookimpl = pluggy.HookimplMarker(name)

    @classmethod
    def manager(cls, condition=lambda _: True):
        pm = pluggy.PluginManager(cls.name)
        pm.add_hookspecs(cls)
        for plugin in cls.base.all():
            if condition(plugin):
                pm.register(plugin())
        return pm

    @hookspec
    def create(self, entry):
        '''
        '''

    @hookspec
    def update(self, entry):
        '''
        '''


class DebugTerminalBehaviour(TerminalBehaviourPlugin):

    name = _('Debugger')

    @TerminalBehaviour.hookimpl
    def create(self, entry):
        logger.debug(f'{self.__class__.__name__}: create({entry})')

    @TerminalBehaviour.hookimpl
    def update(self, entry):
        logger.debug(f'{self.__class__.__name__}: update({entry})')


class CampusOnlineTerminalBehaviour(TerminalBehaviourPlugin):

    name = _('CAMPUSonline')

    @TerminalBehaviour.hookimpl
    def create(self, entry):
        from .models import CampusOnlineHolding, CampusOnlineEntry
        logger.debug(f'{self.__class__.__name__}: create({entry})')
        try:
            holding = CampusOnlineHolding.objects.get(
                room=entry.terminal.room,
                initiated__gte=timezone.now(),
                state__in=('running', 'finished')
            )
        except CampusOnlineHolding.DoesNotExist:
            holding = None
        coe, created = CampusOnlineEntry.objects.get_or_create(
                incoming__student=entry.student,
                incoming__terminal__room=entry.terminal.room,
                holding=holding,
                ended__isnull=True,
                defaults={'created': entry}
        )
        if created:
            # New entry, student should have entered room by now
            return _('Welcome')
        if not holding:
            # No holding but prior entry found, assume he/she left the room
            # with this entry
            coe.cancel(entry)
        else:
            if holding.state == 'running':
                if coe.state == 'assigned':
                    coe.leave(entry)
                if coe.state == 'created':
                    coe.assign(holding)
            if holding.state == 'finished':
                if coe.state == 'assigned':
                    coe.complete(entry)
        coe.save()
        return _('Goodbye')


class StatisticsTerminalBehaviour(TerminalBehaviourPlugin):

    name = _('Statistics')

    @TerminalBehaviour.hookimpl
    def create(self, entry):
        from .models import StatisticsEntry
        logger.debug(f'{self.__class__.__name__}: create({entry})')
        for s in entry.terminal.statistics_set.all():
            try:
                se = StatisticsEntry.objects.filter(
                    statistics=s,
                    incoming__student=entry.student,
                    outgoing=None,
                    state='created'
                ).latest()
                se.complete(entry)
                se.save()

                msg = _('Welcome')
            except StatisticsEntry.DoesNotExist:
                se = StatisticsEntry.objects.create(
                    statistics=s,
                    incoming=entry
                )
                msg = _('Goodbye')
            return msg
