# UR5e Robotic Image-Acquisition Workflow

This repository contains the Python code used to control the UR5e robotic arm and the Robotiq gripper for automated image acquisition.

The workflow was used for robotic sample handling, vial transfer, laser activation, lid control, and scheduled image capture.

## Overview

The system controls a UR5e robotic arm through socket communication and URScript. The Robotiq gripper is used for rack and vial handling. The workflow also controls external hardware, including the imaging enclosure lid and the laser, through digital outputs.

The code was used for the thesis-specific robotic image-acquisition workflow.

### Features

* Socket-based control of the UR5e robotic arm.
* Robotiq gripper control for rack and vial handling.
* Rack-based sample processing.
* Optional vortexing before imaging.
* Laser and lid control using digital outputs.
* Camera triggering and timestamped image saving.
* Scheduled image acquisition using CSV files.

## Main Workflow

The main workflow is:

```text
→ scheduler.py
→ Execution_rack.py
→ UR_tasks_seda_camera.py
→ UR_Functions.py
→ utils.py
```

`rack/` contains the sample information for each rack.

`schedule/` contains the programmed acquisition times.

Captured images are saved to the `image/` folder. There is an image in the folder for demonstration.

## Main Scripts

### `scheduler.py`

This script runs the time-resolved workflow.

It reads a schedule CSV file from the `schedule/` folder. It checks the current time and starts the robot workflow when a scheduled time is reached.

This script is used when the robot needs to collect images at defined time points.

### `Execution_rack.py`

This is the main rack execution script.

It reads the rack CSV files from the `rack/` folder. For each vial, it reads the vial number, sample name, and whether shaking is required.

The script controls the full workflow for each sample:

* pick the rack from the shelf
* pick the vial
* vortex the vial if required
* place the vial into the imaging box
* close the lid
* turn on the laser
* capture an image
* turn off the laser
* remove the vial from the box
* return the vial to the rack
* return the rack to the shelf

### `UR_tasks_seda_camera.py`

This script contains the high-level robot tasks used in the final workflow.

It includes the calibrated robot positions for racks, vials, the imaging box, and the shelf. It also contains functions for gripper control, lid control, laser control, vortexing, vial loading, vial unloading, and image capture.

Images are saved with filenames containing the rack number, vial number, sample name, loop number, and timestamp.

### `UR_Functions.py`

This script contains the low-level UR5e control functions.

It sends commands to the robot through the socket interface. It also uses RTDE for digital output control.

This script generates URScript movement commands such as `movej(...)` and `movel(...)`. These commands are sent from Python to the UR5e controller.

### `util.py`

This script contains helper functions for robot pose calculations.

It converts between rotation vectors, rotation matrices, and roll-pitch-yaw angles. These functions are used when checking or updating the robot TCP pose.

## Supporting Folders

### `robotiq/`

This folder contains the Robotiq gripper-control code.

The main workflow uses this folder to activate the gripper and to open or close it during rack and vial handling.

### `rack/`

This folder contains rack CSV files.

Each file defines the samples in one rack. The CSV files include the vial number, sample name, and whether shaking is needed.

### `schedule/`

This folder contains schedule CSV files.

These files define which rack should be processed at each time point.

## Gripper Control

The final workflow uses the Robotiq gripper through a Python gripper-control class.

The gripper communicates with the robot over the robot IP address and the gripper socket port.

Earlier RG2 gripper code was used only as a development reference. It is not required for this final UR5e-Robotiq workflow.

## URScript Usage

The workflow is written in Python, but the robot movement commands are sent as URScript.

The main URScript commands are generated in `UR_Functions.py`.

Examples include:

```text
movej(...)
movel(...)
```

Higher-level scripts such as `Execution_rack.py`, `scheduler.py`, and `UR_tasks_seda_camera.py` call these lower-level functions.

## Getting Started

### Prerequisites

* UR5e robotic arm
* Robotiq gripper
* Camera connected to the robot-control computer
* Laser and lid connected to robot digital outputs
* Python 3.x

### Python Packages

The main Python packages are:

```text
numpy
pandas
opencv-python
ur-rtde
```

The Robotiq gripper-control files are included in the `robotiq/` folder.

## Usage

### Run one rack workflow

Example:

```bash
python3 Execution_rack.py --rack_number 1 --loops 1
```

Multiple racks can also be processed:

```bash
python3 Execution_rack.py --rack_number 1 --rack_number 2 --loops 1
```

### Run the scheduled workflow

Example:

```bash
python3 scheduler.py
```

The schedule file path is defined inside `scheduler.py`.

## Rack CSV Format

Each rack CSV file should contain the sample information for one rack.

Example columns:

```text
vial
name
shake
```

Example:

```text
1,PS_sample_1,True
2,PMMA_sample_1,False
```

## Notes

The calibrated robot positions are specific to the experimental setup used in this work.

The positions may need to be recalibrated before the code is used with another UR5e robot, rack geometry, camera position, or imaging enclosure.

Generated images, trained models, and demonstration videos are not stored in this repository. These files are archived separately through the associated Zenodo record.

## Legacy Code

An earlier RG2-based socket-control implementation was used during development.

This legacy RG2 code is not included in this repository because the final workflow uses the UR5e arm with a Robotiq gripper and the `UR_tasks_seda_camera.py` / `UR_Functions.py` control structure.

## Other Files
README.md: This file, providing an overview of the project.
requirements.txt: Lists the dependencies required to run the project.

## Authors
Zhengxue Zhou (xx) and Seda Uyanik (seda.uyanik@liverpool.ac.uk)

## License
Distributed under the Unlicense License. See LICENSE.txt for more information.
