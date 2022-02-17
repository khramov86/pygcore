import os
import yaml
from dotenv import load_dotenv

from gcore_api.GCore import GCoreAuth, GCoreCloud

load_dotenv()

username = str(os.getenv("GCORE_USERNAME"))
password = str(os.getenv("GCORE_PASSWORD"))
vm_name_list = ['d-studio-pgsql-gc-msk01', 'pd-studio-pgsql-gc-msk01', 'd-studio-pgsql-gc-msk02']
login = GCoreAuth(username, password)
cloud = GCoreCloud(login)
project = cloud.get_project("SberDevices")
region = cloud.get_region("Moscow")
sec_groups = cloud.get_security_groups(project, region)
report_list = []
for sec_group in sec_groups:
    sec_rule_list = []
    for sec_rule in sec_group['security_group_rules']:
        sec_rule_dict = {
            'description': sec_rule.get('description'),
            'direction': sec_rule.get('direction'),
            'ethertype': sec_rule.get('ethertype'),
            'id': sec_rule.get('id'),
            'port_range_min': sec_rule.get('port_range_min'),
            'port_range_max': sec_rule.get('port_range_max'),
            'protocol': sec_rule.get('protocol'),
            'remote_ip_prefix': sec_rule.get('remote_ip_prefix')
        }
        sec_rule_list.append(sec_rule_dict)
    temp_dict = {
        'id': sec_group.get('id'),
        'name': sec_group.get('name'),
        'security_group_rules': sec_rule_list
    }
    report_list.append(temp_dict)
with open("security_groups.yaml", 'w') as file:
    yaml.safe_dump({'security_group_list': report_list}, file)
