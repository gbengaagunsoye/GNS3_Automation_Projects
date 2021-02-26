
import logging
import subprocess
import re
import sys

try:
    from scapy.all import *

except ImportError:
    print("Scapy is not installed on your system.")
    print("Try using: sudo pip3.8 install scapy.")
    sys.exit()

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
logging.getLogger("scapy.interactive").setLevel(logging.ERROR)
logging.getLogger("scapy.loading").setLevel(logging.ERROR)

conf.checkIPaddr = False

with open("dhcp.txt") as f:
    allowed_dhcp_servers = f.read()

host_if = subprocess.run("ip link", shell = True, stdout = subprocess.PIPE)
interfaces = re.findall(r"\d:\s(.+?):\s", str(host_if))
print(interfaces)

for interface in interfaces:
    if interface != "lo":
        hw = get_if_raw_hwaddr(interface)[1]
        print(hw)

        dhcp_discover = Ether(dst = "ff:ff:ff:ff:ff:ff") / IP(src="0.0.0.0", dst="255.255.255.255") / UDP(sport = 68, dport = 67) / BOOTP(chaddr = hw) / DHCP(options = [("message-type", "discover"), "end"])

        ans, unans = srp(dhcp_discover, multi = True, iface = interface, timeout = 5, verbose = 0)

        mac_ip = {}

        for pair in ans:
            print(pair)
            mac_ip[pair[1][Ether].src] = pair[1][IP].src

        if ans:
            print("\n--> The following DHCP Servers found on the {} LAN:\n".format(interface))
            for mac, ip in mac_ip.items():
                if ip in allowed_dhcp_servers:
                    print("OK! IP Address: {}, MAC Address: {}\n".format(ip, mac))
                else:
                    print("ROGUE! IP Address: {}, MAC Address: {}\n".format(ip, mac))
        else:
            print("\n--> No active DHCP servers found on the {} LAN. \n".format(interface))
    else:
        pass
