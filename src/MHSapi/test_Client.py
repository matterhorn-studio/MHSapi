from MHSapi import MHSapiClient
TOKEN = "67031c6300625373a5a3a0f4576c64592adf1da577a74bf10c8c4ff1315c91e9"

client = MHSapiClient(token=TOKEN, dev=True)

experiments = client.experiments_list()
experiment = experiments[0]

parameters_list = client.parameters_list(experiment)

data = client.experiment_data(experiment)

new_measurements = data.iloc[0:1]
client.experiment_update_data(experiment, new_measurements)