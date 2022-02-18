#!/usr/bin/env python3
import json
import requests

from GCore import GCoreBase, GCoreAuth, BASE_URL, GCoreCloudRegion, GCoreCloudProject


# except ImportError:
#     import sys
#     GCoreCloudProject = sys.modules[__package__ + '.GCoreCloudProject']
#     GCoreBase = sys.modules[__package__ + '.GCoreBase']
#     GCoreAuth = sys.modules[__package__ + '.GCoreAuth']
#     BASE_URL = sys.modules[__package__ + '.BASE_URL']
#     GCoreCloudRegion = sys.modules[__package__ + '.GCoreCloudRegion']
#     GCoreCloudProject = sys.modules[__package__ + '.GCoreCloudProject']


class GCoreCloudSubnet(GCoreBase):
    def __init__(self, creds: GCoreAuth, subnet: dict):
        super().__init__(creds)
        self.subnet = subnet


class GCoreCloudNetwork(GCoreBase):
    def __init__(self, creds: GCoreAuth, network: dict):
        super().__init__(creds)
        self.id = network.get('id')
        self.name = network.get('name')
        self.region_id = network.get('region_id')
        self.type = network.get('type')
        self.subnets = network.get('subnets')
        self.project_id = network.get('project_id')

    def get_subnet_by_id(self, subnet_id):
        subnet_url = f"{BASE_URL}/subnets/{self.project_id}/{self.region_id}/{subnet_id}"
        response = requests.get(subnet_url, headers=self.headers).json()
        return GCoreCloudSubnet(self.creds, response)

    def get_subnet(self, subnet_name):
        for subnet in self.subnets:
            subnet_url = f"{BASE_URL}/subnets/{self.project_id}/{self.region_id}/{subnet}"
            response = requests.get(subnet_url, headers=self.headers).json()
            if response.get('name').lower() == subnet_name.lower():
                return GCoreCloudSubnet(self.creds, response)

        response = requests.get(subnet_url, headers=self.headers).json()
        return GCoreCloudSubnet(self.creds, response)


class GCoreCloudFloatingIP(GCoreBase):
    def __init__(self, creds: GCoreAuth, floating_ip: dict):
        super().__init__(creds)
        self.created_at = floating_ip.get("created_at")
        self.description = floating_ip.get("description")
        self.fixed_ip_address = floating_ip.get("fixed_ip_address")
        self.floating_ip_address = floating_ip.get("floating_ip_address")
        self.id = floating_ip.get("id")
        self.instance = floating_ip.get("instance")
        self.loadbalancer = floating_ip.get("loadbalancer")
        self.port_id = floating_ip.get("port_id")
        self.project_id = floating_ip.get("project_id")
        self.region_id = floating_ip.get("region_id")
        self.router_id = floating_ip.get("router_id")
        self.status = floating_ip.get("router_id")


class GCoreCloudReservedFixedIP(GCoreBase):
    def __init__(self, creds: GCoreAuth, fixed_ip: dict):
        super().__init__(creds)
        self.allowed_address_pairs = fixed_ip.get("allowed_address_pairs")
        self.created_at = fixed_ip.get("created_at")
        self.creator_task_id = fixed_ip.get("creator_task_id")
        self.fixed_ip_address = fixed_ip.get("fixed_ip_address")
        self.is_external = fixed_ip.get("is_external")
        self.is_vip = fixed_ip.get("is_vip")
        self.name = fixed_ip.get("name")
        self.network = fixed_ip.get("network")
        self.network_id = fixed_ip.get("network_id")
        self.port_id = fixed_ip.get("port_id")
        self.project_id = fixed_ip.get("project_id")
        self.region = fixed_ip.get("region")
        self.region_id = fixed_ip.get("region_id")
        self.reservation = fixed_ip.get("reservation")
        self.status = fixed_ip.get("status")
        self.subnet_id = fixed_ip.get("subnet_id")
        self.task_id = fixed_ip.get("task_id")
        self.updated_at = fixed_ip.get("updated_at")


class GCoreCloudSubnet(GCoreBase):
    def __init__(self, creds: GCoreAuth, subnet: dict):
        super().__init__(creds)
        self.enable_dhcp = subnet.get('enable_dhcp')
        self.has_router = subnet.get('has_router')
        self.host_routes = subnet.get('host_routes')
        self.gateway_ip = subnet.get('gateway_ip')
        self.id = subnet.get('id')
        self.region = subnet.get('region')
        self.region_id = subnet.get('region_id')
        self.project_id = subnet.get('project_id')
        self.available_ips = subnet.get('available_ips')
        self.cidr = subnet.get('cidr')
        self.dns_nameservers = subnet.get('dns_nameservers')
        self.name = subnet.get('name')
        self.network_id = subnet.get('network_id')

    def set_routes(self, route_list: list):
        change_subnet_url = f"{BASE_URL}/subnets/{self.project_id}/{self.region_id}/{self.id}"
        response = requests.patch(change_subnet_url, headers=self.headers,
                                  data=json.dumps({'host_routes': route_list})).json()
        return GCoreCloudSubnet(self.creds, response)

    def add_routes(self, route_list: list):
        change_subnet_url = f"{BASE_URL}/subnets/{self.project_id}/{self.region_id}/{self.id}"
        route_list = self.host_routes + [route for route in route_list if route not in self.host_routes]
        response = requests.patch(change_subnet_url, headers=self.headers,
                                  data=json.dumps({'host_routes': route_list})).json()
        return GCoreCloudSubnet(self.creds, response)

    def create_subnet(self, project: GCoreCloudProject, region: GCoreCloudRegion, network: GCoreCloudNetwork,
                      name: str):
        pass


class GCoreCloudRouter(GCoreBase):
    def __init__(self, creds: GCoreAuth, router_name):
        super().__init__(creds)
        self.router_name = router_name

    @property
    def router_id(self):
        pass


class GCoreCloudFixedIP(GCoreBase):
    def __init__(self, creds: GCoreAuth, fixed_ip: dict):
        super().__init__(creds)
        self.allowed_address_pairs = fixed_ip.get('allowed_address_pairs')
        self.fixed_ip_address = fixed_ip.get('fixed_ip_address')
        self.is_external = fixed_ip.get('is_external')
        self.is_vip = fixed_ip.get('is_vip')
        self.name = fixed_ip.get('name')
        self.network = GCoreCloudNetwork(creds, fixed_ip.get('network'))
        self.network_id = fixed_ip.get('network_id')
        self.port_id = fixed_ip.get('port_id')
        self.project_id = fixed_ip.get('project_id')
        self.region = fixed_ip.get('region')
        self.region_id = fixed_ip.get('region_id')
        self.reservation = fixed_ip.get('reservation')
        self.status = fixed_ip.get('status')
        self.subnet_id = fixed_ip.get('subnet_id')
