import logging
import subprocess
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

from celery.task import (
    PeriodicTask,
    Task,
)

from .models import (
    Holding,
    Terminal,
)

logger = logging.getLogger(__name__)


class HoldingCleanUpTask(PeriodicTask):
    run_every = timedelta(minutes=5)

    def run(self, **kwargs):
        # TODO: Fix filter to find holding that have recently ended
        for h in Holding.objects.filter(state='running', campusonline__blafoobar=True):
            h.end()
            h.save()


class TerminalOnlineTask(PeriodicTask):
    run_every = timedelta(minutes=5)

    def run(self, **kwargs):

        def check(terminal):
            logger.debug('Pinging {}.'.format(recorder))
            proc = subprocess.run(
                [
                    'ping',
                    '-c1',
                    '-w2',
                    terminal.hostname
                ]
            )
            online = (proc.returncode == 0)
            if terminal.online != online:
                terminal.online = online
                logger.debug('Terminal {} online: {}'.format(terminal, online))
                terminal.save()

        terminals = Terminal.objects.filter(enabled=True)
        logger.info('Pinging {} terminals.'.format(terminals.count()))

        with ThreadPoolExecutor() as executor:
            executor.map(check, terminals)
