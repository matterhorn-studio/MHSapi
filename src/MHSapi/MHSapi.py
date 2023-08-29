from aiopenapi3 import OpenAPI
from aiopenapi3.errors import HTTPStatusError, ResponseSchemaError
import pandas as pd
import webbrowser

class MHSapiClient:

    def __init__(self, token, dev=False):
        self.token = token
        self.base_url = 'https://matterhorn.studio'
        if dev:
            self.base_url = 'http://localhost:8000/'


        self.api = OpenAPI.load_sync(self.base_url + "api/schema/")
        self.api.authenticate(Authorization=f"Token {self.token}")

        if dev:
            operationIds = list(self.api._.Iter(self.api, False))
            print(operationIds)

    def experiments_create(self,data,open_browser=True):
        req = self.api.createRequest("api_experiments_create")
        try:
            headers, data, response = req.request(parameters={}, data=data)
        except HTTPStatusError as e:
            print(f"Error:{e.response.content}")
        experiment = data
        if open_browser:
            self.open_experiment(experiment)
        return experiment

    def parameters_create(self,data):
        req = self.api.createRequest("api_parameters_create")
        try:
            headers, data, response = req.request(parameters={}, data=data)
        except HTTPStatusError as e:
            print(f"Error:{e.response.content}")
        parameter = data
        return parameter

    def experiments_list(self):
        # List all experiments
        req = self.api.createRequest("api_experiments_list")
        headers, data, response = req.request(parameters={}, data=None)
        print(headers)
        print(data)
        experiments = data
        return experiments

    def parameters_list(self, experiment):
        # List all parameters
        req = self.api.createRequest("api_parameters_list")
        headers, data, response = req.request(parameters={}, data=None)

        # Filter for parameters of one experiment
        parameters = data
        parameters = [p for p in parameters if p.experiment == experiment.id]
        return parameters

    def experiment_data(self, experiment):
        # Get data
        req = self.api.createRequest("api_experiments_data_retrieve")
        try:
            headers, experiment, response = req.request(parameters={'id': experiment.id}, data=None)
        except ResponseSchemaError:
            pass
        try:
            print(experiment.data_table_json)
            df = pd.read_json(experiment.data_table_json)
            return df
        except:
            print("Failed to read data JSON")
            return -99

    def open_experiment(self, experiment):
        webbrowser.open(experiment.url, new=0, autoraise=True)

    def experiment_update_data(self, experiment, new_measurements):
        # Post data
        req = self.api.createRequest("api_experiments_upload_data_create")
        new_measurements = new_measurements.to_json()
        experiment.data_table_json = new_measurements
        headers, experiment, response = req.request(parameters={'id': experiment.id}, data=experiment)
