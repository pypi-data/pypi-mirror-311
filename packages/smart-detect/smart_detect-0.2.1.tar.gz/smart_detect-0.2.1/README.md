# Smart Detect: Pose and Movement Analysis

`smart_detect` is a Python package that uses OpenCV and Mediapipe to detect poses, analyze joint angles, and monitor irregular movements. It can be used for applications like posture correction, exercise tracking, and more.

---

## Features
- Detects body poses in real time using Mediapipe.
- Calculates joint angles (e.g., knees) for movement analysis.
- Alerts users about irregular movements based on thresholds.

---

## Installation

Install the package using pip:

```bash pip install smart_detect ```

## Usage
Here's a quick example to start tracking movement:

from smart_detect import start_tracking

start_tracking()

### Parameters for start_tracking
irregular_threshold (int, default=15): Number of consecutive frames of irregular movement required to trigger an alert.
normal_threshold (int, default=15): Number of consecutive frames of normal movement required to reset the alert.

## Dependencies
OpenCV
Mediapipe
NumPy

These are automatically installed when you install the package.

## Contributing
Feel free to contribute to the project by submitting pull requests or reporting issues on GitHub.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
