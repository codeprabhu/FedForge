from exceptions.unknown_model_error import UnknownModelError

class ModelRegistry:
    def __init__(self):
        self._models={}

    def register(self, name, model_class):
        self._models[name] = model_class
    
    def get(self,name):
        if name not in self._models:
            raise UnknownModelError("Unknown Model: {name}")
        
        return self._models[name]