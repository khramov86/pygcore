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
our_ip_list = ["10.7.0.21", "10.7.0.20", "10.3.0.11", "10.3.0.10", "10.10.0.31", "10.10.0.30", "10.6.0.31", "10.6.0.30"]
with open("current_allowed_host_pairs.yml") as f:
    target_allowed_host_pais_dict = yaml.safe_load(f)
for region_name, region_host_pairs in target_allowed_host_pais_dict.items():
    region = cloud.get_region(region_name)
    fixed_ips = cloud.get_all_fixed_ips(project, region)
    for region_host_pair in region_host_pairs:
        for fixed_ip in fixed_ips:
            if fixed_ip.fixed_ip_address == region_host_pair.get('fixed_ip_address'):
                print(fixed_ip.port_id, region_host_pair.get('allowed_address_pairs'), sep='\n')
                result = cloud.set_allowed_host_pairs(project, region, fixed_ip.port_id, region_host_pair.get('allowed_address_pairs'))
                print(result)
