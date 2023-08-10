from aiopenapi3 import OpenAPI
import pandas as pd
TOKEN = "67031c6300625373a5a3a0f4576c64592adf1da577a74bf10c8c4ff1315c91e9"
class MHSapiClient:

    def __init__(self, token, dev=False):
        self.token = token
        self.base_url = 'https://matterhorn.studio'
        if dev:
            self.base_url = 'http://localhost:8000/'


        self.api = OpenAPI.load_sync(self.base_url + "api/schema/")
        self.api.authenticate(Authorization=f"Token {TOKEN}")

        if dev:
            operationIds = list(self.api._.Iter(self.api, False))
            print(operationIds)

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
        parameters = [p for p in parameters if p.experiment_id == experiment.id]
        return parameters

    def experiment_data(self, experiment):
        # Get data
        req = self.api.createRequest("api_experiments_data_retrieve")
        headers, experiment, response = req.request(parameters={'id': experiment.id}, data=None)
        try:
            df = pd.read_json(experiment.data_table_json)
            return df
        except:
            print("Failed to read data JSON")
            return -1

    def experiment_update_data(self, experiment, new_measurements):
        # Post data
        req = self.api.createRequest("api_experiments_upload_data_create")
        new_measurements = new_measurements.to_json()
        experiment.data_table_json = new_measurements
        headers, experiment, response = req.request(parameters={'id': experiment.id}, data=experiment)
