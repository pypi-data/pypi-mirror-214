import datetime

import typer


def log(msg):
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    typer.echo(f'[{ts}] - {msg}')
