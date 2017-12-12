# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api, Resource
from flask_restful import reqparse
import json, requests, getpass, time

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
            print(json_data) # for debugging, will be removed later
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

class fetchRepository(Resource):
    def __init__(self):
        global Master
        # initializing Master server globaly
        self.server = Master
        # initializing Resource CLass as per Method Resolution Order
        super(fetchRepository, self).__init__()
        self.reqparser = reqparse.RequestParser()
        
        # For every value coming in JSON, you need an argument
        self.reqparser.add_argument('pullStatus', type=int, location = 'json')
        self.reqparser.add_argument('complexity', type=float, location='json')
        
    def get(self):
        repo_args = self.reqparser.parse.args()
        # check if the repository has been pulled
        if repo_args['pull_status'] == False:
            print('not pulled yet') # for debugging will be removed
            return {'repo': "https://api.github.com/VimanyuK/CS7NS1-Chat-Server"}
        if repo_args['pull_status'] == True:
            print('pull status true') # for debugging will be removed
            self.server.current_workers += 1
            #To start the timer when the required number of slaves are assigned
            if self.server.current_workers == self.server.number_of_workers:
                self.start_time = time.time()
                print('Timer Started') # for debugging will be removed
            print("WORKER NUMBER: {}".format(self.server.current_workers))

api.add_resource(fetchRepository, "/repo", endpoint="repo")
    
if __name__ == "__main__":
    Master = master()
    flask.run(port = 5555)
                
                
            