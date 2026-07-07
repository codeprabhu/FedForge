from app.aggregation.strategies.fedavg_strategy import FedAvgStrategy
class AggregationRegistry:
    def __init__(self):
        self._strategies = {"fedavg" : FedAvgStrategy}

    def get(self, name: str):
        if name not in self._strategies:
            raise ValueError(f"Unknown Aggregation Strategy: {name}")

        return self._strategies