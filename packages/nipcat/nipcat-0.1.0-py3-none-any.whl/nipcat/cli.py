import click
from rich.console import Console
from rich.table import Table
from rich.theme import Theme
from ipaddress import IPv4Network
from nipcat.utils import *

theme = Theme({
    "property": "bold magenta",
    "value": "bright_green",
    "title": "bold cyan",
    "error": "bold red"
})
console = Console(theme=theme)


@click.command()
@click.option('-i','--info', is_flag=True, help='current ip')
@click.argument('subnet', required=False)
def main(info:bool, subnet: str):
    if info:
        handle_info()
    elif subnet:
        handle_subnet(subnet)

def handle_subnet(subnet:str):
    try:
        info = NetCalc.compute(subnet)
        table = Table(title=f"Details for {subnet}",
                    show_header=False,
                    show_lines=False,
                    show_edge=False)

        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="yellow")
        basic_rows = [
            ("Address", info.network_address),
            ("Netmask", info.netmask),
            ("Wildcard", info.wildcard_mask),
            ("Broadcast", info.broadcast_address),
            ("HostMin", info.first_host),
            ("HostMax", info.last_host),
            ("Hosts/Net", str(info.num_hosts)),
            ("CIDR", info.cidr_notation),
            ("Class", info.network_class),
            ("Private", "Yes" if info.is_private else "No")
        ]

        for property_name, value in basic_rows:
            table.add_row(property_name, value)
        console.print(table)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {str(e)}")

def handle_info():
    info = NetworkInfo()
    external_ip = info.get_external_ip()
    hostname = info.get_hostname()
    interfaces = info.get_interfaces()
    console.print("External IP: ", external_ip)
    console.print("Hostname: ", hostname)
    for interface in interfaces:
        console.print(interface.name+":")
        console.print("   ip: "+interface.ip_addresses[0])
        console.print("   mac: "+interface.mac_address)


if __name__ == '__main__':
    main()
