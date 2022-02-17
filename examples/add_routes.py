import os

import yaml
from dotenv import load_dotenv

from gcore_api.GCore import GCoreAuth, GCoreCloud, GCoreCloudNetwork

load_dotenv()

routes = """
    - destination: 172.16.0.0/16
      nexthop: 10.10.0.66
    - destination: 172.17.0.0/16
      nexthop: 10.10.0.66
    - destination: 172.28.0.0/17
      nexthop: 10.10.0.66
    - destination: 100.64.30.0/24
      nexthop: 10.10.0.66
    - destination: 10.255.254.0/24
      nexthop: 10.10.0.66
    - destination: 100.65.45.0/30
      nexthop: 10.10.0.66
"""
routes_list = yaml.safe_load(routes)
print(routes_list)
username = str(os.getenv("GCORE_USERNAME"))
password = str(os.getenv("GCORE_PASSWORD"))
login = GCoreAuth(username, password)
cloud = GCoreCloud(login)
project = cloud.get_project("SberDevices")
region = cloud.get_region("Moscow")
networks = cloud.get_all_networks(project, region)
network = cloud.get_network('dev_network')
subnet = network.get_subnet('dev_net')
# print(subnet.host_routes)
subnet = subnet.add_routes(routes_list)
print(yaml.dump(subnet.host_routes))
