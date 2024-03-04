__copyright__ = "Copyright (c) 2018 Alex Laird"
__license__ = "MIT"

import json
import logging

logger = logging.getLogger(__name__)


def cleanup_json(add_ons):
    try:
        return json.dumps(json.loads(add_ons.strip('"')))
    except ValueError:
        return add_ons
