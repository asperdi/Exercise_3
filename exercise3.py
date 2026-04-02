import yfinance as yf
import pandas as pd
import numpy as np

def find_crossovers():
    btc_data = yf.download('BTC-USD', start='2024-01-01', end='2025-11-20', auto_adjust=False)

    btc_data['50-day MA'] = btc_data['Close'].rolling(window=50).mean()
    btc_data['200-day MA'] = btc_data['Close'].rolling(window=200).mean()

    diff = btc_data['50-day MA'] - btc_data['200-day MA']

    crossover_dates = []

    for i in range(1, len(diff)):
        if pd.notna(diff.iloc[i-1]) and pd.notna(diff.iloc[i]):
            if diff.iloc[i-1] < 0 and diff.iloc[i] > 0:
                date = btc_data.index[i].strftime('%Y-%m-%d')
                crossover_dates.append(date)

    return crossover_dates


def calculate_total_btc_traded():
    btc_data = yf.download('BTC-USD', start='2024-01-01', end='2025-11-20', auto_adjust=False)

    btc_data['BTC_traded'] = btc_data['Volume'] / btc_data['Close']

    max_btc = btc_data['BTC_traded'].max()

    return int(max_btc)


if __name__ == '__main__':
    crossover_dates = find_crossovers()
    total_traded = calculate_total_btc_traded()
    
    print(" ".join(crossover_dates))
    print(total_traded)
