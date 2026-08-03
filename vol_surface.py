import yfinance as yf
import datetime
from pricer import implied_volatility
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

ticker = yf.Ticker("AAPL")
firstSix = ticker.options[:6]
print(firstSix)
all_strikes = []
all_expiries = []
all_ivs = []
S = ticker.history(period='1d')['Close'].iloc[-1]
r = 0.05
option_type = 'call'

expirations = [
    '2026-08-21',
    '2026-09-18',
    '2026-10-16',
    '2026-12-18',
    '2027-03-19',
    '2027-09-17'
]

for exp_date in expirations:

    today_date = datetime.date.today()
    expiry_date = datetime.datetime.strptime(exp_date,'%Y-%m-%d').date()
    days_to_exp = expiry_date - today_date
    T = days_to_exp.days / 365
    chain = ticker.option_chain(exp_date)
    options = chain.calls
    for index, row in options.iterrows():
        K = row["strike"]
        market_price = (row["ask"] + row["bid"])/2
        if market_price == 0:
            continue
        try:
            iv = implied_volatility(market_price,S,K,T,r, option_type=option_type, tol=1e-6, max_iter=100)
        except ValueError as e:
            continue
        all_strikes.append(K)
        all_expiries.append(T)
        all_ivs.append(iv)

print(f"Total successful IVs: {len(all_ivs)}")

# print(ticker.options)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_trisurf(all_strikes, all_expiries, all_ivs, cmap='viridis')
ax.set_xlabel("Strike Price")
ax.set_ylabel("Time to Expiry (years)")
ax.set_zlabel("Implied Volatility")
plt.title("AAPL Volatility Surface")
plt.colorbar(surf, ax=ax, label='Implied Volatility')
plt.savefig("aapl_vol_surface.png", dpi=150, bbox_inches='tight')
plt.show()