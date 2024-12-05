from typing import List
from remdex.host import ConnClient
from remdex.util.artifacts import Gradients, DexError
from remdex.util.calculations import multiply_gradients,add_gradient_weighted, divide_gradients
from remdex.util.general import get_eval
from pprint import pprint

def get_summed_gradients(clients: List[ConnClient]):
    # get latest gradients
    weights = []
    grads = None
    for c in clients:
        recv_grads: List[Gradients] = c.call('get_gradients').run().get()
        # skip if none
        if recv_grads == DexError.BATCH_ENDED:
            continue
        if grads == None:
            grads = []
            for idx, rg in enumerate(recv_grads, 0):
                weights.insert(idx, rg.weight)
                grads.insert(idx,multiply_gradients(rg.gradients, rg.weight))
            continue
        # normal situation
        for idx, rg in enumerate(recv_grads, 0):
            weights[idx] += rg.weight
            grads[idx] = add_gradient_weighted(grads[idx], rg.gradients, rg.weight)

    return weights, grads

def sgd_optimize(grads:List[list], clients: List[ConnClient]):
    for c in clients:
        c.call('optimize').run(grads).get()

def sgd_step_update(clients: List[ConnClient]):
    # get gradients
    weights, grads = get_summed_gradients(clients)
    # check if nothing is received
    if grads is None:
        return False
    # get average gradients
    avg_grads = []
    for w, g in zip(weights, grads):
        avg_grads.append(divide_gradients(g, w))
    # optimize
    sgd_optimize(avg_grads, clients)
    return True

def sgd_step(clients: List[ConnClient]):
    # train
    train_requests = [
        c.call('train').run() for c in clients
    ]
    sgd_step_update(clients=clients)

def batch_sgd_step(clients: List[ConnClient], epoch:int, epochs:int):
    # start training first 
    start_requests = [c.call('batch_train_start').run() for c in clients]
    [s.get() for s in start_requests]
    can_continue = True
    batch_position = 1
    # run steps 
    while can_continue:
        train_requests = [
            c.call('batch_train').run() for c in clients
        ]
        [t.get() for t in train_requests]
        can_continue = sgd_step_update(clients)
        # evaluate model
        if can_continue:
            evals = get_eval(clients)
            if evals is not None:
                print(f'Epoch {epoch}/{epochs} Batch:{batch_position}')
                pprint(evals)
                print()
        batch_position+=1