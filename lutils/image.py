from pathlib import Path

import cv2
from PIL import Image


def get_frame(
    video_pth: str | Path,
    frame_idx: int | None = None,
    timestamp_sec: float | None = None,
):
    if not isinstance(video_pth, str):
        video_pth = str(video_pth)

    if frame_idx is None and timestamp_sec is None:
        raise ValueError("Either frame_idx or timestamp_sec must be provided")

    # If frame_idx is float, treat it as timestamp_sec
    if isinstance(frame_idx, float):
        timestamp_sec = frame_idx
        frame_idx = None

    cap = cv2.VideoCapture(video_pth)

    if timestamp_sec is not None:
        # Convert timestamp to frame index
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_idx = int(timestamp_sec * fps)

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx - 1)
    ret, frame = cap.read()
    if not ret:
        return False
    cap.release()

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame_rgb).convert("RGB")

    return image


def center_crop(image):
    width, height = image.size  # Get dimensions
    new_l = min(width, height)

    left = (width - new_l) / 2
    top = (height - new_l) / 2
    right = (width + new_l) / 2
    bottom = (height + new_l) / 2

    # Crop the center of the image
    image = image.crop((left, top, right, bottom))

    return image
