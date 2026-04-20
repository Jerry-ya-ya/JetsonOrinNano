# Nvidia Jetson Orin Nano

## 2026/01/07

- Connected project to remote Git repository.

- Added chapter: Summarize the hardware required for upgrading Jetson.

- Added chapter: Disk Partitioning.

- Implemented the creation of the table of contents.

## 2026/01/22

- Added chapter: Dual Boot Setup – Installing Ubuntu alongside Windows.

- Updated image filenames.

## 2026/01/28

- Added chapter: Upgrade jetson orin nano to maxn super.

## 2026/02/02

- Added chapter: Use ssh to connect to devices and scp to transfer data.

- Fixed an issue where images failed to display on GitHub due to incorrect capitalization in image URLs.

- Added chapter: Installing and Using jtop.

- Added chapter: Installing and Testing the Webcam.

- Added practice: Image processing with OpenCV.

## 2026/03/09

- Added simple optical flow detection.

## 2026/03/19

- Added a dangerous frame counter; danger is only triggered when it exceeds three consecutive frames.

- Added stop function with debounce; trigger on confirmed danger, allow retrigger after safe state, and display stop status.

## 2026/04/07

- Connected the Wave Rover to the Jetson Orin Nano, provided independent power to the Jetson Orin Nano, and modified main.py so that the Jetson Orin Nano can control the Wave Rover via USB.

## 2026/04/09

- Implemented a simple state machine to track the autonomous vehicle’s state, and enabled mouse input to switch the default stopped state to continuous movement or emergency stop.

## 2026/04/19

- Separated Config and Serial from the main program, and consolidated the test files into a single folder.

- Separated State controller and Motor serial from the main program.

## 2026/04/19

- Refactored mouse_listener.py so that it is only responsible for setting up mouse listening, instead of creating the controller and serial object by itself; the actual state and hardware instances should be created in main.py and then passed in.