class DexError:
    BATCH_ENDED = 'BATCHENDEDBATCHENDED'

class Metric:
    def __init__(self, name:str, value, weight:float = 1.0) -> None:
        self.name = name
        self.value = value
        self.weight = weight

class Params:
    def __init__(self, params, weight: float = 1.0) -> None:
        self.params = params
        self.weight = weight

class Gradients:
    def __init__(self, gradients, weight: float = 1.0) -> None:
        self.gradients = gradients
        self.weight = weight

class Model:
    def __init__(self, model, name:str) -> None:
        self.model = model
        self.name = name