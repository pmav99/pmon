import signal
import sys
import time

import typer

from .utils import get_proc, get_proc_data, HEADER, VERBOSE_HEADER


app = typer.Typer()


def _get_header(verbose: bool, color: bool) -> str:
    header = VERBOSE_HEADER if verbose else HEADER
    if color:
        header = typer.style(header.expandtabs(10), fg=typer.colors.GREEN, bold=True)
    else:
        header = header.expandtabs(10)
    return header


@app.command(help="Process monitor for linux")
def monitor(
    pid: int = typer.Argument(..., help="The pid of the process you want to monitor"),
    interval: float = typer.Option(0.5, min=0.1, help="The update interval in seconds"),
    verbose: bool = typer.Option(False, help="Use verbose output"),
    color: bool = typer.Option(True, help="Use colored output"),
    show_header: int = typer.Option(20, min=0, help="Show the header line every N intervals. Use 0 to disable"),
):
    try:
        proc = get_proc(pid)
    except ValueError:
        typer.echo(f"The process does not exist: {pid}")
        raise typer.Exit(1)
    header = _get_header(verbose=verbose, color=color)
    typer.echo(header)
    i = 0
    while True:
        try:
            line = get_proc_data(proc, verbose=verbose)
        except ValueError:
            typer.echo(f"The process no longer exists: {pid}")
            raise typer.Exit(1)
        typer.echo(line.expandtabs(10))
        time.sleep(interval)
        if show_header:
            i += 1
            if i == show_header:
                typer.echo(header)
                i = 0


# handle Ctrl-C
def sigint_handler(sig, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)
