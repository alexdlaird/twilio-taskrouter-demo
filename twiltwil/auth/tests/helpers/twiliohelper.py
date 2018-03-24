from twilio.rest.taskrouter.v1.workspace.worker import WorkerInstance

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'


def get_worker_instance():
    payload = {
        'account_sid': 'account_sid',
        'activity_name': 'activity_name',
        'activity_sid': 'activity_sid',
        'attributes': 'attributes',
        'available': 'available',
        'date_created': 'date_created',
        'date_status_changed': 'date_status_changed',
        'date_updated': 'date_updated',
        'friendly_name': 'friendly_name',
        'sid': 'sid',
        'workspace_sid': 'workspace_sid',
        'url': 'url',
        'links': 'links',
    }

    return WorkerInstance('v1', payload, payload['workspace_sid'], 'worker_sid')
