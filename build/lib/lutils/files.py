import json
import pickle
from pathlib import Path
from typing import Union

from ruamel.yaml import YAML
import pandas as pd
from PIL import Image

yaml = YAML(typ='rt')

def pickle_load(pkl_pth: Union[Path, str]):
    with open(pkl_pth, "rb") as file:
        pickle_data = pickle.load(file)

    return pickle_data


def pickle_dump(pkl_pth: Union[Path, str], data):
    with open(pkl_pth, "wb") as output_file:
        pickle.dump(data, output_file)


def read_txt(txt_pth: Union[Path, str]) -> list:
    with open(txt_pth) as f:
        lines = f.read().split("\n")
    return lines[:-1]


def write_txt(txt_pth: Union[Path, str], data):
    with open(txt_pth, "w") as f:
        for item in data:
            f.write("%s\n" % item)


def write_line(txt_pth: Union[Path, str], line):
    with open(txt_pth, "a") as f:
        f.write(line)


def json_load(json_pth: Union[Path, str]):
    if not isinstance(json_pth, str):
        json_pth = str(json_pth)
    with open(json_pth) as f:
        data = json.load(f)
    return data


def json_dump(json_pth: Union[Path, str], data):
    if not isinstance(json_pth, str):
        json_pth = str(json_pth)
    with open(json_pth, "w") as f:
        json.dump(data, f, indent=2)


def torch_load(pth: Union[Path, str]):
    import torch

    if not isinstance(pth, Path):
        pth = Path(pth)
    return torch.load(str(pth))


def load_pkl_dir(pkl_dir: Union[Path, str]):
    if not isinstance(pkl_dir, Path):
        pkl_dir = Path(pkl_dir)
    pkl_pths = list(pkl_dir.glob("*.pkl"))
    assert len(pkl_pths) > 0, f"No pkl files found in {pkl_dir}"
    pkl_pths.sort()
    pkls = []
    for pkl_pth in pkl_pths:
        pkls.append(pickle_load(str(pkl_pth)))

    data = pd.concat(pkls, ignore_index=True)
    return data


def read_image(image_path: Union[str, Path]) -> Image.Image:
    with open(image_path, "rb") as f:
        img = Image.open(f)
        img.load()
    return img


def yaml_load(file_path: Union[str, Path]):
    with open(file_path, "r") as f:
        return yaml.load(f)


def yaml_dump(file_path: Union[str, Path], data):
    with open(file_path, "w") as f:
        yaml.dump(data, f)


def openf(file_path):
    """
    Open file and return contents
    """
    file_path = Path(file_path)
    assert file_path.exists(), f"File does not exist: {file_path}"

    ext = file_path.suffix

    if ext == ".txt":
        return read_txt(file_path)
    elif ext == ".json":
        return json_load(file_path)
    elif ext in {".pkl", ".pickle", ".pckl", ".pk"}:
        return pickle_load(file_path)
    elif ext == ".pth":
        return torch_load(file_path)
    elif ext in {".jpg", ".jpeg", ".png", ".bmp", ".gif"}:
        return read_image(file_path)
    elif ext in {".yaml"}:
        return yaml_load(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")


def writef(file_path, data, **kwargs):
    """
    Writes data to a file at the given file path. The file format is determined by the file extension.

    Args:
        file_path: str or Path, the path to the file to write.
        data: the data to write to the file. Can be a list, dict, or pandas DataFrame.
        **kwargs: optional keyword arguments to pass to the file writing functions.
    """
    # If file_path is not a string or Path, interchange with data
    if not isinstance(file_path, (str, Path)):
        file_path, data = data, file_path

    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    assert (
        file_path.parent.exists()
    ), f"Parent directory does not exist: {file_path.parent}"

    ext = file_path.suffix
    if ext == ".txt":
        write_txt(file_path, data)
    elif ext == ".json":
        json_dump(file_path, data, **kwargs)
    elif ext in {".pkl", ".pickle", ".pckl", ".pk"}:
        pickle_dump(file_path, data)
    elif ext == ".yaml":
        yaml_dump(file_path, data)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
