import json
import pickle
from pathlib import Path
from typing import Union

import pandas as pd
from PIL import Image
from ruamel.yaml import YAML

yaml = YAML(typ="rt")


def check_path_exists(file_path: Path):
    if file_path.exists():
        return

    current_path = Path("/")
    for part in file_path.parts:
        current_path = current_path / part
        if not current_path.exists():
            break

    existing_path = current_path.parent
    non_existing_path = file_path.relative_to(existing_path)
    raise AssertionError(
        f"Path exists up to: {existing_path}, missing: {non_existing_path}"
    )


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
    return lines[:-1] if lines[-1] == "" else lines


def write_txt(txt_pth: Union[Path, str], data):
    with open(txt_pth, "w") as f:
        if isinstance(data, str):
            f.write(data)
            return
        for item in data:
            f.write("%s\n" % item)


def write_sh(sh_pth: Union[Path, str], data):
    header = "#!/bin/bash\n"
    with open(sh_pth, "w") as f:
        # If the data is a string, we need to check if it starts with the header
        if isinstance(data, str):
            if not data.startswith(header):
                f.write(header)
            f.write(data)
            return

        # If the data is a list, ensure the first item is the header
        if not data or data[0] != header.strip():
            f.write(header)

        # Write the rest of the data
        for item in data:
            f.write(f"{item}\n")


def write_line(txt_pth: Union[Path, str], line):
    with open(txt_pth, "a") as f:
        f.write(line)


def json_load(json_pth: Union[Path, str]):
    if not isinstance(json_pth, str):
        json_pth = str(json_pth)
    with open(json_pth) as f:
        data = json.load(f)
    return data


def jsonl_load(jsonl_pth: Union[Path, str]):
    data = []
    with open(jsonl_pth, "r") as f:
        for line in f:
            data.append(json.loads(line))
    return data


def json_dump(json_pth: Union[Path, str], data):
    if not isinstance(json_pth, str):
        json_pth = str(json_pth)
    with open(json_pth, "w") as f:
        json.dump(data, f, indent=2)


def jsonl_dump(jsonl_pth, data):
    assert isinstance(data, list), "Data must be a list for jsonl"
    with open(jsonl_pth, "w") as f:
        for entry in data:
            json_line = json.dumps(entry)
            f.write(json_line + "\n")


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
    check_path_exists(file_path)

    ext = file_path.suffix

    if ext in {".txt", ".sh", ".md"}:
        return read_txt(file_path)
    elif ext == ".json":
        return json_load(file_path)
    elif ext == ".jsonl":
        return jsonl_load(file_path)
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


def writef(file_path, data, overwrite=True):
    """
    Writes data to a file at the given file path. The file format is determined by the file extension.

    Args:
        file_path: str or Path, the path to the file to write.
        data: the data to write to the file. Can be a list, dict, or pandas DataFrame.
        overwrite: bool, whether to overwrite the file if it exists. Defaults to True.
    """
    # If file_path is not a string or Path, interchange with data
    if not isinstance(file_path, (str, Path)):
        file_path, data = data, file_path

    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    assert (
        file_path.parent.exists()
    ), f"Parent directory does not exist: {file_path.parent}"

    if file_path.exists() and not overwrite:
        print(f"Warning: File {file_path} exists and overwrite=False. Skipping write.")
        return

    ext = file_path.suffix
    if ext in {".txt", ".md"}:
        write_txt(file_path, data)
    elif ext == ".json":
        json_dump(file_path, data)
    elif ext == ".jsonl":
        jsonl_dump(file_path, data)
    elif ext in {".pkl", ".pickle", ".pckl", ".pk"}:
        pickle_dump(file_path, data)
    elif ext == ".yaml":
        yaml_dump(file_path, data)
    elif ext == ".sh":
        write_sh(file_path, data)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
