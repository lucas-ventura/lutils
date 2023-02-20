# lutils

`lutils` is a Python package that provides utility functions for reading and writing files, as well as image processing functions.

## Installation

To install `lutils`, run:

```bash
pip install git+https://github.com/lucas-ventura/lutils.git
```

## Usage

### Reading and writing files

`lutils` provides the following functions for reading and writing files:

- `read_txt(txt_pth: str) -> list`: Reads a text file and returns its contents as a list of strings.
- `write_txt(txt_pth: str, data)`: Writes a list of strings to a text file.
- `json_load(json_pth: str)`: Loads a JSON file and returns its contents.
- `json_dump(json_pth: str, data)`: Writes a dictionary to a JSON file.
- `pickle_load(pkl_pth: str)`: Loads a pickled object from a file.
- `pickle_dump(pkl_pth: str, data)`: Pickles an object and writes it to a file.

### Image processing

`lutils` provides the following function for image processing:

- `center_crop(image)`: Crops the center of an image to a square.

## Example

```python
from lutils import openf, writef, center_crop

# Read a text file
lines = openf("example.txt")

# Write a list of strings to a text file
writef("example.txt", ["foo", "bar", "baz"])

# Load a JSON file
data = openf("example.json")

# Write a dictionary to a JSON file
writef("example.json", {"foo": 1, "bar": 2, "baz": 3})

# Load a pickled object from a file
obj = openf("example.pkl")

# Pickle an object and write it to a file
writef("example.pkl", {"foo": 1, "bar": 2, "baz": 3})

# Crop the center of an image
image = openf("example.jpg")
cropped_image = center_crop(image)
```
