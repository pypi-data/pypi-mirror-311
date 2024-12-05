from typing import List
from remdex.host import ConnClient
from remdex.util.artifacts import Params, DexError
from remdex.util.calculations import multiply_gradients, add_gradient_weighted, divide_gradients
from remdex.util.general import get_eval
from pprint import pprint


def get_summed_params(clients: List[ConnClient]):
    # get latest paramms
    weights = []
    params = None
    for c in clients:
        recv_params: List[Params] = c.call('get_params').run().get()
        # skip if none
        if recv_params == DexError.BATCH_ENDED:
            continue
        if params == None:
            params = []
            for idx, rg in enumerate(recv_params, 0):
                weights.insert(idx, rg.weight)
                params.insert(idx,multiply_gradients(rg.params, rg.weight))
            continue
        # normal situation
        for idx, rg in enumerate(recv_params, 0):
            weights[idx] += rg.weight
            params[idx] = add_gradient_weighted(params[idx], rg.params, rg.weight)

    return weights, params


def avg_update_params(params, clients: List[ConnClient]):
    for c in clients:
        c.call('update_params').run(params).get()

def avg_step_update(clients: List[ConnClient]):
    # get parameters
    weights, params = get_summed_params(clients)
    # check if nothing is received
    if params is None:
        return False
    # get average parameters
    avg_params = []
    for w, g in zip(weights, params):
        avg_params.append(divide_gradients(g, w))
    # optimize
    avg_update_params(avg_params, clients)
    return True

def avg_step(clients: List[ConnClient]):
    # train
    trains = [ c.call('train').run() for c in clients]
    [t.get() for t in trains]
    
    avg_step_update(clients)

def batch_avg_step(clients: List[ConnClient], epoch:int, epochs:int):
    starts = [c.call('batch_train_start').run() for c in clients]
    [s.get() for s in starts]
    can_continue = True
    batch_position = 1
    while can_continue:
        trains = [ c.call('batch_train').run() for c in clients]
        [t.get() for t in trains]
        can_continue = avg_step_update(clients=clients)
        # evaluate model
        if can_continue:
            evals = get_eval(clients)
            if evals is not None:
                print(f'Epoch {epoch}/{epochs} Batch:{batch_position}')
                pprint(evals)
                print()
        batch_position+=1