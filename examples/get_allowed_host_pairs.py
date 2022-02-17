import os

import yaml
from dotenv import load_dotenv

from gcore_api.GCore import GCoreAuth, GCoreCloud

load_dotenv()
username = str(os.getenv("GCORE_USERNAME"))
password = str(os.getenv("GCORE_PASSWORD"))
login = GCoreAuth(username, password)
cloud = GCoreCloud(login)
project = cloud.get_project("SberDevices")
allowed_host_pais_list = []
allowed_host_pais_dict = {}
our_ip_list = ["10.7.0.21", "10.7.0.20", "10.3.0.11", "10.3.0.10", "10.10.0.31", "10.10.0.30", "10.6.0.31", "10.6.0.30"]
for region_name in ["Khabarovsk", "Moscow"]:
    region = cloud.get_region(region_name)
    fixed_ips = cloud.get_all_fixed_ips(project, region)
    floating_ips = cloud.get_all_floating_ips(project, region)
    for fixed_ip in fixed_ips:
        if fixed_ip.fixed_ip_address in our_ip_list:
            allowed_host_pais_list.append({
                "fixed_ip_address": fixed_ip.fixed_ip_address,
                "port_id": fixed_ip.port_id,
                "allowed_address_pairs": fixed_ip.allowed_address_pairs
            }
            )
    allowed_host_pais_dict[region_name] = allowed_host_pais_list
    allowed_host_pais_list = []
with open("current_allowed_host_pairs.yml", "w") as f:
    yaml.dump(allowed_host_pais_dict, f)

