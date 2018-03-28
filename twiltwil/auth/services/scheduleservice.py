import logging
import threading
import time

from django.contrib.auth import get_user_model
from django.core.cache import cache
from schedule import Scheduler as SchedulerBase

from twiltwil.auth.services import authservice, twilioauthservice

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class Scheduler(SchedulerBase):
    def __init__(self):
        super().__init__()

    def run_continuously(self, interval=1):
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    self.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.setDaemon(True)
        continuous_thread.start()
        return cease_continuous_run


def delete_inactive_users():
    logger.info('Deleting inactive users task ...')

    for user in get_user_model().objects.filter(is_superuser=False).iterator():
        token = cache.get('tokens:{}'.format(user.worker_sid))
        if not token:
            logger.info('Deleting user with expired token: {}'.format(user.username))

            authservice.delete_user(user)

    logger.info('... done deleting inactive users task')


def delete_orphaned_workers():
    logger.info('Deleting orphaned Workers ...')

    for worker in twilioauthservice.get_workers():
        if not get_user_model().objects.filter(worker_sid=worker.sid).exists():
            logger.info('Deleting a orphaned Worker with no database entry: {}'.format(worker.sid))

            twilioauthservice.delete_worker(worker.sid)

    logger.info('Done deleting orphaned Workers task ...')


scheduler = Scheduler()
scheduler.every(5).minutes.do(delete_inactive_users)
scheduler.every().hour.do(delete_orphaned_workers)
scheduler.run_continuously()
