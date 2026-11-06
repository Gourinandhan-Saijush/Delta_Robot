# Delta Robot

Project materials for the Maynooth University EE413 robotics lab tutorial on the igus Delta robot. The repository brings together the presentation, Python demonstrations, an iRC XML program, connection diagnostics, and a summary of the project notes.

## Project at a glance

- Robot: igus DLE-DR-0050 Delta robot
- Control software noted in the project materials: iRC V902-15-000 / configuration V15-000-2
- End effector: Schmalz CobotPump Mini ECBPMi vacuum generator
- Python interface: CRI Ethernet interface with `cri_lib`

The presentation is the main overview of the robot mechanics, control cabinet, iRC workflow, safety controls, coordinate frames, and programming options. See[`docs/project-notes.md`](docs/project-notes.md).

## Repository contents

| Path | Contents |
| --- | --- |
| `programs/python/` | Pick-and-place, mouse jog, and shape-motion examples |
| `programs/irc/` | iRC pick-and-place XML example |
| `diagnostics/` | Network and CRI status/API inspection tools |
| `docs/project-notes.md` | Curated setup, safety, vacuum, coordinate-frame, and CRI notes |

## Python setup

The project notes record Python 3.13.17 and `cri_lib` 0.4.0 on the original Windows laptop. The CRI library is maintained separately at [CommonplaceRobotics/CRI-Python-Lib](https://github.com/CommonplaceRobotics/CRI-Python-Lib). Confirm the library and controller versions that are supported by the lab setup before installing or connecting.

The diagnostics and motion programs contain controller connection settings from earlier setup notes. Treat these as historical values and verify the live controller address and CRI port with the lab supervisor before use.

## Safety and validation status

Some Python programs and the iRC XML file can send robot motion or digital-output commands. The mouse-control file displays a preview-only message while its physical-motion setting is enabled; the shape program also has dry-run mode disabled. The code is included as supplied and has not been changed or tested as part of this repository setup.

The project notes do not confirm a successful physical CRI connection or a successful workpiece grip. The active tool file, TCP offset, physical suction/blow-off wiring, worktable frame, and safe motion targets are not fully verified. Do not run motion or output commands until an authorized lab technician has checked the robot state, tool and TCP, I/O mapping, targets, workspace, and lab-approved safeguards.

## Credit

Maynooth University · EE413 Tutorial · MSc Robotics and Embedded AI

