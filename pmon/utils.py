from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

import psutil


__all__: List[str] = [
    "get_proc",
    "get_proc_data",
    "HEADER",
    "VERBOSE_HEADER",
]


SYMBOLS = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
ATTRS = ("memory_full_info", "cpu_percent")
HEADER = "\t".join("rss,vms,shared,pss,swap,uss,cpu (%),mem (%)".split(","))
VERBOSE_HEADER = "\t".join("rss,vms,shared,text,lib,data,dirty,pss,swap,uss,cpu (%),mem (%)".split(","))


def to_bytes(n: int) -> str:
    prefix = {}
    for i, symbol in enumerate(SYMBOLS):
        prefix[symbol] = 1 << (i + 1) * 10
    for symbol in reversed(SYMBOLS):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return f"{value:.2f}{symbol}"
    return f"{n}B"


def get_line(info: Dict[str, Any]) -> str:
    memory_full_info = info["memory_full_info"]._asdict()
    line = "\t".join([
        to_bytes(memory_full_info["rss"]),
        to_bytes(memory_full_info["vms"]),
        to_bytes(memory_full_info["shared"]),
        to_bytes(memory_full_info["pss"]),
        to_bytes(memory_full_info["swap"]),
        to_bytes(memory_full_info["uss"]),
        f"{info['cpu_percent']:.2f}",
        f"{info['memory_percent']:.2f}",
    ])
    return line


def get_verbose_line(info: Dict[str, Any]) -> str:
    memory_full_info = info["memory_full_info"]._asdict()
    line = "\t".join([
        to_bytes(memory_full_info["rss"]),
        to_bytes(memory_full_info["vms"]),
        to_bytes(memory_full_info["shared"]),
        to_bytes(memory_full_info["text"]),
        to_bytes(memory_full_info["lib"]),
        to_bytes(memory_full_info["data"]),
        to_bytes(memory_full_info["dirty"]),
        to_bytes(memory_full_info["pss"]),
        to_bytes(memory_full_info["swap"]),
        to_bytes(memory_full_info["uss"]),
        f"{info['cpu_percent']:.2f}",
        f"{info['memory_percent']:.2f}",
    ])
    return line


def get_proc(pid: int) -> psutil.Process:
    try:
        proc = psutil.Process(pid)
    except psutil.NoSuchProcess:
        raise ValueError(f"The process does not exist: {pid}")
    else:
        return proc


def get_proc_data(proc: psutil.Process, verbose: bool = False, attrs: Tuple[str] = ATTRS) -> str:
    try:
        with proc.oneshot():
            info = proc.as_dict(attrs=attrs)
            info["memory_percent"] = proc.memory_percent("uss")
    except psutil.NoSuchProcess:
        raise ValueError(f"The process no longer exists: {proc.pid}")
    else:
        if verbose:
            line = get_verbose_line(info)
        else:
            line = get_line(info)
        return line
