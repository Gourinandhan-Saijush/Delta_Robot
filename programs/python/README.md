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

If the temporary `CRI-Python-Lib` folder already exists, choose a different folder name for `$criLibSource`. The Windows setup notes from 22 October 2026 record Python 3.13.17, pip 26.2.2, and `cri_lib` 0.4.0; the install and import checks succeeded, but the notes say a physical CRI connection was not confirmed. Treat these as historical setup results, not a guarantee about current versions or robot connectivity.

## Robot address and port

The example scripts use the standard embedded-controller endpoint documented by the CRI project. The live controller settings at the university lab may differ, so confirm them with the lab supervisor or in the controller configuration before connecting.

| Connection target | IP address | TCP port | Notes |
| --- | --- | ---: | --- |
| Embedded robot controller | `192.168.3.11` | `3920` | Standard defaults; used by the examples in this repository. |
| iRC/CPRog simulation on the same computer | `127.0.0.1` | Usually `3921` (may use `3921`–`3931`) | Check the simulation log or CRI interface settings for its active port. |

For an embedded controller, the computer running the Python script needs an Ethernet connection on the robot controller's network. The CRI documentation gives `192.168.3.1` as an example computer address for the standard controller subnet. Use only the address and network setup approved for the lab; do not change college network settings based on this example.

The Windows diagnostics notes record `192.168.3.20` with subnet mask `255.255.255.0` as a previously used laptop Ethernet configuration. This is a historical example, not a confirmed current laptop or lab setting. Check the active adapter with `ipconfig` and use only the values approved for the robot network.

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

## Check the network and CRI connection

The notes do not confirm a successful connection to the physical controller. Check the network before attempting the read-only CRI diagnostic:

1. From the repository root, run `ipconfig` and identify the Ethernet adapter connected to the robot network. Compare its address and subnet with the lab-approved settings.
2. Run `diagnostics\network_check.bat`. It pings the example controller address and checks TCP port `3920` with `Test-NetConnection`.
3. A failed ping by itself does not prove the controller is unreachable because ICMP may be blocked. Check the `TcpTestSucceeded` result for the TCP port check. A successful TCP check confirms that the port accepts a network connection; it does not confirm safe robot operation or authorize motion.
4. If the TCP check succeeds and the lab procedure allows it, run the read-only status diagnostic and retain its terminal output:

```powershell
.\.venv\Scripts\python.exe diagnostics\cri_status_test.py
```

The batch file and status diagnostic use the repository's example controller IP and port. Change them only after confirming the live lab settings. If TCP fails, check the selected Ethernet adapter, cable/link, approved subnet configuration, controller address, and CRI port with the supervisor before retrying.

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
