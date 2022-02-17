import os
from pprint import pprint

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
instances = cloud.list_instances(project, region)
report_list = []
for instance in instances:
    # if instance['instance_name'] in vm_name_list:
    pprint(instance)
    try:
        sec_groups = [sec_group['name'] for sec_group in instance['security_groups']]
    except:
        sec_groups = []
    vm_dict = {
        'instance_name': instance['instance_name'],
        'instance_id': instance['instance_id'],
        'security_groups': sec_groups
    }
    report_list.append(vm_dict)

with open("all_vm_list.yaml", "w") as file:
    yaml.safe_dump({'vm_list': report_list}, file)
print("Done")
