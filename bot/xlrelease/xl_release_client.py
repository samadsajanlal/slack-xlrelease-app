import requests


class XLReleaseClient(object):
    """XL Release Client to connect to fetch data from server"""

    def __init__(self, xl_release_config=None, secret=None):
        self.base_url = xl_release_config["xl_release_url"]
        self.username = xl_release_config["username"]
        self.password = secret

    def get_user(self):
        url = "{}/api/v1/users/{}".format(self.base_url, self.username)
        return requests.get(url, auth=(self.username, self.password))

    def get_templates(self):
        url = self.base_url + "/api/v1/templates"
        response = requests.get(url, auth=(self.username, self.password))
        if response.status_code == 200:
            return response.json()

    def get_template(self, template_id=None):
        url = "{}/api/v1/templates/{}".format(self.base_url, template_id)
        response = requests.get(url, auth=(self.username, self.password))
        if response.status_code == 200:
            return response.json()

    def get_releases(self):
        url = self.base_url + "/api/v1/releases"
        response = requests.get(url, auth=(self.username, self.password))
        if response.status_code == 200:
            return response.json()

    def get_release(self, release_id=None):
        url = "{}/api/v1/releases/{}".format(self.base_url, release_id)
        response = requests.get(url, auth=(self.username, self.password))
        if response.status_code == 200:
            return response.json()

    def create_release(self, template_id=None, request_body=None):
        url = "{}/api/v1/templates/{}/create".format(self.base_url, template_id)
        response = requests.post(url, auth=(self.username, self.password), data=request_body,
                                 headers={"Content-Type": "application/json"})
        return response

    def get_active_tasks(self, release_id=None):
        url = "{}/api/v1/releases/{}/active-tasks".format(self.base_url, release_id)
        response = requests.get(url, auth=(self.username, self.password))
        return response

    def get_task(self, task_id=None):
        url = "{}/api/v1/tasks/{}".format(self.base_url, task_id)
        response = requests.get(url, auth=(self.username, self.password))
        if response.status_code == 200:
            return response.json()

    def assign_task(self, task_id=None, owner=None):
        url = "{}/api/v1/tasks/{}/assign/{}".format(self.base_url, task_id, owner)
        response = requests.post(url, auth=(self.username, self.password))
        return response

    def task_action(self, task_id=None, action=None, request_body=None):
        url = "{}/api/v1/tasks/{}/{}".format(self.base_url, task_id, action)
        response = requests.post(url, auth=(self.username, self.password), data=request_body,
                                 headers={"Content-Type": "application/json"})
        return response

    def get_task_definitions(self):
        url = "{}/tasks/task-definitions".format(self.base_url)
        response = requests.get(url, auth=(self.username, self.password))
        return response
