# Multi-Object Tracking (MOT) Algorithm Benchmark

A controlled, empirical comparison of 5 MOT algorithms (ByteTrack, BoT-SORT, TrackTrack, Deep OC-SORT, FastTracker) under a fixed YOLOv8 detection pipeline.  

Paper: [PDF](paper/mot-tracker-comparison.pdf)

![Quality-speed trade-off across the five evaluated trackers](evaluation/results/figures/quality_speed_tradeoff.png)

## Key finding

**TrackTrack produced the strongest overall tracking quality and identity stability. ByteTrack offered the best balance between quality and speed for a 30 FPS laptop deployment.**  
TrackTrack reached 48.17% HOTA and 58.08% IDF1, while ByteTrack was over twice as fast at 38.81 FPS.

## Experimental setup

| Component | Configuration |
|---|---|
| Detector | YOLOv8 large |
| Dataset | MOT17-09 pedestrian sequence |
| Input | 525 frames, 1920x1080 at 30 FPS |
| Class filter | COCO person class only |
| Detection threshold | 0.10 |
| Inference size | 640 pixels |
| Hardware | NVIDIA GeForce RTX 5060 Laptop GPU |
| Evaluation | HOTA, DetA, AssA, IDF1, MOTA, ID switches, fragments, precision, recall, latency, and FPS |
| Protocol | Fresh model and tracker state per run. First five frames excluded from timing (CUDA kernel warmup) |

- Fixed: detector, input sequence, preprocessing, confidence threshold, class filter, and evaluation code (`experiment.py`)  
- Variable: tracking configuration between runs

## Trackers evaluated

- [ByteTrack](https://github.com/FoundationVision/ByteTrack) performs a second association pass using lower-confidence detections, recovering partially occluded pedestrians without an appearance model.
- [BoT-SORT](https://github.com/NirAharon/BoT-SORT) combines motion, confidence, and camera-motion compensation. Re-ID (Re-identification) was disabled in this experiment.
- [TrackTrack](https://github.com/kamkyu94/TrackTrack) uses track-perspective association and track-aware initialization to preserve established trajectories and suppress unnecessary new tracks.
- [Deep OC-SORT + ReID](https://github.com/GerardMaggiolino/Deep-OC-SORT) combines observation-centric motion correction with adaptively weighted appearance features for identity recovery after occlusion.
- [FastTracker](https://github.com/Hamidreza-Hashempoor/FastTracker) adds occlusion-aware track retention and recovery to a lightweight ByteTrack-style association pipeline.

## Results

| Tracker | HOTA (%) | IDF1 (%) | AssA (%) | ID switches | Fragments | Median latency (ms) | FPS |
|---|---:|---:|---:|---:|---:|---:|---:|
| ByteTrack | 44.48 | 50.69 | 40.70 | 43 | 61 | **25.26** | **38.81** |
| BoT-SORT | 46.36 | 54.05 | 42.70 | 45 | 57 | 53.18 | 18.76 |
| **TrackTrack** | **48.17** | **58.08** | **44.30** | **29** | **49** | 53.69 | 18.51 |
| Deep OC-SORT + ReID | 44.66 | 52.87 | 40.79 | 47 | 62 | 29.12 | 33.63 |
| FastTracker | 44.15 | 51.78 | 40.51 | 56 | 59 | 27.54 | 35.76 |

The complete result is available in [`tracker_comparison.csv`](evaluation/results/tracker_comparison.csv).  
Note: All 5 trackers were scored from their saved frame-level predictions by the same evaluation code in `experiment.py`, which follows the TrackEval formulas but omits the official MOTChallenge ignore-region handling. Thus, the scores are valid for comparing these trackers with each other, not with the public MOTChallenge leaderboard.

## Reproducing the experiment

The experiment was executed with Python 3.13. CUDA is optional, but hardware and PyTorch builds materially affect the reported latency and throughput. Install the appropriate PyTorch build for your platform before installing the remaining dependencies.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Next:
1. Download yolov8l.pt into the repo root (or let Ultralytics fetch it).
2. Download MOT17 and run python scripts/make_mot17_video.py path/to/MOT17-09-FRCNN.
3. Run python experiment.py.

The matching pedestrian ground truth is provided at `evaluation/ground_truth.txt`. Run either the script or the executed notebook:

```powershell
python experiment.py
# or
jupyter notebook experiment.ipynb
```

Both entry points regenerate frame-level prediction CSVs, annotated videos, and `evaluation/results/tracker_comparison.csv`.

## Limitations

- The study uses one short, stationary-camera MOT17-09 sequence and one laptop environment
- The local evaluator does not reproduce official MOTChallenge distractor and ignore-region handling, so these are controlled relative results rather than official leaderboard scores
- Each tracker was only timed once
- Timing includes frame capture, preprocessing, detection, tracking, and result transfer, but excludes rendering and video encoding
- Tracker behavior depends on the installed Ultralytics implementations and their configuration defaults

## Citation

```bibtex
@misc{loke2026mot,
  author = {Jerome Loke},
  title = {Comparing Multi-Object Tracking Algorithms for Stable Real-Time YOLOv8 Tracking},
  year = {2026},
  url = {https://github.com/lokejer/MOT-algo-benchmark},
  note = {Technical report and reproducible implementation}
}
```
