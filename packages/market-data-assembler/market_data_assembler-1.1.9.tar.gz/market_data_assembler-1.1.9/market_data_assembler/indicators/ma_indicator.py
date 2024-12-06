from market_data_assembler.indicators.indicator_abstract import BaseIndicator


class MovingAverageIndicator(BaseIndicator):

    def calculate(self):
        return [candle['c'] for candle in self.candles]
