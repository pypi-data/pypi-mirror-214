import lzma
from pathlib import Path
import shutil
from urllib.request import urlopen

def download_file(write_dir: Path, url: str) -> Path:
    filename = url.rsplit("/", 1)[-1]
    filepath = Path(write_dir, filename)
    with urlopen(url) as response:
        with filepath.open(mode="w+b") as f:
            shutil.copyfileobj(response, f)
    return filepath


def try_unzip(arg: Path):
    one_less_suffix = arg.with_suffix("")
    if arg.suffix == ".xz":
        with lzma.open(arg) as decompressed:
            with one_less_suffix.open(mode="w+b") as f:
                shutil.copyfileobj(decompressed, f)
        return try_unzip(one_less_suffix)
    return arg



