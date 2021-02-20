from netmiko import ConnectHandler
from datetime import datetime
from pprint import pprint

with open("ip.txt") as f:
    ips = f.readlines()


pprint(ips)


arista1 = {
        "device_type": "arista_eos",
        "host": ips[0].rstrip("\n"),
        "username": "admin",
        "password": "Python1"

}

arista2 = {
        "device_type": "arista_eos",
        "host": ips[1].rstrip("\n"),
        "username": "admin",
        "password": "Python2"

}

arista3 = {
        "device_type": "arista_eos",
        "host": ips[2].rstrip("\n"),
        "username": "admin",
        "password": "Python3"

}


switches = [arista1, arista2, arista3]

output_list = []

for switch in switches:
    connection = ConnectHandler(**switch)
    syslog_output = connection.send_command("show logging last 1 day")
    output_list.append(syslog_output)

output_map = 
