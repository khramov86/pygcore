import os
from pprint import pprint

import requests
import yaml
from dotenv import load_dotenv

from gcore_api.GCore import GCoreAuth, GCoreCloud, GCoreCloudNetwork

load_dotenv()

username = str(os.getenv("GCORE_USERNAME"))
password = str(os.getenv("GCORE_PASSWORD"))
login = GCoreAuth(username, password)
cloud = GCoreCloud(login)
project = cloud.get_project("SberDevices")
region = cloud.get_region("Khabarovsk")
floating_ips = cloud.get_all_floating_ips(project, region)
print("Printing floating ips")
for floating_ip in floating_ips:
    print(floating_ip.floating_ip_address)
