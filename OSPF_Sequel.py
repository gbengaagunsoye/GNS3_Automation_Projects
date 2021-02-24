import matplotlib
import networkx
from easysnmp import Session
from pprint import pprint


ip = input("\nEnter the 'root' device IP address: ")

ospf = []

def ospf_func(ip):
    nbridlist = []
    nbriplist = []
    ospf_device = {}

    session = Session(hostname = ip, version = 3, security_level = "auth_with_privacy", security_username = "gbenga", auth_protocol="SHA", auth_password="shapass1234", privacy_protocol="AES", privacy_password="aespass1234")
    snmp_walk = session.walk('.1.3.6.1.2.1.14.1.1')
    # pprint(snmp_walk)
    ospf_host_id = snmp_walk[0].value

    #performing snmp walk to get OSPF neighbor IDs
    snmp_walk = session.walk('.1.3.6.1.2.1.14.10.1.3')
    # pprint(snmp_walk)

    for neighbor_id in snmp_walk:
        nbridlist.append(neighbor_id.value)

    #performing snmp walk to get OSPF neighbor IPs
    snmp_walk = session.walk('.1.3.6.1.2.1.14.10.1.1')
    # pprint(snmp_walk)

    for neighbor_ip in snmp_walk:
        nbriplist.append(neighbor_ip.value)

    ospf_device["HostID"] = ospf_host_id
    ospf_device["NbrRtrID"] = nbridlist
    ospf_device["NbrRtrIP"] = nbriplist
    # pprint(ospf_device)

    if ospf_device not in ospf:
        ospf.append(ospf_device)

    return ospf

ospf = ospf_func(ip)
pprint(ospf)
