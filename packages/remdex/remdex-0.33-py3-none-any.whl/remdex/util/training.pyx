from typing import List
from threading import Event
from queue import Queue
from remdex.host import ConnClient, ClientResult, ConnServer, connect_to, Socket
from remdex.util.artifacts import DexError, Params, Metric, Model, Gradients
from remdex.util.general import init_parameters, finish_clients, get_eval
from remdex.util.avg_ops import batch_avg_step, avg_step
from remdex.util.sgd_ops import batch_sgd_step, sgd_step
from pprint import pprint

class FedAvgClient:

    def __setup_add__(self):
        self.__batched__ = False
        self.__server__: ConnServer
        self.__train_q__ = Queue()
        self.__batch_generator__ = None
        self.__batch_ended__ = True
        self.__batched__ = False
        self.__finish_event__ = Event()

    def __train__(self):
        self.train()
        self.__train_q__.put(0)

    def __get_params__(self): 
        self.__train_q__.get()
        if self.__batch_ended__ and self.__batched__:
            return DexError.BATCH_ENDED
        return self.get_params()
    
    def __batch_train__(self):
        try: 
            self.batch_train(next(self.__batch_generator__))
            self.__train_q__.put(0)
        except:
            self.__train_q__.put(0)
            self.__batch_ended__ = True

    def __batch_train_start__(self):
        self.__batched__ = True
        self.__batch_ended__ = False
        self.__batch_generator__ = self.batch_generator()

    def __finish__(self):
        self.__finish_event__.set()

    def __setup_user_methods__(self):
        self.__server__.add('train')(self.__train__) 
        self.__server__.add('get_params')(self.__get_params__)
        self.__server__.add('update_params')(self.update_params)
        self.__server__.add('batch_train')(self.__batch_train__)
        self.__server__.add('batch_train_start')(self.__batch_train_start__)
        self.__server__.add('evaluate')(self.evaluate)
        self.__server__.add('finish')(self.__finish__)
        self.__server__.add('return_models')(self.return_models)

    def __init__(self):
        pass

    def get_params(self,) -> List[Params]:
        pass

    def update_params(self, parameters: List[list]):
        pass

    def train(self, ):
        pass

    def batch_generator(self):
        pass

    def batch_train(self, batch):
        pass

    def save(self,):
        pass

    def evaluate(self,)->List[Metric]:
        pass

    def return_models(self, ) -> List[Model]:
        pass

    def start(self, server_address:str):
        self.__setup_add__()
        [address, port] = server_address.split(':') 
        port = int(port)
        # connect to server address 
        conn = connect_to(address=address, port=port)
        server = ConnServer(sock=conn)
        self.__server__ = server 
        self.__setup_user_methods__()
        self.__finish_event__.wait()


class FedSgdClient:

    def __setup_add__(self):
        self.__batched__ = False
        self.__server__: ConnServer
        self.__gradient_q__ = Queue()
        self.__all_gradients__ = [] 
        self.__batch_data_generator__ = None
        self.__finish_event__ = Event()

    def __get_latest_gradients__(self):
        self.__gradient_q__.get()
        return self.__all_gradients__.pop(0)
    
    def __train__(self):
        #print('trained') 
        self.__all_gradients__.append(self.train())
        self.__gradient_q__.put(0)
        

    def __batch_train_start__(self):
        self.__batch_data_generator__ = self.batch_generator()

    def __batch_train__(self):
        try:
            self.__all_gradients__.append(
                self.batch_train(
                    next(self.__batch_data_generator__)
                )
            )   
            self.__gradient_q__.put(0)
        except:
            self.__all_gradients__.append(DexError.BATCH_ENDED)
            self.__gradient_q__.put(0)

    def __finish__(self):
        self.__finish_event__.set()

    def __setup_user_methods__(self):
        self.__server__.add('train')(self.__train__)
        self.__server__.add('init_parameters')(self.init_parameters)
        self.__server__.add('optimize')(self.optimize)
        self.__server__.add('batch_train')(self.__batch_train__)
        self.__server__.add('get_gradients')(self.__get_latest_gradients__)
        self.__server__.add('batch_train_start')(self.__batch_train_start__)
        self.__server__.add('evaluate')(self.evaluate)
        self.__server__.add('finish')(self.__finish__)
        self.__server__.add('return_models')(self.return_models)

    def __init__(self):
        pass

    def train(self)->List[Gradients]:
        pass
    
    def init_parameters(self, parameters:List[list]):
        pass
    
    def optimize(self, gradients: List[list]):
        pass

    def batch_generator(self):
        pass

    def batch_train(self, batch)->List[Gradients]:
        pass

    def return_models(self, ) -> List[Model]:
        pass

    def evaluate(self,)->List[Metric]:
        pass

    def start(self, server_address:str):
        self.__setup_add__()
        [address, port] = server_address.split(':') 
        port = int(port)
        # connect to server address 
        conn = connect_to(address=address, port=port)
        server = ConnServer(sock=conn)
        self.__server__ = server 
        self.__setup_user_methods__()
        self.__finish_event__.wait()

