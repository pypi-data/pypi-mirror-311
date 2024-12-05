from pathlib import Path
from typing import Self

from neowg.wg_client_config import WgClientConfig
from neowg.key_pair import KeyPair
from neowg.config import WIREGUARD_PORT
from neowg.utils import get_server_ip, get_server_net_interface


class WgServerConfig:
    _keys: KeyPair
    _clients: list[WgClientConfig]
    _server_ip: str
    _net_adapter: str

    @classmethod
    def new(cls: type[Self], clients_count: int = 100) -> Self:
        """Создание нового конфига."""
        config = cls()
        config._server_ip = get_server_ip()
        config._keys = KeyPair()
        config._net_adapter = get_server_net_interface()

        config._clients = []

        last_octec = 0
        pre_last_octec = 0
        i = 0
        octecs = []

        while i < clients_count:
            if i % 255 == 0 and i != 0:
                last_octec = 1
                pre_last_octec += 1
            else:
                last_octec += 1

            i += 1
            octecs.append((pre_last_octec, last_octec))


        for pre_last_octec, last_octec in octecs:
            if not (pre_last_octec == 0 and last_octec in (0, 1)):
                config._clients.append(WgClientConfig(
                    ip=f"10.8.{pre_last_octec}.{last_octec}",
                    server_host=f"{config._server_ip}:{WIREGUARD_PORT}",
                    server_pubkey=config._keys.pubkey,
                ))

        return config

    @classmethod
    def from_file(cls: type[Self], path: Path | str) -> Self:
        """Чтение wireguard конфига из файла."""
        path = Path(path)
        config = cls()

        with path.open() as f:
            interface, *peers = f.read().split("\n\n")

        config._keys = cls._parse_server_keys(interface)
        config._server_ip = cls._parse_server_ip(interface)
        config._clients = cls._parse_clients(peers, config._keys.pubkey, f"{config._server_ip}:{WIREGUARD_PORT}")
        config._net_adapter = cls._parse_net_adapter(interface)

        return config

    def dump(self, path: Path | str) -> None:
        """Запись wireguard конфига в файл по указанному пути."""

        path = Path(path)

        file_content = """[Interface]
Address = 10.8.0.1/24
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o {net_adapter} -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o {net_adapter} -j MASQUERADE
ListenPort = {server_port}
PrivateKey = {private_key}
# PublicKey = {pubkey}
# ServerIP = {server_ip}
"""
        file_content = file_content.format(
            server_port=51280,
            private_key=self._keys.private_key,
            pubkey=self._keys.pubkey,
            server_ip=self._server_ip,
            net_adapter=self._net_adapter,
        )

        for client in self._clients:
            client_content = """
[Peer]
AllowedIPs = {ip}/32
# PrivateKey = {private_key}
PublicKey = {pubkey}
# Used = {used}
"""
            file_content += client_content.format(
                pubkey=client.pubkey, ip=client.ip, private_key=client.private_key, used=client.used
            )

        with path.open("w", encoding="utf-8") as f:
            f.write(file_content)

    def update_keys(self, ip: str) -> KeyPair:
        """Обновление пары ключей у указанного ip. Вернет новую пару ключей."""

        for client in self._clients:
            if client.ip == ip:
                return client.update_keys()

    @staticmethod
    def _parse_server_keys(interface: str) -> KeyPair:
        *_, private_key, pubkey, server_ip = interface.splitlines()
        _, pubkey = pubkey.split(' = ')
        _, private_key = private_key.split(' = ')
        return KeyPair(pubkey=pubkey, private_key=private_key)

    @staticmethod
    def _parse_server_ip(interface: str) -> str:
        *_, server_ip = interface.splitlines()
        return server_ip.split(' = ')[-1]

    @staticmethod
    def _parse_clients(peers: list[str], server_pubkey: str, server_host: str) -> list[WgClientConfig]:
        clients: list[WgClientConfig] = []
        for peer in peers:
            *_, ip, private_key, pubkey, used = peer.splitlines()
            private_key = private_key.split(' = ')[-1]
            pubkey = pubkey.split(' = ')[-1]
            ip = ip.split(' = ')[-1].split('/')[0]
            used = used.split(' = ')[-1].split('/')[0]

            clients.append(WgClientConfig(
                ip=ip,
                server_host=server_host,
                server_pubkey=server_pubkey,
                keys=KeyPair(pubkey=pubkey, private_key=private_key),
                used=used == "True",
            ))

        return clients

    @staticmethod
    def _parse_net_adapter(interface: str) -> str:
        lines = interface.splitlines()
        return lines[2].split('POSTROUTING -o ')[-1].replace(' -j MASQUERADE', '')

    def __str__(self) -> str:
        return f'WgServerConfig(keys={self._keys}, server="{self._server_ip}", clients={self._clients})'

    @property
    def clients(self) -> list[WgClientConfig]:
        return self._clients.copy()

    def allocate_config(self) -> WgClientConfig | None:
        for i in range(len(self._clients)):
            if not self._clients[i].used:
                self._clients[i].mark_used()
                return self._clients[i]
        return None