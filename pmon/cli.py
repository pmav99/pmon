from __future__ import annotations

import enum
import signal
import sys
import time

from typing import Any
from typing import Dict
from typing import Union

import typer

from .utils import get_proc, get_proc_data, to_bytes


TABS = 10


class RAMVerbosity(str, enum.Enum):
    short = "short"
    default = "default"
    verbose = "verbose"


_HEADERS = {
    RAMVerbosity.short: "uss,uss (%),cpu (%)",
    RAMVerbosity.default: "vms,rss,pss,uss,shared,swap,rss (%),pss (%),uss (%),cpu (%)",
    RAMVerbosity.verbose: "vms,rss,pss,uss,shared,text,lib,data,dirty,swap,rss (%),pss (%),uss (%),cpu (%)",
}

_KEYS = {
    RAMVerbosity.short: "uss,uss_percent,cpu_percent".split(","),
    RAMVerbosity.default: "vms,rss,pss,uss,shared,swap,rss_percent,pss_percent,uss_percent,cpu_percent".split(","),
    RAMVerbosity.verbose: "vms,rss,pss,uss,shared,text,lib,data,dirty,swap,rss_percent,pss_percent,uss_percent,cpu_percent".split(
        ","
    ),  # fmt: off
}


def _get_header(ram: RAMVerbosity, color: bool) -> str:
    header = "\t".join(_HEADERS[ram].split(",")).expandtabs(TABS)
    header = typer.style(header, fg=typer.colors.GREEN, bold=True) if color else header
    return header


def _get_line(ram: RAMVerbosity, data: Dict[str, Union[int, float]]) -> str:
    keys = _KEYS[ram]
    values = [to_bytes(data[key]) for key in keys if not key.endswith("percent")]
    values += ["%.2f" % data[key] for key in keys if key.endswith("percent")]
    line = "\t".join(values).expandtabs(TABS)
    return line


app = typer.Typer()


@app.command(help="Process monitor for linux")
def monitor(
    pid: int = typer.Argument(..., help="The pid of the process you want to monitor"),
    ram: RAMVerbosity = typer.Option(RAMVerbosity.default, help="Choose the verbosity of the RAM output"),
    interval: float = typer.Option(0.5, min=0.01, help="The update interval in seconds"),
    color: bool = typer.Option(True, help="Use colored output"),
    repeat_header: int = typer.Option(20, min=0, help="Repeat the header line every N intervals. Use 0 to disable"),
) -> None:
    try:
        proc = get_proc(pid)
    except ValueError:
        typer.echo(f"The process does not exist: {pid}")
        raise typer.Exit(1)
    header = _get_header(ram=ram, color=color)
    typer.echo(header)
    i = 0
    while True:
        try:
            data = get_proc_data(proc)
        except ValueError:
            typer.echo(f"The process no longer exists: {pid}")
            raise typer.Exit(1)
        line = _get_line(ram, data)
        typer.echo(line)
        time.sleep(interval)
        if repeat_header:
            i += 1
            if i == repeat_header:
                typer.echo(header)
                i = 0


# handle Ctrl-C
def sigint_handler(sig: Any, frame: Any) -> None:
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)
