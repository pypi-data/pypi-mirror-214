import json
import requests
import time
import re
import socket
from stix2 import Indicator

class ioc():
    def __init__(self, api_token = "", limit = 10):
        self.api_token = api_token
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        self.limit = limit
        self.json_data = {
            'api_token': self.api_token,
            'limit': self.limit,
        }

    def daily_ioc(self,):
        if self.api_token == "":
            return print("Please Use Your API Token")
        if self.limit > 100:
            return print("Limit can not exceed 100")

        return requests.post(
            'https://ioc.threatmonit.io/api/daily-ioc/',
            headers=self.headers,
            json=self.json_data,
        ).json()

    def QRadarIntegration(self, 
                        import_data,
                        qradar_auth_key,
                        qradar_server,
                        qradar_ref_set
                        ):
        
        # self.qradar_auth_key = "811aacf9-jh68-444h-98f4-5d25b7a94844"
        self.qradar_ref_set = "THREATMON_Event_IOC"

        QRadar_POST_url = f"https://{qradar_server}/api/reference_data/sets/bulk_load/{qradar_ref_set}"

        self.QRadar_headers = {
            'sec': qradar_auth_key,
            'content-type': "application/json",
        }

        print(time.strftime("%H:%M:%S") + " -- " + "Initiating, IOC POST to QRadar ")
        files = []

        for key in import_data["entities"]:
            files.extend(ioc["hash"] for ioc in key["hashes"])
            
        qradar_response = requests.request("POST", QRadar_POST_url, data=files, headers=self.QRadar_headers, verify=False)
        if qradar_response.status_code == 200:
            print(time.strftime("%H:%M:%S") + " -- " + " (Finished) Imported IOCs to QRadar (Success)" )
        else:
            print(time.strftime("%H:%M:%S") + " -- " + "Could not POST IOCs to QRadar (Failure)")
            
    def SentinelIntegration(self,
                            import_data,
                            bearerToken,
                            workspaceId,
                            systemName,
                            ):  # sourcery skip: avoid-builtin-shadow
        
        ioc_list = []
        api_url = f"https://sentinelus.azure-api.net/{workspaceId}/threatintelligence:upload-indicators?api-version=2022-07-01"
                        
        for iocs in import_data["entities"]:
            for ioc in iocs["hashes"]:
                if ioc["algorithm"] == "MD5":
                    hash = ioc["hash"]
                    indicator = Indicator(name="indicator",
                        pattern= f"[file:hashes.md5 = '{hash}']",
                        pattern_type="stix")
                    
                if ioc["algorithm"] == "SHA-1":
                    hash = ioc["hash"]
                    indicator = Indicator(name="indicator",
                        pattern= f"[file:hashes.sha1 = '{hash}']",
                        pattern_type="stix")
                    
                if ioc["algorithm"] == "SHA-256":
                    hash = ioc["hash"]
                    indicator = Indicator(name="indicator",
                        pattern= f"[file:hashes.sha256 = '{hash}']",
                        pattern_type="stix")
                    
                indicator = indicator.serialize(sort_keys=True)
                indicator = json.loads(indicator)
                ioc_list.append(indicator)

        request_body = {
            "sourcesystem": systemName,
            "value": ioc_list
        }
        
        headers = {
            'Authorization': bearerToken,
            'Content-Type': 'application/json',
        }
        
        try:
            microsof_api = requests.post(
                url=api_url,
                headers=headers,
                json=request_body,
            )
            if microsof_api.status_code == 200:
                print(time.strftime("%H:%M:%S") + " -- " + " (Finished) Imported IOCs to Sentinel (Success)" )
            else:
                print(time.strftime("%H:%M:%S") + " -- " + "Could not POST IOCs to Sentinel (Failure)")
        except Exception as e:
            print(e)