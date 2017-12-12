# -*- coding: utf-8 -*-
import json, requests 

def Slave_main():
    ip = input('Enter the IP for the Master Server: ')
    port = input('Enter the Port number for the Master Server: ')
    commits = 0
    
    link = requests.get("http://{}:{}/repo".format(ip,port), json={'pullStatus': False})
    json_data = json.load(link.text)
    print(json_data)
    repository_link = json_data['repo']
    
if __name__ == "__main__":
    Slave_main()