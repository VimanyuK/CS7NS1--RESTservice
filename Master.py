# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 15:28:15 2017

@author: Vimanyu
"""

from flask import Flask
from flask_restful import Api
import json, requests, getpass

flask = Flask(__name__)
api = Api(flask)

class master():
    def __init__(self):
        self.number_of_workers = input ('Enter the number of workers needed: ')
        #number of slave connected to the master
        self.current_workers = 0
        #to initialize the timer
        self.start_time = 0.0
        #to store all the commit sha values
        self.commit_list = []
        #taking the git username form the user
        git_username = input('Enter the username or press enter to continue: ')
        #if username is entered, ask for password
        if len(git_username) !=0:
            git_password = getpass.getpass('Enter the Password: ')
        #to check if there are more than 1 page
        pages = True
        page_number = 1
        print('while loop') # for debugging, will be removed later
        while pages:
            if len(git_username) ==0:
                print('if') # for debugging, will be removed later
                link = requests.get("https://api.github.com/repos/VimanyuK/CS7NS1-Chat-Server/commits?page={}&per_page=100".format(page_number))
            else:
                print('else') # for debugging, will be removed later
                link = requests.get("https://api.github.com/repos/VimanyuK/CS7NS1-Chat-Server/commits?page={}&per_page=100".format(page_number), auth=(git_username, git_password))
            json_data = json.loads(link.text)
            print(json_data)
            if len(json_data) < 2:
                pages = False
            else:
                for i in json_data:
                    self.commit_list.append(i['sha'])
                    print("Commit Sha: {}".format(i['sha']))
                    page_number = page_number + 1 
        # Total number of commits in reporepository
        self.total_number_of_commits = len(self.commit_list)  
        print("Number of commits: {}".format(self.total_number_of_commits))

if __name__ == "__main__":
    Master = master()
    flask.run(port = 5555)
                
                
            