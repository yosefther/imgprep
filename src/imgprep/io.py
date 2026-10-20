"""Find images in a class-per-folder dataset and load them safely.

Corrupted files are reported instead of raising.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

from PIL import Image

IMAGE_EXTENSIONS: Final = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
UNLABELED: Final = "unlabeled"


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


def class_of(path: Path, root: Path) -> str:
    """Return the first folder under root, e.g. root/cats/x.jpg -> "cats".

    Images sitting directly in root have no class and get UNLABELED.
    """
    parts = path.relative_to(root).parts
    if len(parts) == 1:
        return UNLABELED
    return parts[0]


@dataclass
class ScanResult:
    valid: list[tuple[Path, str]] = field(default_factory=list)  # (path, class name)
    corrupt: list[tuple[Path, str]] = field(default_factory=list)  # (path, reason)


def scan_dataset(root: Path) -> ScanResult:
    """Find every image under root and sort it into valid (with class) or corrupt (with reason)."""
    result = ScanResult()
    for path in find_images(root):
        reason = check_image(path)
        if reason is None:
            result.valid.append((path, class_of(path, root)))
        else:
            result.corrupt.append((path, reason))
    return result
