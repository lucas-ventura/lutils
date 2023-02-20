import cv2
from PIL import Image


def get_frame(video_pth: str, frame_idx):
    if not isinstance(video_pth, str):
        video_pth = str(video_pth)
    cap = cv2.VideoCapture(video_pth)
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
