# Project Notes

This is a curated summary of the Delta Robot Notion notes, organized around the EE413 tutorial presentation. Facts that were unresolved in those notes are labelled accordingly. The original notes include historical values and setup reports; this document does not treat them as current verification.

## Robot and iRC setup

- Robot: igus DLE-DR-0050.
- iRC / Robot Control version recorded: V902-15-000, configuration V15-000-2.
- The setup described in the notes uses a Windows laptop connected to the robot controller over Ethernet.
- The controller address and CRI port found in the example programs are historical settings. Verify the live settings before attempting a connection.
- The physical CRI connection was not confirmed in the project status notes.

## Safety and operating state

- Follow the lab's approved robot operating procedure and work with an authorized supervisor or technician.
- Confirm the emergency-stop and stop procedures, robot state, active tool and TCP, coordinate frame, target positions, and speed settings before any physical test.
- Keep people and loose objects outside the robot's work envelope. Never bypass safety interlocks or open an energized cabinet.
- A successful connection or enabled state is not proof that a motion target or tool setup is safe.

## Vacuum tool

- The end effector recorded in the notes is a Schmalz CobotPump Mini ECBPMi, 24 V DC, part number 10.03.01.00556.
- The notes report a vacuum activation noise, an E03 calibration error, and an H1/SP1 suction threshold message. The root causes were not confirmed.
- Project output mapping: DOut22 is blow-off and DOut23 is suction. Verify the controller's I/O configuration before physically switching outputs.
- The 24 V supply, configured control mode, and physical cabinet wiring require verification by an authorized technician.
- No successful physical workpiece grip is confirmed in the notes.

## iRC programs and motion examples

- `programs/irc/demoprog_pick_place.xml` is the attached XML example from the project notes.
- `CobotPump.xml` is a custom iRC tool configuration built for the Schmalz CobotPump Mini ECBPMi end effector. The included demo-program XML header refers to `CobotPumpSimTest.xml`; confirm the exact configuration loaded by iRC before running the program. The custom tool configuration file is not included in this repository.
- The XML and Python motion examples contain targets and output sequences that have not been validated for the current physical setup. Do not infer safety from the example values.
- Some historical XML snippets are documented in the Notion notes but were not available as separate attached program files, so they are not recreated here as runnable files.

## Worktable frame and vision

- The notes describe fixed-slot pick-and-place as the simpler approach for a short demonstration, provided the worktable frame and target coordinates are measured and validated.
- The worktable frame, slot coordinates, and TCP/tool offset were not confirmed as calibrated.
- Intel RealSense D415 camera localization is a proposed future option. Camera calibration and the camera-to-robot transform are not documented as complete.

## Python and CRI

- The notes record Python 3.13.17 and `cri_lib` 0.4.0 installed on the original Windows laptop.
- The repository includes a read-only status diagnostic, network diagnostic, and two scripts that inspect the CRI library API. These are supporting tools; they do not establish that a live physical connection has been tested.
- The original laptop paths and personal account identifiers from the setup history are intentionally not copied into this document.

## Reference material

- [CRI Python library](https://github.com/CommonplaceRobotics/CRI-Python-Lib)
- [CRI Ethernet Interface documentation](https://wiki.cpr-robots.com/index.php/CRI_Ethernet_Interface)
- [igus robot control software](https://www.igus.eu/automation/robot-control-system/robot-software)
- [Schmalz ECBPMi product page](https://www.schmalz.com/en/products/automation-743270/vacuum-generators-307617/electric-vacuum-generators-738973/electric-vacuum-generators-end-of-arm-739374/vacuum-generators-ecbpmi-308305/10.03.01.00556)

