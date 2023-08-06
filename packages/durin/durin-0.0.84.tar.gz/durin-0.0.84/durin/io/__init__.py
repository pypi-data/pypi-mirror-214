import logging
from pathlib import Path
from typing import List

import capnp

PORT_TCP = 1337
PORT_UDP = 2300

SENSORS = {
    "tof_a": 128,
    "tof_b": 129,
    "tof_c": 130,
    "tof_d": 131,
    "misc": 132,
    "uwb": 133,
}

schema = capnp.load(str((Path(__file__).parent / "schema.capnp").absolute()))

def decode(buffer) -> List[schema.DurinBase]:
    # TODO: Use packed version later
    try:
        msg = schema.DurinBase.from_bytes_packed(buffer)
        return msg
    except ValueError as e:
        logging.warn("Error in decoded message", e)
    except capnp.lib.capnp.KjException as e:
        logging.warn("Failed to deserialize", e)
        return None
