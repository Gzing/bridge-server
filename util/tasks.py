import os

from celery import Celery
from celery.utils.log import get_task_logger

from config import settings
from flask import Flask
from database import db
from database import db_models
from .contract import ContractHelper
from logic.indexer_service import event_reducer

logger = get_task_logger(__name__)


class CeleryConfig(object):
    SQLALCHEMY_DATABASE_URI = settings.DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


def make_celery(app):
    celery = Celery(app.import_name,
                    backend=settings.REDIS_URL,
                    broker=settings.REDIS_URL,
                    task_always_eager=settings.CELERY_DEBUG)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

flask_app = Flask(__name__)

flask_app.config.from_object(__name__ + '.CeleryConfig')

db.init_app(flask_app)
celery = make_celery(flask_app)


@celery.task
def event_listner():
    event_tracker = db_models.EventTracker.query.first()
    if not event_tracker:
        event_tracker = db_models.EventTracker(last_read=0)
        db.session.add(event_tracker)
        db.session.commit()
    ContractHelper().fetch_events(['NewListing(uint256)'],
                                  block_from=event_tracker.last_read,
                                  block_to='latest',
                                  f=event_reducer)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # run every 2 minutes for now
    sender.add_periodic_task(20.0, event_listner)