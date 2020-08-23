import paramiko
import time
from devices import switches

for switch in switches:
    ip_address = switch['ip']
    username = switch['username']
    password = switch['password']
    host = switch['host']

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_address, username=username, password=password)

    print("Configuring ", host + "... ")
    print("Successful connection", ip_address)

    remote_connection = ssh_client.invoke_shell()

    remote_connection.send("terminal length 0\n")
    remote_connection.send("configure terminal\n")
    remote_connection.send("int loop 0\n")
    remote_connection.send("ip address 1.1.1.1 255.255.255.255\n")
    remote_connection.send("int loop 1\n")
    remote_connection.send("ip address 2.2.2.2 255.255.255.255\n")
    remote_connection.send("router ospf 1\n")
    remote_connection.send("network 0.0.0.0 255.255.255.255 area 0\n")

    for n in range(2, 11):
        print("Creating VLAN " + str(n))
        remote_connection.send("vlan " + str(n) + "\n")
        remote_connection.send("name AXIOM_" + str(n) + "\n")
        time.sleep(1)

    remote_connection.send("end\n")

    time.sleep(2)
    output = remote_connection.recv(65535)
    print(output.decode('ascii'))

    ssh_client.close()
