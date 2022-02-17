#!/usr/bin/env python3
# from __future__ import annotations
import time
import requests
import json

from GCoreNetwork import GCoreCloudSubnet, GCoreCloudFloatingIP, GCoreCloudReservedFixedIP, GCoreCloudNetwork


API_TIMEOUT = 3600
GCORE_AUTH_URL = "https://api.gcdn.co/auth/jwt/login"
BASE_URL = "https://api.cloud.gcorelabs.com/v1"


class GCoreAuth:
    def auth_to_gcore(self):
        headers = {'Content-type': 'application/json'}
        auth = requests.post(GCORE_AUTH_URL, data=(json.dumps(self.gcore_auth)), headers=headers).json()
        self.__headers = {"Authorization": "Bearer {}".format(auth['access']), 'Content-type': 'application/json'}
        self.__headers_timestamp = time.time()

    def __init__(self, username, password):
        self.gcore_auth = {"username": username, "password": password}
        self.auth_url = GCORE_AUTH_URL
        self.auth_to_gcore()

    @property
    def headers(self):
        if self.__headers_timestamp - time.time() < API_TIMEOUT:
            return self.__headers
        else:
            self.auth_to_gcore()
            return self.__headers


class GCoreBase:
    def __init__(self, creds: GCoreAuth):
        self.__headers = creds.headers
        self.__creds = creds

    @property
    def headers(self):
        return self.__headers

    @property
    def creds(self):
        return self.__creds


class GCoreCloudProject(GCoreBase):
    def __init__(self, creds: GCoreAuth, project: dict):
        super().__init__(creds)
        self.name = project.get('name')
        self.id = project.get('id')
        self.state = project.get('state')


class GCoreCloudRegion(GCoreBase):
    def __init__(self, creds: GCoreAuth, region: dict):
        '''
        :param gcoreauth:
        :param region: region object with rows country, display_name, keystone_name, state
        '''
        super().__init__(creds)
        self.country = region.get('country')
        self.keystone_id = region.get('keystone_id')
        self.external_network_id = region.get('external_network_id')
        self.id = region.get('id')
        self.state = region.get('state')
        self.display_name = region.get('display_name')


class GCoreCloud(GCoreBase):
    def __init__(self, creds: GCoreAuth):
        regions_url = f"{BASE_URL}/regions"
        projects_url = f"{BASE_URL}/projects"
        super().__init__(creds)
        self.projects = [GCoreCloudProject(creds, i) for i in requests.get(
            projects_url, headers=self.headers).json().get('results')]
        self.regions = [GCoreCloudRegion(creds, i) for i in requests.get(
            regions_url, headers=self.headers).json().get('results')]

    def get_project(self, project_name):
        for project in self.projects:
            if project.name.lower() == project_name.lower():
                return project
        raise Exception(f"Wrong project name, should"
                        f" be in: {', '.join([project.name for project in self.projects])}")

    def get_region(self, display_name):
        for region in self.regions:
            if region.display_name.lower() == display_name.lower():
                return region
        raise Exception(f"Wrong region name, should"
                        f" be in: {', '.join([region.display_name for region in self.regions])}")

    def get_region_names(self):
        return [region.country for region in self.regions]

    def get_project_name(self):
        return [project.name for project in self.projects]

    def get_all_networks(self, project: GCoreCloudRegion, region: GCoreCloudProject):
        networks_url = f"{BASE_URL}/networks/{project.id}/{region.id}"
        self.networks = [GCoreCloudNetwork(self.creds, i)
                         for i in requests.get(networks_url, headers=self.headers).json().get('results')]
        return self.networks

    def get_network(self, network_name):
        for curr_network in self.networks:
            if network_name.lower() == curr_network.name.lower():
                return curr_network

    def get_all_floating_ips(self, project: GCoreCloudRegion, region: GCoreCloudProject):
        floating_ip_url = f"{BASE_URL}/floatingips/{project.id}/{region.id}"
        self.floating_ips = [GCoreCloudFloatingIP(self.creds, i)
                             for i in requests.get(floating_ip_url, headers=self.headers).json().get('results')]
        return self.floating_ips

    def get_all_subnets(self, project: GCoreCloudRegion, region: GCoreCloudProject):
        subnet_url = f"{BASE_URL}/subnets/{project.id}/{region.id}"
        response = requests.get(subnet_url, headers=self.headers).json().get('results')
        self.subnet_list = [GCoreCloudSubnet(self.creds, subnet) for subnet in response]
        return self.subnet_list

    def get_all_fixed_ips(self, project: GCoreCloudRegion, region: GCoreCloudProject):
        fixed_ips_url = f"{BASE_URL}/reserved_fixed_ips/{project.id}/{region.id}"
        response = requests.get(fixed_ips_url, headers=self.headers).json().get('results')
        self.fixed_ips = [GCoreCloudReservedFixedIP(self.creds, fixed_ip) for fixed_ip in response]
        return self.fixed_ips

    def get_all_ports(self, project: GCoreCloudRegion, region: GCoreCloudProject):
        fixed_ips = self.get_all_fixed_ips(project, region)
        self.ports = []
        for fixed_ip in fixed_ips:
            response = requests.get(
                f"{BASE_URL}/ports/{project.id}/{region.id}/{fixed_ip.port_id}/allow_address_pairs",
                headers=self.headers).json().get("results")
            self.ports.append(response)
        return self.ports

    def set_allowed_host_pairs(self, project: GCoreCloudRegion, region: GCoreCloudProject, port_id: str,
                               allowed_address_pairs: list):
        # self.get_all_ports(project, region)
        # if port_id not in [port for port in self.ports]:
        #     raise Exception("No such port")
        response = requests.put(
            f"{BASE_URL}/ports/{project.id}/{region.id}/{port_id}/allow_address_pairs",
            data=(json.dumps({"allowed_address_pairs": allowed_address_pairs})), headers=self.headers).json()
        return response

    def list_instances(self, project: GCoreCloudRegion, region: GCoreCloudProject):
        """
        Get all instances from GCORE API
        https://apidocs.gcorelabs.com/cloud#operation/InstanceViewSetV1.get
        """
        response = requests.get(f"{BASE_URL}/instances/{project.id}/{region.id}", headers=self.headers).json().get(
            "results")
        return response

    def get_security_groups(self, project: GCoreCloudRegion, region: GCoreCloudProject):
        """
        Get all security groups from GCORE API
        https: // api.cloud.gcorelabs.com / v1 / securitygroups / {project_id} / {region_id}
        """
        response = requests.get(f"{BASE_URL}/securitygroups/{project.id}/{region.id}", headers=self.headers).json().get(
            "results")
        return response
