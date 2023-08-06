# Durin control system

This repository contains Python code that interfaces with the robot Durin, built by the [Neurocomputing Systems group](https://neurocomputing.systems) at the [KTH Royal Instititute of Technology](https://kth.se).
Please note that this is only the reference implementation for our interface. See below.

## Installation

We require a working Python installation with access to [pip](https://pypi.org/project/pip/).
After that, installation is straight-forward:

```bash
pip install durin
```

## Usage

The interface is meant to be used via Python. More examples can be found in the [`durin/examples`](https://github.com/ncskth/durin/tree/main/durin/examples) folder.


```python
from durin import *

# The ip address to Durin is 172.16.223.9X, where X is the number of the robot (1, 2, or 5).
durin_ip = "172.16.223.91"

# This connects to durin and displays a user interface (UI)
with DurinUI(durin_ip) as durin:

    while True:
        # Get observation
        (obs, dvs, cmd) = durin.read()

        # Do clever things...

        # Move durin 100 units left with 0 forward/backward motion and 0 rotation
        command = Move(100, 0, 0)

        # Send a command to Durin
        durin(command)

        # ... this loop continues forever!
        # You can exit it on your computer by pressing CTRL+C
```

## Sensory data

The `durin.read()` method will give you access to 

1. An `Observation` from the robot sensors object containing
    * `.tof` Time of Flight sensors
    * `.charge` Battery charge
2. A 640x480 DVS [PyTorch](pytorch.org) tensor
    * This tensor has buffered/stacked events since the last `.read()` command.
    * Note that this is **only** available if the Durin has a DVS sensor installed
3. Replies from the robot, following any `Poll` commands
    * This is specified in the protocol datasheet below - feel free to ignore

## Commands
The most important command is `Move(x, y, rotation)`. the `x`, `y`, `rotation` values should be in the interval between [-500, 500].

## Custom implementation
You can interface to the microcontroller (sensor + wheel actuation) and DVS microcamera with TCP and UDP.
A complete specification is available via Google Drive: https://docs.google.com/spreadsheets/d/11jD30J00-03ygZ6zJaVTnjJRQKfczT-wMIdBdpYMxD4/edit?usp=sharing

Each robot has two IP addresses - one for the microcontroller and one for the DVS controller.
The robots are numbered 1, 2, or 5. Insert those numbers where `X` is written below:

* `172.16.223.9X`: Microcontroller for sensory data and motor commands
* `172.16.223.10x`: Raspberry Pi for streaming DVS data

## Contact

Reach out to Juan or Jens if you need anything.
