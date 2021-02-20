from easysnmp import Session

def snmpv3():
    ip = input("\nEnter the device IP address: ")
    oid = input("\nEnter the OID or MIB name to work on: ")

    session = Session(hostname = ip, version = 3, security_level = "auth_with_privacy", security_username = "gbenga", auth_protocol="SHA", auth_password="shapass1234", privacy_protocol="AES", privacy_password="aespass1234")
    return oid, session

while True:
    print("\nChoose the SNMP operation you want to perform:\n\ng - SNMP GET\nw - SNMP WALK\ns - SNMP SET\ne -  Exit Program)")
    user_choice = input("\nEnter your choice: ")

    if user_choice == 'g':
        snmp = snmpv3()
        oid = snmp[0]
        session = snmp[1]

        snmp_get = session.get(oid)
        result = snmp_get.value

        print("\nThe result of SNMP GET on {} is: ".format(oid))
        print("\n" + result + "\n")

        continue
    elif user_choice == 'w':
        snmp = snmpv3()
        oid = snmp[0]
        session = snmp[1]

        snmp_walk = session.walk(oid)

        print("\nThe result of SNMP WALK on {} is: ".format(oid))

        for obj in snmp_walk:
            result = obj.value
            print("\n" + result)
        continue

    elif user_choice == 's':
        snmp = snmpv3()
        oid = snmp[0]
        session = snmp[1]

        value = input("\nEnter the value for the object: ")
        snmp_set = session.set(oid, value)

        print("\nDone. Please check device configuration.")
        continue
    elif user_choice == 'e':
        print("\nExiting program...\n")
        break

    else:
        print("\nInvalid Input. Try again!\n")
        continue
        
