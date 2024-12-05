import shutil
import subprocess
from pathlib import Path

from neowg import WgServerConfig
from neowg.config import SERVER_CONFIG_PATH

__all__ = [
    "WgService",
]


class WgService:
    def start(self) -> bool:
        if not self._check_ip_forwarding():
            self._setup_ip_forwarding()

        if not self._check_wireguard_exists():
            print("[WgService] WireGuard not found. Trying install wireguard.")
            if not self._install_wireguard():
                return False

        print("[WgService] WireGuard found.")
        if not self._check_config_exists():
            self._create_server_config()

        if not self._is_wireguard_running():
            print("[WgService] WireGuard is not running.")
            if not self._start_wireguard_service():
                return False

        return True

    def _check_wireguard_exists(self) -> bool:
        print("[WgService] Checking if WireGuard exists")
        return shutil.which("wg") is not None

    def _install_wireguard(self) -> bool:
        print("[WgService] Installing WireGuard")
        command = "apt install wireguard"
        result = subprocess.run(command, shell=True,capture_output=True)

        if result.returncode == 0:
            print("[WgService] WireGuard installed")
            return True

        print("[WgService] Installing WireGuard failed")
        print(f"[WgService] stderr='{result.stderr.decode().strip()}'")
        print(f"[WgService] stdout='{result.stdout.decode().strip()}'")
        return False

    def _check_config_exists(self) -> bool:
        print("[WgService] Checking if config file exists")
        return SERVER_CONFIG_PATH.exists()

    def _create_server_config(self) -> None:
        print("[WgService] Creating config file")
        config = WgServerConfig.new()
        config.dump(SERVER_CONFIG_PATH)
        print("[WgService] Config file created")

    def _is_wireguard_running(self) -> bool:
        print("[WgService] Check WireGuard Service up")
        command = "systemctl status wg-quick@wg0"
        result = subprocess.run(command, shell=True, capture_output=True)

        return result.returncode == 0

    def _start_wireguard_service(self) -> bool:
        print("[WgService] Starting WireGuard service")
        command = "systemctl start wg-quick@wg0"
        result = subprocess.run(command, shell=True, capture_output=True)

        if result.returncode == 0:
            print("[WgService] WireGuard Service started")
            return True

        print("[WgService] WireGuard Service start failed")
        print(f"[WgService] stderr='{result.stderr.decode().strip()}'")
        print(f"[WgService] stdout='{result.stdout.decode().strip()}'")
        return False

    def _check_ip_forwarding(self) -> bool:
        print("[WgService] Checking if IP forwarding")
        command = "sysctl -a | grep 'ip_forward ='"
        result = subprocess.run(command, shell=True, capture_output=True)
        stdout = result.stdout.decode().strip()

        if not stdout:
            return False

        return int(stdout.split(' = ')[-1]) == 1

    def _setup_ip_forwarding(self) -> None:
        with Path("/etc/sysctl.conf").open("a") as f:
            f.write("net.ipv4.ip_forward=1\nnet.ipv6.conf.all.forwarding=1")

        command = "sysctl -p"
        subprocess.run(command, shell=True, capture_output=True)
        print("[WgService] IP forwarding setuped")

if __name__ == "__main__":
    WgService().start()