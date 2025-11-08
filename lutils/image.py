from pathlib import Path
from typing import Union

import cv2
from PIL import Image


def get_frame(
    video_pth: Union[str, Path],
    frame_idx: Union[int, None] = None,
    timestamp_sec: Union[float, None] = None,
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


def hconcat_images(image_list):
    min_height = min(img.height for img in image_list)

    resized_images = []
    total_width = 0

    for img in image_list:
        # Calculate the new width to maintain the aspect ratio
        original_width, original_height = img.size

        # New height is the minimum height found in the list
        new_height = min_height

        # Calculate new width: new_width = original_width * (new_height / original_height)
        new_width = int(original_width * (new_height / original_height))

        # Resize the image
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Store the resized image and update the total width
        resized_images.append(img_resized)
        total_width += new_width

    # The new image size is (total_width, min_height)
    concatenated_image = Image.new("RGB", (total_width, min_height))

    x_offset = 0
    for img in resized_images:
        # The position is (x, y) - y is 0 for horizontal concatenation
        concatenated_image.paste(img, (x_offset, 0))
        # Update the horizontal offset for the next image
        x_offset += img.width

    return concatenated_image


def vconcat_images(image_list):
    min_width = min(img.width for img in image_list)

    resized_images = []
    total_height = 0

    for img in image_list:
        original_width, original_height = img.size
        new_width = min_width
        new_height = int(original_height * (new_width / original_width))
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        resized_images.append(img_resized)
        total_height += new_height

    concatenated_image = Image.new("RGB", (min_width, total_height))
    y_offset = 0
    for img in resized_images:
        concatenated_image.paste(img, (0, y_offset))
        y_offset += img.height

    return concatenated_image
