
import json
import os
from collections import namedtuple
import requests
import datetime,configparser, re
from palindrome.TargetResource import *
from palindrome.ClientCredentials import *
from palindrome.AuthorizationHeader import *



class TraceProduction:

    def ppn(self,url):
        config = configparser.RawConfigParser()
        config.read('palindrome.ini')
        palindromeConfig = config['palindrome-config']
        clientId = palindromeConfig['clientid']
        secret = palindromeConfig['secret']
        context = palindromeConfig['service']
        payload=""
        regex = r"^(.*:)\/\/([A-Za-z0-9\-\.]+)(:[0-9]+)?(.*)$"    
        host = re.search(regex, url).group(2)
        endpoint = re.search(regex,url).group(4)
        resource = endpoint
        dt = '{:%Y%m%d}'.format(datetime.datetime.now())
        targetResource = TargetResource(host, resource)
        credentials = ClientCredentials(clientId, dt, context)
        header = AuthorizationHeader.from_(secret, credentials, targetResource,payload)
        secureHeaderAuth = header.serialize()
        headers = {'Authorization' : secureHeaderAuth, 'Content-Type' : "application/x-www-form-urlencoded"}#headers=headers/
        return headers

    def load_conf(self):
        file = open("configuration.json")
        self.conf  = json.load(file)

    def initialize_conduit(self,):
        try:
            self.json_template = json.loads(open('templates/template.json','r').read())
            self.endpoint = self.conf['curl']
            self.json_template['source']['client_id']=self.conf["data_source"]
            self.json_template['source']['workstation']['station']=self.conf['station']
        except Exception as e:
            print(e)

    def __init__(self) -> None:
        self.load_conf()
        self.initialize_conduit()

    
    def conduit_login(self,un,pw):
        try:
            self.json_template['source']['employee']= un
            self.json_template['source']['password']= pw
            self.json_template['transactions'] = []
            self.json_template['transactions'].append({"unit": {"unit_id":"123" ,"part_number": "","revision": ""},"commands": [{"command":{"name": "End"}}]})
            login_info = requests.post(self.endpoint, json=self.json_template).json()
            if login_info["status"]["code"] == "ERROR" and "cannot log in" in login_info["status"]["message"]:
                self.json_template['source']['employee']= ""
                self.json_template['source']['password']= ""
                return False

            else:
                return True  
        except Exception as e:
            return False

    def check_whatlog(self,sn,swk,pn):
        try:
            url = self.conf["murl"]+ "/" +self.conf["data_source"]+ f"/units/{sn}"
            unit_info = requests.request("GET", url,headers=self.ppn(url)).json()
            with open("123.txt","w") as f:
                json.dump(unit_info,f)
            if unit_info['success']==True:
                try:
                    if unit_info["data"]["short_workstation"] == swk:

                        if unit_info["data"]["part_number"]==pn:
                                return True,"",unit_info["data"]["short_workstation"]
                            
                        else:
                            return False, "Invalid Part - "+ unit_info["data"]["part_number"],unit_info["data"]["short_workstation"]
                    else:
                        return False, "Flow Error - "+ unit_info["data"]["long_workstation"],unit_info["data"]["short_workstation"]
                except Exception:
                    return False,"The Serial seems to be assembled or Not Found",""
                                
            else:
                return False,"Request Failed - Invalid Request / Serial",""
        except Exception as e:
            print(e)
            return False, "AppException or Invalid Serial",""

    def assemble_pcba(self,p_sn,c_sn,ref_desg):
        try:
            transaction = self.json_template['transactions'] = []
            unit = {"unit":{"unit_id":p_sn},"commands":[]}
            transaction.append(unit)
            addnt = {"command":{"name":"AddTrackedComponent", "component_id":c_sn, "ref_designator":ref_desg}}
            transaction[0]['commands'].append(addnt)
            posting = requests.post(self.endpoint, json=self.json_template)
            if posting.status_code == 200:
                reply = posting.json()
                if reply["status"]["code"]=="OK":
                        return True, reply["status"]["message"],reply
                else: 
                    return False, reply["status"]["message"],reply
        except Exception as e:
            print("assemble_pcba",str(e))
            return False,"App Exception","e"

    def conduit_end(self,sn):
        try:
            self.json_template['transactions'] = []
            self.json_template['transactions'].append({"unit": {"unit_id":sn ,"part_number": "","revision": ""},"commands": [{"command":{"name": "End"}}]})
            posting = requests.post(self.endpoint, json=self.json_template)
            if posting.status_code == 200:
                reply = posting.json()
                if reply["status"]["code"]=="OK":
                    return True, reply["status"]["message"],reply
                else: 
                    return False, reply["status"]["message"],reply
                
            else:
                raise Exception('Conduit Communication Error')
           
        except Exception as e:
            print(e)
            return False, e
            









