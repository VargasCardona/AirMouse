
# AirMouse

Computer vision application that enables natural interaction with digital interfaces using hand movements and gestures. It leverages Mediapipe's trained models to accurately detect, track, and interpret hand poses and gestures in real-time from a connected camera feed. 


## Features

- Real-time Hand Detection and Tracking
- Basic gestures for natural interaction
- Finger Tracking and Recognition

## Demo

![2024-03-17 17-32-13 (online-video-cutter com)](https://github.com/VargasCardona/AirMouse/assets/142677238/74ccd6bb-ecaa-4f36-94c1-feee7d28e042)

## Optimizations

- Use of optimized computer vision algorithms and libraries (e.g., OpenCV, Mediapipe, TensorFlow) for efficient hand detection, tracking, and pose estimation.
- Separation of the computer vision pipeline (hand detection, tracking, and pose estimation) from the cursor movement or interaction logic.
- Region of interest (ROI) around the hand, rather than processing the entire camera frame.


## Tech Stack

**Languages:** Python3

**Libraries:** OpenCv, Mediapipe, Pyautogui, Numpy


## License

[GPL-3.0](https://www.gnu.org/licenses/)

