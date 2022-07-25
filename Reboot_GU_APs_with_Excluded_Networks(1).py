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

def get_org_id(name):
    all_orgs = dashboard.organizations.getOrganizations()

    for org in all_orgs:
        if org['name'] == name:
            return org['id']

    print("Org Does Not Exist")
    raise Exception

def get_AP_SNs(org_id: str):
     x = 0
     print(org_id)
     response = dashboard.organizations.getOrganizationInventoryDevices(organizationId = org_id, total_pages='all')
##     print(response)
     exludedNetworks = [None, 'L_660903245316631764','L_660903245316631781']
     includedModels = ['MR52','MR53','MR53E']
     for item in response:
         if item['model'] in includedModels and item['networkId'] not in excludedNetworks:
             x=x+1
             print(x)
             ap_dict.append([item['name'],item['serial']])
  ##           print(ap_dict)
  ##   SN_list = response.json()['serial']
             
     return 

def reboot_APs():
    for i in ap_dict:
##        print(i[1])
        time.sleep(15)
        response = dashboard.devices.rebootDevice(i[1])
##        print(response['success'])
        if response['success'] == True:
            rebooted_dict.append([i[0],i[1]])
##            print(rebooted_dict)
##            print(ap_dict)
            print(i[0]+" rebooted")
        else:
            print("Problem rebooting " + i[0] + ", Retrying now...")
            response = dashboard.devices.rebootDevice(i[1])
            if response['success'] == True:
                rebooted_dict.append([i[0],i[1]])
##                print(rebooted_dict)
##                print(ap_dict)
                print(i[0]+" rebooted")
            else:
                print("Could not reboot "+i[0]+". Please view Access Point on Dashboard")
            
        
    return 



if __name__ == "__main__":
    API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ORG_NAME = "<insert org name>"
    
    dashboard = meraki.DashboardAPI(
        api_key=API_KEY,
        base_url='https://api.meraki.com/api/v1/',
        output_log=False,
        log_file_prefix=os.path.basename(__file__)[:-3],
        log_path='',
        print_console=False
    )

    org_id = get_org_id(name=ORG_NAME)
##    print(org_id)
    get_AP_SNs(org_id)
    ap_dict = sorted(ap_dict)
    print(ap_dict)
    x = 0
    for i in ap_dict:
        print(i)
        x=x+1
        print(x)
    df = pd.DataFrame({'Name':'','serial':''},columns= ['Name', 'serial'])
    for i in ap_dict:
        df2 = pd.DataFrame({i[0],i[1]}, columns= ['Name', 'serial'])
        df.append(df2)
    df.to_csv()
##    reboot_APs()

    
    
