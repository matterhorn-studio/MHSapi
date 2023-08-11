from MHSapi.src.MHSapi import MHSapi
TOKEN = "67031c6300625373a5a3a0f4576c64592adf1da577a74bf10c8c4ff1315c91e9"

client = MHSapi.MHSapiClient(token=TOKEN, dev=True)
import time
import json
data = {'name_text':f'SDL4Kids_{time.time()}', 'data_table_json':"-"}
#data = json.dumps(data)
experiment = client.experiments_create(data)
print(f"Created:{experiment}")

experiments = client.experiments_list()
assert experiments[0].id == experiment.id
assert experiments[0].name_text == experiment.name_text

for p in ['Red', 'Green', 'Blue', 'Error']:
    new_parameter = {"parameter_text": p, 'experiment':experiment.id}
    new_parameter['lower_bound'] = 255
    new_parameter['upper_bound'] = 255
    new_parameter['reviewed'] = True
    if p == "Error":
        new_parameter["outcome"] = True
    parameter = client.parameters_create(new_parameter)

parameters_list = client.parameters_list(experiment)
print(parameters_list)
data = client.experiment_data(experiment)

new_measurements = data.iloc[0:1]
client.experiment_update_data(experiment, new_measurements)

client.open_experiment(experiment)