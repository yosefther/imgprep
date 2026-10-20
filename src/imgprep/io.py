"""Find images in a class-per-folder dataset and load them safely.

Corrupted files are reported instead of raising.
"""

from pathlib import Path
from typing import Final

from PIL import Image

IMAGE_EXTENSIONS: Final = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def is_image_file(path: Path) -> bool:
    """check 1 : decided by the NAME only. Doesn't open the file."""
    if not path.is_file():
        return False
    if path.name.startswith("."):
        return False
    return path.suffix.lower() in IMAGE_EXTENSIONS


def check_image(path: Path) -> str | None:
    """Return None if the image is fine, otherwise the reason it's broken."""
    try:
        with Image.open(path) as img:
            img.load()
    except Image.DecompressionBombError:
        return "image too large (possible decompression bomb)"
    except OSError as e:
        return f"cannot read image: {e}"
    except Exception as e:  # malformed files can raise other errors inside Pillow
        return f"unexpected error: {type(e).__name__}: {e}"
    return None


def is_valid_image(path: Path) -> bool:
    """check 2 : opens the file and fully decodes it."""
    return check_image(path) is None


def find_images(root: Path) -> list[Path]:
    """Return every image file under root, including subfolders, sorted."""
    if not root.exists():
        raise FileNotFoundError(f"folder not found: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"not a folder: {root}")
    images: list[Path] = []
    for path in root.rglob("*"):
        if is_image_file(path):
            images.append(path)
    return sorted(images)


def class_of(path): ...
def scan_dataset(): ...


# FUNCTION scan_dataset(root) -> ScanResult
# valid   = empty list
# corrupt = empty list
# FOR each path in find_images(root)
# IF is_valid_image(path)
# add (path, class_of(path, root)) to valid
# ELSE
# add path to corrupt
# return ScanResult(valid, corrupt)


# FUNCTION class_of(path, root) -> string
# return the name of the folder that directly contains path
# dataset/cats/cat1.jpg -> "cats"
# an image sitting directly in root has no class -> decide: return "" or "unlabeled"

# DATA ScanResult
# valid:   list of (path, class name)
# corrupt: list of paths
