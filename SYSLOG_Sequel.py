from netmiko import ConnectHandler
from datetime import datetime
from pprint import pprint
import re

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

pprint(output_list)
print(len(output_list))


output_map = {}

for output in output_list:
    hostname_regex = re.findall(r".+\d\d:\d\d:\d\d\s(.+?)\s", output)
    # pprint(hostname_regex)
    hostname = hostname_regex[0]

    output_lines = output.split("\n")
    pprint(output_lines)

    lldp_lines = []

    for line in output_lines:
        if re.search(r"LLDP", line, re.I) and re.search(r"neighbor", line, re.I):
            lldp_lines.append(line + "\n")

    output_map[hostname] = lldp_lines

# pprint(output_map)

with open("lldp_{}".format(datetime.now().strftime("%Y-%m-%d-%H-%M")), "w") as f:
    for entry in output_map.items():
        f.write(entry[0] + "\n")
        f.writelines(entry[1])
        f.write("\n\n")
