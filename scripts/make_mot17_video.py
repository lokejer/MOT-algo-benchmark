"""Convert a MOTChallenge sequence (img1/ frames) into the MP4 used by experiment.py."""

# this script is AI-generated.

import argparse
import configparser
from pathlib import Path

import cv2

DEFAULT_OUTPUT = Path("evaluation/stationary_webcam_eval.mp4")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sequence_dir", type=Path, help="e.g. MOT17/train/MOT17-09-FRCNN")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--overwrite", action="store_true", help="replace an existing output file")
    args = parser.parse_args()

    # seqinfo.ini ships with every motchallenge sequence and holds the true fps and frame size
    # reading it avoids hardcoding 30 fps or 1920x1080 for sequences that differ
    seqinfo = configparser.ConfigParser()
    if not seqinfo.read(args.sequence_dir / "seqinfo.ini"):
        raise FileNotFoundError(f"seqinfo.ini not found in {args.sequence_dir}")
    info = seqinfo["Sequence"]
    fps = float(info["frameRate"])
    size = (int(info["imWidth"]), int(info["imHeight"]))
    expected_frames = int(info["seqLength"])

    # frames are named 000001.jpg, 000002.jpg, ... so a plain sort keeps them in order
    frames = sorted((args.sequence_dir / "img1").glob("*.jpg"))
    if len(frames) != expected_frames:
        raise ValueError(f"Found {len(frames)} frames in img1/, seqinfo.ini expects {expected_frames}")

    if args.output.exists() and not args.overwrite:
        raise FileExistsError(f"{args.output} already exists, pass --overwrite to replace it")
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # mp4v matches the encoding the paper's results were produced from
    # mp4v is lossy, so a different codec gives slightly different pixels and slightly different scores
    writer = cv2.VideoWriter(str(args.output), cv2.VideoWriter_fourcc(*"mp4v"), fps, size)
    if not writer.isOpened():
        raise RuntimeError(f"Could not open video writer for {args.output}")

    try:
        for path in frames:
            frame = cv2.imread(str(path))
            if frame is None or (frame.shape[1], frame.shape[0]) != size:
                raise ValueError(f"Unreadable or wrongly sized frame: {path}")
            writer.write(frame)
    finally:
        writer.release()

    print(f"Wrote {len(frames)} frames at {fps:g} FPS ({size[0]}x{size[1]}) to {args.output}")


if __name__ == "__main__":
    main()
