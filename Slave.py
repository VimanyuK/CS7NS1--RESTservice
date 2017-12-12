# -*- coding: utf-8 -*-
import json, requests, subprocess

def Slave_main():
    ip = input('Enter the IP for the Master Server: ')
    port = input('Enter the Port number for the Master Server: ')
    commits = 0
    
    link = requests.get("http://{}:{}/repo".format(ip,port), json={'pull_status': False})
    json_data = json.loads(link.text)
    print(json_data)
    repository_link = json_data['repo']
    subprocess.call(["bash","workerInitScript.sh",repository_link],shell=True)
    print('subprocess') # for debugging will be removed
    
    link = requests.get("http://{}:{}/repo".format(ip,port), json={'pull_status': True})
    
    have_commits = True
    while have_commits:
        print('while') # for debugging will be removed
        link = requests.get("http://{}:{}/cyclomatic".format(ip,port))
        json_data = json.loads(link.text)
        print("Received: {}".format(json_data['sha']))
        if json_data['sha'] == -2:
            print("Polling")
        else:
            if json_data['sha'] == -1:
                print("No items left")
                break
            subprocess.call(["bash", "workerGetCommit.sh", json_data['sha']], shell=True)
            binRadonCCOutput = subprocess.check_output(["radon", "cc", "-s", "-a" , "workerData"])
            radonCCOutput = binRadonCCOutput.decode("utf-8")  
            print(radonCCOutput)
            avgCCstartPos = radonCCOutput.rfind("(")  
            if radonCCOutput[avgCCstartPos+1:-2] == "":  
                print("NO RELEVENT FILES")
                link = requests.post("http://{}:{}/cyclomatic".format(ip,port),
                                  json={'commitSha': json_data['sha'], 'complexity': -1})
            else:
                averageCC = float(radonCCOutput[avgCCstartPos+1:-2]) 
                link = requests.post("http://{}:{}/cyclomatic".format(ip,port),
                                  json={'commitSha': json_data['sha'], 'complexity': averageCC})
            commits += 1  # Increment the number of commits this node has completed
    print("Completed having computed {} commits (including non-computable commits)".format(commits))
    
    
if __name__ == "__main__":
    Slave_main()