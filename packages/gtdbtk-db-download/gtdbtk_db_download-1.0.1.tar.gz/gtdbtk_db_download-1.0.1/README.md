# GTDB-Tk Database Download

Minimal toolkit for downloading the GTDB-Tk database to disk.

This is **not the recommended way** to download the GTDB-Tk reference database, please see 
[here](https://ecogenomics.github.io/GTDBTk/installing/index.html#gtdb-tk-reference-data) for the reccomended method.

This softare may be useful for users who are experiencing intermittent connection errors, or slow download speeds.

## 📚 Requirements

This software requires Python >=3.8 and makes use of the following packages:

* [requests](https://pypi.org/project/requests/)
* [tqdm](https://pypi.org/project/tqdm/)
* [typer](https://pypi.org/project/typer/)

## ⚙️ Installation

In a new virtual environment, or conda environment that is running Python >=3.8, simply run:

```shell
python -m pip install gtdbtk_db_download
```

## 🚀 Usage

For a complete list of options, run: `gtdbtk_db_download --help`

Example usage downloading to the `/tmp/db` directory:

```shell
gtdbtk_db_download /tmp/db --threads 10
```

### Example output

```text
[2023-06-16 13:51:41] - gtdbtk_downloader v1.0.0
[2023-06-16 13:51:41] - Creating output directory.
[2023-06-16 13:51:41] - Loading R214 manifest
[2023-06-16 13:51:42] - Creating queue
[2023-06-16 13:51:42] - Downloading files
[2023-06-16 16:00:00] - Done.
```
