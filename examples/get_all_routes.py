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
region = cloud.get_region("Moscow")
networks = cloud.get_all_networks(project, region)
subnets = cloud.get_all_subnets(project, region)
routes_dict = {}
for network in networks:
    routes_dict.setdefault(network.name, {})
    for subnet in subnets:
        if subnet.network_id == network.id:
            routes_dict[network.name].setdefault(subnet.name, {})
            routes_dict[network.name][subnet.name] = {'cidr': subnet.cidr, 'routes': subnet.host_routes}
with open('all_routes.yml', 'w', encoding='utf-8') as f:
    print(yaml.dump(routes_dict), file=f)
