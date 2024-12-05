import subprocess

__all__ = [
    "get_server_net_interface",
    "get_server_ip",
]

def get_server_net_interface() -> str:
    command = "ip -o -4 route show to default"
    output = subprocess.check_output(command, shell=True).decode("utf-8")
    return output.split()[4]


def get_server_ip() -> str:
    network_interface = get_server_net_interface()
    command = f"ip -o -4 addr show dev {network_interface}"

    output = subprocess.check_output(command, shell=True).decode("utf-8")
    return output.split()[5]
