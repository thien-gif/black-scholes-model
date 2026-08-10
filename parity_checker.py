import pandas as pd
import yfinance as yf
import numpy as np      
import datetime     

def get_basic(ticker_symbol,exp_date, r = 0.05):
    ticker = yf.Ticker(ticker_symbol)
    S = ticker.history(period='1d')['Close'].iloc[-1]
    today = datetime.date.today()
    expiry = datetime.datetime.strptime(exp_date,'%Y-%m-%d').date()
    days_to_exp = expiry - today
    T = days_to_exp.days /365
    print(f"Current stock price: {S:.2f}")
    chain = ticker.option_chain(exp_date)
    calls = chain.calls
    puts = chain.puts

    diffs = []
    violations = []

    for index, call_row in calls.iterrows():
        K = call_row['strike']
        if K < 0.7 * S or K > 1.3 * S:
            continue
        market_callPrice = (call_row["bid"] + call_row["ask"])/2
        if market_callPrice == 0:
            continue
        match_puts = puts[puts['strike'] == K]
        if match_puts.empty:
            continue
        put_row = match_puts.iloc[0]
        market_putPrice = (put_row["bid"] + put_row["ask"])/2
        if market_putPrice == 0:
            continue
        left = market_callPrice - market_putPrice
        right = S - K*np.exp(-r * T)
        diff = left - right
        diffs.append(diff)
        if abs(diff) > 1.0:
            violations.append(K)
        print(f"K: {K} C: {market_callPrice:.2f} P: {market_putPrice:.2f} Difference: {diff:.4f}")

    print(f"\n--- Summary ---")
    print(f"Strikes checked: {len(diffs)}")
    print(f"Average difference: {np.mean(diffs):.4f}")
    print(f"Max violation: {max(diffs, key=abs):.4f}")
    print(f"Strikes violating parity (diff > $1): {violations}")
            


        
while(True):
    ticker_symbol = input("Enter your stock: \n").upper()
    exp_date = input("Enter expiration date (YYYY-MM-DD): \n")
    get_basic(ticker_symbol,exp_date)
    break
    





