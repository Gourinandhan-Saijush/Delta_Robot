# Python Programs and CRI Connection

This folder contains Python examples for the igus Delta robot. The programs use the `cri_lib` package to communicate with the robot control over the CRI Ethernet interface.

## Install the CRI Python library

The library is maintained in the official [CommonplaceRobotics/CRI-Python-Lib repository](https://github.com/CommonplaceRobotics/CRI-Python-Lib). Its installation instructions are to install the package from the top-level library source folder. The following PowerShell steps create a virtual environment for this project and install the library into it.

Run these commands from the root of the `Delta_Robot` repository:

```powershell
py --version
py -m venv .venv

# Clone the CRI library outside this project so it does not become part of this repository.
$criLibSource = Join-Path $env:TEMP "CRI-Python-Lib"
git clone https://github.com/CommonplaceRobotics/CRI-Python-Lib.git $criLibSource

.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install $criLibSource
.\.venv\Scripts\python.exe -c "from cri_lib import CRIController; print('cri_lib import OK')"
```

If the temporary `CRI-Python-Lib` folder already exists, choose a different folder name for `$criLibSource`. The original project notes recorded Python 3.13.17 and `cri_lib` 0.4.0 on the setup laptop; those are historical details, not a guarantee that the same versions are installed or required now.

## Robot address and port

The example scripts use the standard embedded-controller endpoint documented by the CRI project. The live controller settings at the university lab may differ, so confirm them with the lab supervisor or in the controller configuration before connecting.

| Connection target | IP address | TCP port | Notes |
| --- | --- | ---: | --- |
| Embedded robot controller | `192.168.3.11` | `3920` | Standard defaults; used by the examples in this repository. |
| iRC/CPRog simulation on the same computer | `127.0.0.1` | Usually `3921` (may use `3921`–`3931`) | Check the simulation log or CRI interface settings for its active port. |

For an embedded controller, the computer running the Python script needs an Ethernet connection on the robot controller's network. The CRI documentation gives `192.168.3.1` as an example computer address for the standard controller subnet. Use only the address and network setup approved for the lab; do not change college network settings based on this example.

## Connection-only example

This sample opens a CRI connection and closes it. It does not acquire control, enable the drives, move the robot, or switch outputs.

```python
from cri_lib import CRIController

ROBOT_IP = "192.168.3.11"
CRI_PORT = 3920

controller = CRIController()
try:
    connected = controller.connect(ROBOT_IP, CRI_PORT)
    if not connected:
        raise ConnectionError(f"Could not connect to {ROBOT_IP}:{CRI_PORT}")

    print(f"Connected to the robot control at {ROBOT_IP}:{CRI_PORT}")
finally:
    controller.close()
```

The CRI library manages the connection and keep-alive handling. A successful connection only confirms communication with the controller; it does not confirm that the robot, tool, or any motion target is safe.

## Check the connection

From the repository root, the read-only status diagnostic can connect and print the latest robot state without commanding motion or digital outputs:

```powershell
.\.venv\Scripts\python.exe diagnostics\cri_status_test.py
```

The network diagnostic is also available at `diagnostics/network_check.bat`. Both diagnostics use the repository's example IP and port, so update those values only after confirming the live lab settings.

## End-effector output channels

The project mapping is:

- **DOut22:** blow-off
- **DOut23:** suction

The Python pick-and-place example and iRC XML labels use this mapping. Check the controller's I/O configuration and follow the lab procedure before physically switching either output.

## Before running a motion example

`demoprog_pick_place.py`, `mouse_program.py`, and `shape_program.py` can command physical robot motion; the pick-and-place program also switches end-effector outputs. Do not run them as a connection test. Follow the lab's approved robot procedure and have an authorized supervisor verify the emergency stop, operating mode, active tool and TCP, I/O mapping, coordinate frame, work area, targets, and speed settings before any physical run.

## Official references

- [CRI Python library installation and usage](https://github.com/CommonplaceRobotics/CRI-Python-Lib)
- [CRI Ethernet Interface](https://wiki.cpr-robots.com/index.php/CRI_Ethernet_Interface)
- [CRI Client Structure, standard IP and port](https://wiki.cpr-robots.com/index.php/CRI_Client_Structure)
- [Project setup and safety notes](../../docs/project-notes.md)
