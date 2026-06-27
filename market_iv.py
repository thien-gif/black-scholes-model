import yfinance as yf
import datetime
from pricer import implied_volatility
import matplotlib.pyplot as plt

ticker = yf.Ticker("AAPL")
exp_date = '2026-07-17'
S = ticker.history(period='1d')['Close'].iloc[-1]
today_date = datetime.date.today()
expiry_date = datetime.datetime.strptime(exp_date,'%Y-%m-%d').date()
days_to_exp = expiry_date - today_date
T = days_to_exp.days / 365
print(f"Apple current price: {S:.2f}")

chain = ticker.option_chain(exp_date)
calls = chain.calls

print(calls[['strike','lastPrice','bid','ask']].head(10))

print(f"Days to expiration: {days_to_exp.days}")
print(f"T in years: {T:.4f}")

r = 0.05
strikes_list =[]
ivs_list = []
for index, row in calls.iterrows():
    K = row["strike"]
    market_price = (row["bid"] + row["ask"])/2
    if market_price == 0:
        continue
    try: 
        iv = implied_volatility(market_price,S,K,T,r, option_type = 'call', tol = 1e-6, max_iter = 100)
    except ValueError:
        continue
    print("Strike: ", K,"implied_volatility: ",iv)
    strikes_list.append(K)
    ivs_list.append(iv)

print(len(calls))

plt.plot(strikes_list, ivs_list)
plt.xlabel("Strike Price")
plt.ylabel("Implied Volatility")
plt.title("AAPL Implied Volatility Skew")
plt.show()
plt.savefig("aapl_iv_skew.png")




