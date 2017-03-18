'''
Description: Flask Application to read yaml file from Github
Created By: Jasmeet Singh
'''
import json
import sys
import re

from flask import Flask, Response
import yaml
import github

class GithubConfig(object):
    GITHUB_USER = None
    GITHUB_REPO = None

    def __init__(self, github_url):
        github_detail = re.split(r'/|\\', github_url)
        try:
            self.GITHUB_USER = github_detail[3]
            self.GITHUB_REPO = github_detail[4]
            print "GITHUB_USER : " + self.GITHUB_USER
            print "GITHUB_REPO : " + self.GITHUB_REPO
        except Exception:
            raise ValueError("Github url invalid")

    def get_github_user_name(self):
        return self.GITHUB_USER

    def get_github_repo(self):
        return self.GITHUB_REPO

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello test first Dockerized Flask App!!!"

@app.route("/v1/<config_file_name>")
def print_config(config_file_name):
    (filename, file_extension) = tuple(re.split(r'\.', config_file_name))
    actualfilename = filename + ".yml"
    try:
        github_auth = github.Github()
        github_user = github_auth.get_user(app.config['GITHUB_USER'])
        github_repo = github_user.get_repo(app.config['GITHUB_REPO'])
        file_content = github_repo.get_file_contents(actualfilename).decoded_content

        data = yaml.load(file_content)

        if (file_extension == 'yml' or file_extension == 'yaml'):
            #Commented as professor requirments is to display without single quotes
            #Response(yaml.load(file_content), mimetype='application/yaml')
            return Response(file_content, mimetype='application/yaml')
        else:
            return Response(json.dumps(data), mimetype='application/json')
    except Exception as error:
        print error
        return "404: Invalid Page access!!"

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            GITHUB_URL = str(sys.argv[1])
            Github_Config = GithubConfig(GITHUB_URL)
            app.config.from_object(Github_Config)
            app.run(debug=True, host='0.0.0.0')
        else:
            raise ValueError("Github: Depot location is missing!!")
    except ValueError as error:
        sys.exit(error)
