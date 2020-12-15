from __future__ import annotations

from typing import Dict
from typing import List
from typing import Union

import psutil  # type: ignore


__all__: List[str] = [
    "get_proc",
    "get_proc_data",
]


SYMBOLS: List[str] = ["K", "M", "G", "T", "P", "E", "Z", "Y"]
TOTAL_MEMORY: int = psutil.virtual_memory().total
PREFIX: Dict[str, int] = {
    "K": 1024,
    "M": 1048576,
    "G": 1073741824,
    "T": 1099511627776,
    "P": 1125899906842624,
    "E": 1152921504606846976,
    "Z": 1180591620717411303424,
    "Y": 1208925819614629174706176,
}


def to_bytes(n: Union[int, float]) -> str:
    for symbol in reversed(SYMBOLS):
        if n >= PREFIX[symbol]:
            value = float(n) / PREFIX[symbol]
            return f"{value:.3f}{symbol}"
    return f"{n}B"


def get_proc(pid: int) -> psutil.Process:
    try:
        proc = psutil.Process(pid)
    except psutil.NoSuchProcess:
        raise ValueError(f"The process does not exist: {pid}")
    else:
        return proc


def get_proc_data(proc: psutil.Process) -> Dict[str, Union[int, float]]:
    data: Dict[str, Union[int, float]] = {}
    try:
        with proc.oneshot():
            data.update(proc.memory_full_info()._asdict())
            data["cpu_percent"] = proc.cpu_percent()
            data["rss_percent"] = data["rss"] / TOTAL_MEMORY * 100
            data["pss_percent"] = data["pss"] / TOTAL_MEMORY * 100
            data["uss_percent"] = data["uss"] / TOTAL_MEMORY * 100
            data["vms_percent"] = data["vms"] / TOTAL_MEMORY * 100
    except psutil.NoSuchProcess:
        raise ValueError(f"The process no longer exists: {proc.pid}")
    else:
        return data
