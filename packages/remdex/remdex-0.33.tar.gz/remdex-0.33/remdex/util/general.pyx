from typing import List
from remdex.host import ConnClient
from remdex.util.artifacts import Model, Metric

def init_parameters(
    client:ConnClient, 
    parameters: List[list]
):
    return client.call('init_parameters').run(
        parameters = parameters
    )

def save_model(model:Model):
    try:
        model.model.save(model.name)
    except:
        import torch
        torch.save(model.model.state_dict(), f'{model.name}.pth')

def return_models(clients:List[ConnClient], ):
    models: List[Model] = clients[0].call('return_models').run().get()
    if models is None: return
    # save the models
    for m in models:
        save_model(m)

def finish_clients(clients: List[ConnClient]):
    r = [c.call('finish').run() for c in clients]

def compute_eval(evals:List[Metric]):
    values = dict()
    weights = dict()
    for i in evals:
        if i is None:continue
        for e in i:
            try:
                values[e.name] += e.value * e.weight
                weights[e.name] += e.weight
            except:
                values[e.name] = e.value * e.weight
                weights[e.name] = e.weight

    for k in values.keys():
        values[k] = values[k] / weights[k]

    if len([k for k in values.keys()]) == 0:
        return None
    
    return values
            

def get_eval(clients: List[ConnClient]):
    evals = [c.call('evaluate').run() for c in clients]
    evals = [ e.get() for e in evals ]
    evals:List[Metric] = evals
    computed_eval = compute_eval(evals=evals)
    if computed_eval is None:
        return 
    return computed_eval


