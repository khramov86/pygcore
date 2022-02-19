#!/usr/bin/env python3
# from __future__ import annotations
from dataclasses import dataclass

import requests
import json

from GCoreNetwork import GCoreCloudSubnet, GCoreCloudFloatingIP, GCoreCloudReservedFixedIP, GCoreCloudNetwork
from settings import BASE_URL


class GCoreBase:
    # Пока не вырезать
    def __init__(self, creds: GCoreAuth):
        self.__headers = creds.headers
        self.__creds = creds

    @property
    def headers(self):
        return self.__headers

    @property
    def creds(self):
        return self.__creds


class ProjectDoesNotExists(Exception):
    pass


class RegionDoesNotExists(Exception):
    pass


class GCoreCloud:
    """Облако."""

    regions_url = f'{BASE_URL}/regions'
    projects_url = f'{BASE_URL}/projects'

    def __init__(self, headers: dict):
        self.headers = headers
        self.projects = self._get_request(self.projects_url)
        self.regions = self._get_request(self.regions_url)

    def _get_request(self, url):
        response = requests.get(
            url, headers=self.headers
        ).json().get('results')
        return response

    def get_project(self, project_name):
        for project in self.projects:
            if project['name'] == project_name:
                return project
        raise ProjectDoesNotExists(
            f'Wrong project name, should '
            f'be in: {", ".join([project["name"] for project in self.projects])}'
        )

    def get_region(self, display_name):
        for region in self.regions:
            if region.display_name.lower() == display_name.lower():
                return region
        raise RegionDoesNotExists(
            f'Wrong region name, should '
            f'be in: {", ".join([region.display_name for region in self.regions])}')

    def get_region_names(self):
        return [region.country for region in self.regions]

    def get_project_names(self):
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
