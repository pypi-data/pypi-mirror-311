import os
from bisect import bisect_right
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from typing import List, Type, Dict, Any

from market_data_assembler.common.common import generate_date_range, save_compressed_json
from market_data_assembler.loader.book_dept_loader_interface import IBookDeptLoader
from market_data_assembler.loader.ohlc_loader_interface import IOhlcLoader
from market_data_assembler.loader.trades_loader_interface import ITradesLoader


class CryptoSeriesDataProvider:
    raw_series_folder = './out/raw'

    def __init__(self, instruments: List[str], day_from: datetime, day_to: datetime,
                 ohlc_loader_class: Type[IOhlcLoader], trades_loader_class: Type[ITradesLoader],
                 book_depth_loader_class: Type[IBookDeptLoader] = None,
                 max_workers: int = 1):
        self.selected_days = generate_date_range(day_from, day_to)
        self.instruments = instruments
        self.ohlc_loader_class = ohlc_loader_class
        self.trades_loader_class = trades_loader_class
        self.book_depth_loader_class = book_depth_loader_class
        self.max_workers = max_workers
        if not os.path.exists(self.raw_series_folder):
            os.makedirs(self.raw_series_folder)

    def _load_for_day(self, instrument: str, target_day: datetime) -> None:
        file_name = f"{instrument}_{target_day.strftime('%Y-%m-%d')}.parquet"
        instrument_path = os.path.join(self.raw_series_folder, instrument)
        os.makedirs(instrument_path, exist_ok=True)
        archive_path = os.path.join(instrument_path, file_name)

        if os.path.exists(archive_path):
            print(f'{file_name} already exists')
            return

        ohlc_loader = self.ohlc_loader_class(target_day, instrument)
        trades_loader = self.trades_loader_class(target_day, instrument)
        book_depths_loader = self.book_depth_loader_class(target_day, instrument)

        if ohlc_loader.is_exist():
            ohlc_series = ohlc_loader.get_ohlc_series()
            trades = []
            if trades_loader.is_exist():
                trades = trades_loader.get_trades()
                grouped_trades = self._group_trades(trades, target_day)
            else:
                grouped_trades = {}

            updated_series = self._update_ohlc_with_trades(ohlc_series, grouped_trades)
            book_depths = []
            if book_depths_loader.is_exist():
                book_depths = book_depths_loader.get_book_depths()
                grouped_book_depths = self._group_book_depths(book_depths, target_day)
            else:
                grouped_book_depths = {}
            updated_series = self._update_ohlc_with_book_depths(updated_series, grouped_book_depths)

            save_compressed_json(updated_series, archive_path)
            print(
                f'process-{os.getpid()}, time: {datetime.now()}, {instrument}: saved {file_name}, ohlc_series: {len(ohlc_series)}, trades: {len(trades)}, book_depths: {len(book_depths)}')

    def load_raw_series(self) -> None:
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for instrument in self.instruments:
                for target_day in self.selected_days:
                    futures.append(executor.submit(self._load_for_day, instrument, target_day))

            for future in as_completed(futures):
                future.result()

            self._final_report()

    def _final_report(self) -> None:
        instruments = set()

        for name in os.listdir(self.raw_series_folder):
            path = os.path.join(self.raw_series_folder, name)
            if os.path.isdir(path):
                instruments.add(name)

        report_lines = []

        for instrument in instruments:
            available_dates = []
            raw_series = os.path.join(self.raw_series_folder, instrument)
            for file_name in os.listdir(raw_series):
                if file_name.startswith(instrument) and file_name.endswith('.parquet'):
                    date_str = file_name.split('_')[-1].replace('.parquet', '')
                    available_dates.append(datetime.strptime(date_str, '%Y-%m-%d'))

            if available_dates:
                period_from = min(available_dates).strftime('%Y-%m-%d')
                period_to = max(available_dates).strftime('%Y-%m-%d')

                full_date_range = generate_date_range(min(available_dates), max(available_dates))
                missing_days = [
                    day.strftime('%Y-%m-%d') for day in full_date_range
                    if day not in available_dates
                ]

                missing_days_str = f"[{', '.join(missing_days)}]" if missing_days else "[]"
                report_lines.append(f"{instrument}, {period_from} - {period_to}, missed {missing_days_str}")
            else:
                report_lines.append(f"{instrument}, has no raw data")

        print("\n".join(report_lines))

    @staticmethod
    def _update_ohlc_with_trades(ohlc_series: List[dict], grouped_trades: dict) -> List[dict]:
        updated_series = []

        for candle in ohlc_series:
            trade_time = candle['t']
            if trade_time in grouped_trades:
                trades = grouped_trades[trade_time]
                candle['trades'] = trades
                candle['n'] = len(trades)
            else:
                candle['trades'] = []
                candle['n'] = 0

            updated_series.append(candle)

        return updated_series

    @staticmethod
    def _update_ohlc_with_book_depths(ohlc_series: List[dict], book_depths: dict) -> List[dict]:
        updated_series = []

        for candle in ohlc_series:
            trade_time = candle['t']
            if trade_time in book_depths:
                candle['book_depth'] = book_depths[trade_time]
            else:
                candle['book_depth'] = []
            updated_series.append(candle)

        return updated_series

    @staticmethod
    def _group_book_depths(book_depths: List[Dict[str, Any]], selected_date: datetime):
        book_depth_snapshots = defaultdict(list)
        for item in book_depths:
            book_depth_snapshots[item['t']].append(item)

        interval_length = 60000
        start_datetime = selected_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
        end_datetime = start_datetime + timedelta(days=1)
        start_time = int(start_datetime.timestamp() * 1000)
        end_time = int(end_datetime.timestamp() * 1000)
        intervals = list(range(start_time, end_time, interval_length))
        grouped_snapshots = {start: [] for start in intervals}

        for item in book_depth_snapshots:
            depth_time_ms = item
            idx = bisect_right(intervals, depth_time_ms) - 1
            grouped_snapshots[intervals[idx]].append(book_depth_snapshots[item])

        grouped_snapshots = {k: v for k, v in grouped_snapshots.items() if v}

        return grouped_snapshots

    @staticmethod
    def _group_trades(trades: List[Dict[str, Any]], selected_date: datetime):
        interval_length = 60000
        start_datetime = selected_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
        end_datetime = start_datetime + timedelta(days=1)
        start_time = int(start_datetime.timestamp() * 1000)
        end_time = int(end_datetime.timestamp() * 1000)
        intervals = list(range(start_time, end_time, interval_length))
        grouped_trades = {start: [] for start in intervals}

        for trade in trades:
            trade_time_ms = trade['t']
            idx = bisect_right(intervals, trade_time_ms) - 1
            grouped_trades[intervals[idx]].append(trade)

        grouped_trades = {k: v for k, v in grouped_trades.items() if v}

        return grouped_trades
