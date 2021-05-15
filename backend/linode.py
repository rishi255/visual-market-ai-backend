import os
import time

import paramiko
from dotenv import load_dotenv
from linode_api4 import LinodeClient
from paramiko.client import SSHClient

# ssh into Linode in commandline
print("-" * 100)
load_dotenv()
USERNAME = os.getenv(key="USERNAME")
PASSWORD = os.getenv(key="PASSWORD")
IP = os.getenv(key="IP")

client = SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.load_system_host_keys()
client.connect(hostname=IP, username=USERNAME, password=PASSWORD, look_for_keys=True)
command = "cd /root & ls -1Fa"
fish_shell = client.invoke_shell(term="fish")

print(f"client: {client}")
print(f"\nfish shell: {fish_shell}")
print(f"\nexecuted command: {command}")
stdin, stdout, stderr = client.exec_command(command=command)
time.sleep(5)

print(f"stdout: {stdout}")
print(f"stdout content: {stdout.readlines()}")
client.close()

# accessing linode client via API
print("-" * 100)
TOKEN1 = os.getenv(key="TOKEN1")
client = LinodeClient(token=TOKEN1)

my_linodes = client.linode.instances()
print("available linodes:\n")
for current_linode in my_linodes:
    print(current_linode.label)

available_regions = client.regions()
print(f"\navailable regions:\n{list(available_regions)}")

current_linode = my_linodes[0]
print(f"\ncurrent linode: {current_linode}")
# print(f'ssh root@{current_linode.ipv4[0]} - {PASSWORD}')
