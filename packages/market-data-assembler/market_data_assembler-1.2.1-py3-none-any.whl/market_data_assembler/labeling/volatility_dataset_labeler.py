from abc import ABC
from typing import Dict, List

from market_data_assembler.assembling.aggregation_config import AggregationConfigInstance
from market_data_assembler.labeling.dataset_labeler_abstract import BaseDatasetLabeler


class VolatilityDatasetLabeler(BaseDatasetLabeler, ABC):

    def process_window(self, aggregations: List[AggregationConfigInstance]) -> Dict:
        main_aggregation = AggregationConfigInstance.get_main_aggregation(aggregations)
        main_aggregation_list = main_aggregation.ohlc.get_history()
        prediction_window = main_aggregation_list[-self.prediction_window:]
        training_window = main_aggregation_list[:-self.prediction_window]

        training_volatility = self._calculate_volatility(training_window)
        prediction_volatility = self._calculate_volatility(prediction_window)

        return {
            'class_1': 1 if prediction_volatility * 2 <= training_volatility else 0
        }

    @staticmethod
    def _calculate_volatility(window: List[Dict]) -> float:
        highs = [candle['h'] for candle in window]
        lows = [candle['l'] for candle in window]
        return max(highs) - min(lows)
