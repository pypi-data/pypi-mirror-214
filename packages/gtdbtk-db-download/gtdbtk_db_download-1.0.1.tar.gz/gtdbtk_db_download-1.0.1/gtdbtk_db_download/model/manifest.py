import gzip
from pathlib import Path
from typing import Dict

from gtdbtk_db_download.util.hash import md5
from gtdbtk_db_download.util.package import get_module_path


class Manifest:

    def __init__(self, data: Dict[Path, str]):
        self.data: Dict[Path, str] = data

    @classmethod
    def from_file(cls, path: Path, expected_hash: str):

        # Verify the integrity of the file
        calculated_hash = md5(path)
        if calculated_hash != expected_hash:
            raise ValueError(f'{path} hash mismatch: {calculated_hash} != {expected_hash}')

        with gzip.open(path, 'rb') as f:
            content = f.read().decode('utf-8')

        out = dict()
        for line in content.splitlines():
            relative_url, file_md5 = line.strip().split('\t')
            out[Path(relative_url)] = file_md5
        return cls(out)


class ManifestR214(Manifest):
    PATH = Path(get_module_path() / 'data' / 'r214_manifest.tsv.gz')
    MD5 = 'df7d0640eac3741a8ffad028d6a27e51'

    @classmethod
    def from_file(cls):
        return super().from_file(ManifestR214.PATH, ManifestR214.MD5)
