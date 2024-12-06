from abc import ABC, abstractmethod
from typing import Dict, List


class BaseIndicator(ABC):
    def __init__(self, window_length: int, history_size: int):
        self.history_size = history_size
        self.window_length = window_length
        self.candles: List[Dict] = []
        self.history: List[float] = []

    def apply(self, candle: Dict):
        if not self.candles:
            self.candles.append(candle)
            value = self._calculate_value()
            self.history.append(value)
            return

        if candle['t'] == self.candles[-1]['t']:
            self.candles[-1] = candle
            self.history[-1] = self._calculate_value()
            return

        self.candles.append(candle)
        if len(self.candles) > self.window_length:
            self.candles.pop(0)
        self.history.append(self._calculate_value())
        if len(self.history) > self.history_size:
            self.history.pop(0)

    def is_ready(self):
        return len(self.history) == self.history_size

    def get_history(self):
        return self.history

    def _calculate_value(self) -> float:
        calculated_values = self.calculate()
        smoothed_value = sum(calculated_values) / len(calculated_values) if len(calculated_values) > 0 else 0

        return smoothed_value

    @abstractmethod
    def calculate(self) -> List[float]:
        pass
