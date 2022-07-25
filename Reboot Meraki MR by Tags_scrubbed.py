##Alex R Hansen
##Systems Engineer
##SLED East, Mid-Atlantic




import requests
from datetime import datetime
from datetime import timedelta
import meraki
import os
import csv
import time
import pandas as pd

ap_dict = []
rebooted_dict = []
reboot_aps = []



def get_org_id(name):
    all_orgs = dashboard.organizations.getOrganizations()

    for org in all_orgs:
        if org['name'] == name:
            return org['id']

    print("Org Does Not Exist")
    raise Exception
def get_tagged_devices(org_id: str):
    response = dashboard.organizations.getOrganizationInventoryDevices(organizationId = org_id, total_pages='all')
    product_type = ['wireless']
    for item in response:
        if item['productType'] in product_type and item['tags']:
            print(item['name'])
            print(item['tags'])
            ap_dict.append([item['name'],item['tags'],item['serial']])
    print(response)
    print(ap_dict)
    
def which_tag():
    desired_tag = input('Which Tag would you like the APs to reboot?')
    for item in ap_dict:
        if desired_tag in item[1]:
            reboot_aps.append([item[0],item[1],item[2]])
        else:
            continue
    if reboot_aps == []:
        print('Could not find Tag in network, please re-run this script')
    print(reboot_aps)
    

def reboot_APs():
    for i in reboot_aps:
##        print(i[1])
        time.sleep(15)
        response = dashboard.devices.rebootDevice(i[2])
##        print(response['success'])
        if response['success'] == True:
            rebooted_dict.append([i[0],i[1],i[2]])
##            print(rebooted_dict)
##            print(ap_dict)
            print(i[0]+" rebooted")
        else:
            print("Problem rebooting " + i[0] + ", Retrying now...")
            response = dashboard.devices.rebootDevice(i[2])
            if response['success'] == True:
                rebooted_dict.append([i[0],i[1],i[2]])
##                print(rebooted_dict)
##                print(ap_dict)
                print(i[0]+" rebooted")
            else:
                print("Could not reboot "+i[0]+". Please view Access Point on Dashboard")
            
        
    return 






    
if __name__ == "__main__":
    API_KEY = "a679774fe018e983fbedff81d0fc067dfa70c54b"
    ORG_NAME = "RogueNet"
    
    dashboard = meraki.DashboardAPI(
        api_key=API_KEY,
        base_url='https://api.meraki.com/api/v1/',
        output_log=False,
        log_file_prefix=os.path.basename(__file__)[:-3],
        log_path='',
        print_console=False
    )

    org_id = get_org_id(name=ORG_NAME)
    get_tagged_devices(org_id)
    which_tag()
    print(org_id)
    print(ap_dict)
    print(reboot_aps)
    ##reboot_APs()
