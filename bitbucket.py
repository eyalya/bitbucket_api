__version__ = 'dev'

import requests
import json
import string

class Bitbucket():
    def __init__(self, username, password, workspace):
        self.username   = username
        self.password   = password
        self.workspace  = workspace
        self.base_url   = f"https://api.bitbucket.org/2.0/repositories/{self.workspace}"

    def SetVar(self, repo_name, payload, deployment_uuid=None):
        
        if deployment_uuid:
            url = f"{self.base_url}/{repo_name}/deployments_config/environments/{deployment_uuid}/variables"
        else:
            url = f"{self.base_url}/{repo_name}/pipelines_config/variables/"

        print(url)
        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

        response = requests.request(
        "POST",
        url,
        auth=(self.username, self.password),
        data=payload,
        headers=headers
        )

        print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        print(response.status_code)

    def GetVarUUID(self, repo_name):
        url = f"{self.base_url}/{repo_name}/pipelines_config/variables/"

        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

        response = requests.request(
        "GET",
        url,
        auth=(self.username, self.password),
        headers=headers
        )

        values = json.loads(response.text)["values"]
        print(json.dumps(values, sort_keys=True, indent=4, separators=(",", ": ")))
        # repos = [d['key'] for d in values if d['key'] == "ECS_TASKS_COUNT"]
        # print(repos)
        # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

    def GetEnvUUID(self, repo_name):
        url = f"{self.base_url}/{repo_name}/environments/"

        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

        response = requests.request(
        "GET",
        url,
        auth=(self.username, self.password),
        headers=headers
        )

        # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        return json.loads(response.text)

    def ListEnvUUID(self, repo_name, env_uuid=None, url=None):
        if not url:
            url = f"{self.base_url}/{repo_name}/deployments_config/environments/{env_uuid}/variables?page=0"
        
        # print(url)
        headers = {
        "Accept": "application/json"
        }

        s = requests.Session()
        response = s.get(
        url,
        auth=(self.username, self.password),
        headers=headers
        )
        results = []
        resp_json = response.json()

        # print(json.dumps(resp_json, sort_keys=True, indent=4, separators=(",", ": ")))
        return resp_json, url

    def GetallResults(self, func, *args, **kwargs): 
        results = []
        resp_json, url = func(*args, **kwargs)
        page_num = 1
        
        while resp_json["values"]:
            cleaned = url.rstrip(string.digits)
            url = cleaned + str(page_num)
            page_num += 1
            resp_json, url = func(*args, **kwargs, url=url)
            results += resp_json["values"]

        # print(json.dumps(json.loads(json.dumps(results)), sort_keys=True, indent=4, separators=(",", ": ")))
        return results
                
    def DeleteEnv(self, environment_uuid, variable_uuid):
        url = f"{self.base_url}/{repo_name}/distancecalculationservice/deployments_config/environments/{environment_uuid}/variables/{variable_uuid}"

        response = requests.request(
        "DELETE",
        url,
        auth=(self.username, self.password),
        )

        print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

    def GetAllRepositories(self, url=None):
        if not url:
            url = "https://api.bitbucket.org/2.0/repositories/%7B27d8b4c9-f3db-49f7-b3ba-19a70393cf9b%7D/?page=2"
        
        headers = {
        "Accept": "application/json"
        }

        s = requests.Session()
        response = s.get(
        url,
        auth=(self.username, self.password),
        headers=headers
        )
        results = []
        resp_json = response.json()
        return resp_json, url
        
    def GetAllPRS(self, repo_name):
        url = f"{self.base_url}/{repo_name}/pullrequests"

        response = requests.request(
        "GET",
        url,
        auth=(self.username, self.password),
        )

        values = json.loads(response.text)["values"]
        # repos = [d['full_name'] for d in values]
        # print(response.text)
        print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

    def RunPipeline(self, repo_name, branch):
        url = f"{self.base_url}/{repo_name}/pipelines/"

        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

        payload = json.dumps( {
        "target": {
            "ref_type": "branch",
            "type": "pipeline_ref_target",
            "ref_name": branch
        }
        } )

        response = requests.request(
        "POST",
        url,
        data=payload,
        auth=(self.username, self.password),
        headers=headers
        )

        # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        return response

    def TestCommand(self):
        url = "https://api.bitbucket.org/2.0/repositories/cordiodev/cordio-lambda-schedule-task/pipelines/?page=2"

        headers = {
        "Accept": "application/json"
        }

        s = requests.Session()
        response = s.get(
        url,
        auth=(self.username, self.password),
        headers=headers
        )
        results = []
        resp_json = response.json()

        print(json.dumps(resp_json, sort_keys=True, indent=4, separators=(",", ": ")))

    def ListBranchPermisions(self, repo_name):
        url = f"{self.base_url}/{repo_name}/branch-restrictions"

        response = requests.request(
        "GET",
        url,
        auth=(self.username, self.password),
        )

        values = json.loads(response.text)["values"]
        # repos = [d['full_name'] for d in values]
        # print(response.text)
        # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        return values
    
    def SetBranchPermisions(self, repo_name, payload):
        
        url = f"{self.base_url}/{repo_name}/branch-restrictions"

        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

        response = requests.request(
        "POST",
        url,
        auth=(self.username, self.password),
        data=payload,
        headers=headers
        )

        print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        print(response.status_code)
    
    def DeleteBranchRestriction(repo, id):
        url = f"{self.base_url}/{repo_name}/branch-restrictions/{id}"

        headers = {
            "Accept": "application/json"
        }

        response = requests.request(
        "DELETE",
        url,
        auth=(username, password),
        headers=headers
        )
        print(response)