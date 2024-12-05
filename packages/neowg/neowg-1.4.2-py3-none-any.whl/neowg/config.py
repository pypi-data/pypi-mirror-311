from typing import Final
from pathlib import Path

__all__ = [
    "WIREGUARD_PORT",
    "SERVER_CONFIG_PATH",
]

WIREGUARD_PORT: Final[int] = 51280
SERVER_CONFIG_PATH: Final[Path] = Path("/etc/wireguard/wg0.conf")
