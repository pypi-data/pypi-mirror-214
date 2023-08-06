import multiprocessing as mp
import sys
from enum import Enum
from pathlib import Path

import typer
from tqdm import tqdm
from typing_extensions import Annotated

from gtdbtk_db_download import __version__
from gtdbtk_db_download.model.manifest import ManifestR214
from gtdbtk_db_download.util.log import log
from gtdbtk_db_download.worker import download_file_worker_mp

HOST_HELP = 'The remote host to download the data from.'
THREADS_HELP = 'The number of threads to use for downloading.'
FORCE_HELP = 'True existing files in target_dir that do not match the checksum should be overwritten.'


class Release(str, Enum):
    r214 = 'r214'


def download(
        target_dir: Path,
        force: Annotated[bool, typer.Option(help=FORCE_HELP)] = False,
        release: Annotated[
            Release, typer.Option(help='The GTDB-Tk release to download.', case_sensitive=False)] = Release.r214,
        threads: Annotated[int, typer.Option(help=THREADS_HELP)] = 1,
):
    """
    Download the (uncompressed) GTDB-Tk data repository from the remote host.
    """

    log(f'gtdbtk_downloader v{__version__}')

    log('Creating output directory.')
    target_dir.mkdir(parents=True, exist_ok=True)

    log('Loading R214 manifest')
    manifest = ManifestR214.from_file()

    log('Creating queue')
    queue = [(target_dir, k, v, force) for k, v in manifest.data.items()]

    log('Downloading files')
    with mp.Pool(threads) as pool:
        results = list(tqdm(pool.imap_unordered(download_file_worker_mp, queue), total=len(queue), smoothing=0.01))

    # Report any errors
    if all((x['success'] for x in results)):
        log('All files downloaded successfully.')
        log('Done.')
        sys.exit(0)
    else:
        log('Some errors were encountered while downloading files:')
        for result in results:
            if not result['success']:
                log(f'    {result["relative_path"]}: {result["error"]}')
        log('Re-run the program again to retry, potentially with --force to overwrite existing files.')
        log('Done.')
        sys.exit(1)


def main():
    typer.run(download)


if __name__ == '__main__':
    main()
