"""
data/fetcher.py — 歷史股價下載與快取
職責：從 Yahoo Finance 取得 OHLCV 數據，並在本地快取以避免重複請求
"""

import os
import pandas as pd
import yfinance as yf

from config import TICKER, START_DATE, END_DATE, DATA_CACHE_DIR


def fetch_price_data(
    ticker: str = TICKER,
    start: str = START_DATE,
    end: str = END_DATE,
    cache_dir: str = DATA_CACHE_DIR,
) -> pd.DataFrame:
    """
    下載或讀取快取的股價數據。

    回傳欄位：Date (index), Open, High, Low, Close, Volume
    """
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f"{ticker}_{start}_{end}.csv")

    if os.path.exists(cache_path):
        print(f"[Fetcher] 讀取快取：{cache_path}")
        df = pd.read_csv(cache_path, index_col="Date", parse_dates=True)
        return df

    print(f"[Fetcher] 下載 {ticker} 數據（{start} ~ {end}）...")
    raw = yf.download(ticker, start=start, end=end, progress=False)

    if raw.empty:
        raise ValueError(f"無法取得 {ticker} 的數據，請確認股票代號與日期區間。")

    df = raw[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.index.name = "Date"

    df.to_csv(cache_path)
    print(f"[Fetcher] 已快取至：{cache_path}")

    return df
