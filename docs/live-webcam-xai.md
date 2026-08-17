# Earlier Prototype: Live YOLOv8 Tracking with Eigen-CAM

This repository began as a live webcam application for object detection, persistent tracking, and a toggleable Eigen-CAM feature-activation overlay. The later five-tracker study documented in the [main README](../README.md) grew from this prototype.

![YOLOv8 live detection demo](https://github.com/user-attachments/assets/6258e14b-26c0-4571-9f5f-ba741175817b)

## Capabilities

- Live YOLOv8 detection and persistent multi-object tracking
- Adjustable brightness and confidence controls
- Confidence hysteresis to reduce box flicker
- Temporal label voting to stabilize class names
- Stale-track cleanup for long-running sessions
- Smoothed end-to-end FPS reporting
- Toggleable, class-agnostic Eigen-CAM overlay

## Running the live application

The camera workflow was tested with Python 3.13 on Windows. It uses DirectShow by default; change `CAMERA_BACKEND` in [`config.py`](../config.py) for another operating system.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python camera.py
```

Press **Q** to quit and **E** to toggle the Eigen-CAM overlay. The OpenCV window also exposes live brightness and detection-confidence sliders.

## Processing flow

1. [`camera.py`](../camera.py) captures and mirrors each frame, applies brightness adjustment and Gaussian blur, and coordinates inference and display.
2. [`detector.py`](../detector.py) performs persistent YOLO tracking, confidence hysteresis, temporal label voting, and stale-state cleanup.
3. [`explain.py`](../explain.py) captures an intermediate activation from the existing inference pass and estimates its dominant Eigen-CAM component.
4. [`display.py`](../display.py) blends the heatmap beneath the detection boxes and settings HUD.

## Eigen-CAM implementation

The explainer attaches a forward hook only while the overlay is enabled. It reuses the detector's activation rather than performing a second inference pass, then estimates the first principal component with warm-started power iteration. Because a principal component has an arbitrary sign, the positive and negative orientations are compared against the detected boxes and the orientation that emphasizes the objects is displayed.

The feature map is projected back through the detector's letterbox geometry before being resized to the webcam frame. This keeps the overlay aligned with the input seen by YOLO.

## Limitations

- The heatmap is scene-wide and class-agnostic; it is not a causal explanation for an individual detection.
- Detection-guided sign selection makes the visualization easier to interpret but also means the displayed orientation depends on the detected boxes.
- Webcam capture and inference share one loop, so a slow model reduces the effective capture rate.
- Camera exposure and gain are not controlled directly; Gaussian blur is only a software-side noise reduction measure.
- The live application was an exploratory prototype and is not evaluated by the MOT benchmark.

The implementation history and design rationale are preserved in [`improvements.md`](improvements.md).
