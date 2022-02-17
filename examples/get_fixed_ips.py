import os

from dotenv import load_dotenv

from gcore_api.GCore import GCoreAuth, GCoreCloud

load_dotenv()
username = str(os.getenv("GCORE_USERNAME"))
password = str(os.getenv("GCORE_PASSWORD"))
login = GCoreAuth(username, password)
cloud = GCoreCloud(login)
project = cloud.get_project("SberDevices")
region = cloud.get_region("Khabarovsk")
print(cloud.get_region_names())
for region in cloud.regions:
    print(region.display_name, region.id)
fixed_ips = cloud.get_all_fixed_ips(project, region)
print("Printing fixed external ips")
our_ip_list = ["10.7.0.21", "10.7.0.20"]
for fixed_ip in fixed_ips:
    print(
        f"status:{fixed_ip.status}\n"
        f"fixed ip name: {fixed_ip.name}\n"
        f"fixed ip address {fixed_ip.fixed_ip_address}\n"
        f"is vip: {fixed_ip.is_vip}\n"
        f"allowed address pairs: {fixed_ip.allowed_address_pairs}\n"
        f"fixed ip name: {fixed_ip.name}\n")
