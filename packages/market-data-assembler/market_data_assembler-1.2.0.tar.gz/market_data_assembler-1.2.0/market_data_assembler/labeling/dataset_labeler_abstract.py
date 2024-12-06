from abc import ABC, abstractmethod
from typing import Dict, List

from market_data_assembler.assembling.aggregation_config import AggregationConfigInstance


class BaseDatasetLabeler(ABC):
    def __init__(self, prediction_window: int):
        self.prediction_window = prediction_window

    def apply(self, aggregations: List[AggregationConfigInstance]) -> Dict:
        labels = self.process_window(aggregations)
        return {'labels': labels}

    @abstractmethod
    def process_window(self, aggregations: List[AggregationConfigInstance]) -> Dict:
        pass
