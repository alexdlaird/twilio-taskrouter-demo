import json
import logging

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'

logger = logging.getLogger(__name__)


def cleanup_json(add_ons):
    try:
        return json.dumps(json.loads(add_ons.strip('"')))
    except ValueError:
        return add_ons
