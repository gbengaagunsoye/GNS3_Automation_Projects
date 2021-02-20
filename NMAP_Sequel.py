import nmap
from pprint import pprint

while True:
    print("""\nWhat do you want to do?\n
                1 - Get detailed info about a device
                2 - Scan the network for open ports
                e - Exit the application""")
    user_input = input("\nEnter your option: ")

    if user_input == "1":
        mynmap = nmap.PortScanner()
        ip = input("\nPlease enter the IP address to scan: ")
        print("\nThis may take a while ...\n")
        scan = mynmap.scan(ip, '1-1024', '-v -sS -sV -O -A -e ens3')
        # pprint(scan)

        print("\n= = = = = = = HOST {} = = = = = = =".format(ip))
        print("\n\nGENERAL INFO")

        try:
            mac = scan['scan'][ip]['address']['mac']
            print("\n-> MAC address: {}".format(mac))
        except KeyError:
            pass

        os = scan['scan'][ip]['osmatch'][0]['name']
        print("\n-> Operating System: {}".format(os))

        uptime = scan['scan'][ip]['uptime']['lastboot']
        print("\n-> Device uptime: {}".format(uptime))

        print("\n\nPORTS\n")

        for port in list(scan['scan'][ip]['tcp'].items()):
            print("-> {} | {} | {}".format(port[0], port[1]['name'], port[1]['state']))

        print("\n\nOTHER INFO\n")
        print("-> NMAP command: {}".format(scan['nmap']['command_line']))

        version = str(mynmap.nmap_version()[0]) + "." + str(mynmap.nmap_version()[1])
        print("-> NMAP version: {}".format(version))

        print("-> Time elapsed: {}".format(scan['nmap']['scanstats']['elapsed'] + "seconds"))

        print("-> Time of scan: {}".format(scan['nmap']['scanstats']['timestr']))
        print("\n\n")

        continue
    elif user_input == "2":
        mynmap = nmap.PortScanner()
        print("\nThis may take a while ...\n")
        scan = mynmap.scan(ports = '1-1024', arguments = '-sS -e ens3 -iL /home/osboxes/Apps/ip.txt')

        for device in scan['scan']:
            print("\nPorts open on {}".format(device))
            for port in scan['scan'][device]['tcp'].items():
                if port[1]['state'] == 'open':
                    print("-->" + str(port[0]) + "|" + port[1]['name'])
        continue

    elif user_input == "e":
        print("\nExiting program....\n")
        break
    else:
        print("\nInvalid input. Try again!\n")
        continue
