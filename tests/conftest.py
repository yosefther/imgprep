"""Shared fixtures.

Builds a small temporary dataset (classes, duplicates, a corrupted file) for tests.
"""
from pathlib import Path 
import pytest 
from PIL import Image

def make_image(path:Path , color:str ="red" , size:tuple[int, int] = (32,32))-> None:
    path.parent.mkdir(parents=True , exist_ok=True)
    Image.new("RGB" , size , color).save(path)

@pytest.fixture
def sample_dataset(tmp_path: Path):
    
    root = tmp_path / "dataset"
    make_image(root / "cats" / "cat1.jpg", "red")
    make_image(root / "cats" / "cat2.PNG", "blue")      
    make_image(root / "dogs" / "dog1.jpg", "green")

    (root / "dogs"/"fake.jpg").write_text("not an image")
    (root / "cats" / ".DS_Store").write_text("junk")
    (root / "notes.txt").write_text("readme")
    (root / "cats" / "._cat1.jpg").write_bytes(b"\x00\x05\x16\x07" + b"\x00" * 20)

    good = root / "dogs" / "truncated.jpg"
    make_image(good , "yellow" , (256,256))
    data=good.read_bytes()
    good.write_bytes(data[:len(data)//2])

    return root 