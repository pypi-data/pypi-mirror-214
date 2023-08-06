from pathlib import Path

import requests

from gtdbtk_db_download.config import GTDBTK_R214_REMOTE
from gtdbtk_db_download.util.hash import md5


def download_file_worker_mp(job):
    return download_file_worker(*job)


def download_file_worker(target_dir: Path, relative_path: Path, expected_md5: str, force: bool):
    # Messages to be returned
    result = {
        'relative_path': relative_path,
        'success': False,
        'error': None,
    }

    try:
        # Create the output file path
        target_path = target_dir / relative_path

        # If the file already exists, check the md5
        if target_path.exists():
            if md5(target_path) != expected_md5:
                if force:
                    target_path.unlink()
                else:
                    result['error'] = 'File exists and md5 does not match.'
                    result['success'] = False
                    return result

        # Create the parent directory
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Download the file
        url = f'{GTDBTK_R214_REMOTE}/{relative_path}'
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with target_path.open('wb') as f:
                for chunk in r.iter_content(chunk_size=8_192):
                    f.write(chunk)

        # Validate the checksum
        calculated_md5 = md5(target_path)
        if calculated_md5 != expected_md5:
            target_path.unlink()
            result['error'] = f'File was corrupted on download.'
            result['success'] = False
            return result

        # Return the result
        result['success'] = True
        return result

    except Exception as e:
        result['error'] = str(e)
        result['success'] = False