def retrieve_models(clients:List[ConnClient]):
    print('retrieving models')
    models: List[Model] = clients[0].call('return_models').run().get()
    for m in models:
        print(m.name)
        print(m.model)

def train_avg(
    clients: List[ConnClient],
    epochs: int, 
    batched: bool = False,
    parameters: List[list] = None,
):
    if parameters is not None:
        init_requests: List[ClientResult] = [init_parameters(i, parameters) for i in clients]
        [i.get() for i in init_requests]
    # start training
    for i in range(1,epochs+1):
        if batched:
            #print('batched')
            batch_avg_step(clients, epoch=i, epochs=epochs)
        else:
            #print('not batched')
            avg_step(clients)
            evals = get_eval(clients)
            if evals is not None:
                print(f'Epoch {i}/{epochs}')
                pprint(evals)
                print()
    retrieve_models()
    finish_clients(clients=clients)



def train_sgd(
    clients: List[ConnClient],
    epochs: int, 
    batched: bool = False,
    parameters: List[list] = None,
):
    # init parameters 
    if parameters is not None:
        init_requests: List[ClientResult] = [init_parameters(i, parameters) for i in clients]
        [i.get() for i in init_requests]
    # start training
    for i in range(1, epochs+1):
        if batched:
            #print('batched')
            batch_sgd_step(clients, i, epochs)
        else:
            #print('not batched')
            sgd_step(clients)
            evals = get_eval(clients)
            if evals is not None:
                print(f'Epoch {i}/{epochs}')
                pprint(evals)
                print()
    retrieve_models(clients=clients)
    finish_clients(clients=clients)

class FedAvgServer:

    def __init__(
        self, address:str, epochs:int, 
        num_clients:int, batched=False, 
        init_params: List[list]=None
    ) -> None:
        self.address = address
        self.epochs = epochs
        self.batched = batched
        self.num_clients = num_clients
        [self.ip, port] = address.split(':')
        self.port = int(port)
        self.init_params = init_params

    def start(self, ):
        sock = Socket(address=self.ip, port=self.port)
        clients = [ConnClient(sock.get_incoming()) for i in range(self.num_clients)]
        train_avg(
            clients=clients,
            epochs=self.epochs, 
            batched=self.batched,
            parameters=self.init_params
        )


class FedSgdServer(FedAvgServer):
    def __init__(self, address: str, epochs: int, 
                 num_clients: int, batched=False, 
                 init_params: List[List] = None
        ) -> None:
        super().__init__(address, epochs, num_clients, batched, init_params)

    def start(self):
        sock = Socket(address=self.ip, port=self.port)
        clients = [ConnClient(sock.get_incoming()) for i in range(self.num_clients)]
        train_sgd(
            clients=clients,
            epochs=self.epochs, 
            batched=self.batched,
            parameters=self.init_params
        )
