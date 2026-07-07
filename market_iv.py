import yfinance as yf
import datetime
from pricer import implied_volatility
import matplotlib.pyplot as plt

def get_implied_vols(ticker_symbol, exp_date, r = 0.05, option_type= 'call'):
    ticker = yf.Ticker(ticker_symbol)
    S = ticker.history(period='1d')['Close'].iloc[-1]
    today_date = datetime.date.today()
    expiry_date = datetime.datetime.strptime(exp_date,'%Y-%m-%d').date()
    days_to_exp = expiry_date - today_date
    T = days_to_exp.days / 365
    print(f"Stock current price: {S:.2f}")
    chain = ticker.option_chain(exp_date)
    if option_type == 'call':
            options = chain.calls
    elif option_type == 'put':
            options = chain.puts
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    

    print(f"Days to expiration: {days_to_exp.days}")
    print(f"T in years: {T:.4f}")
    strikes_list =[]
    ivs_list = []
    for index, row in options.iterrows():
        K = row["strike"]
        market_price = (row["bid"] + row["ask"])/2
        if market_price == 0:
            continue
        try:
            iv = implied_volatility(market_price,S,K,T,r, option_type=option_type, tol=1e-6, max_iter=100)
        except ValueError as e:
            continue

        print(f"Strike: {K} implied_volatility: {iv}")
        strikes_list.append(K)
        ivs_list.append(iv)

    
    print(f"Successful IVs: {len(strikes_list)}")
    plt.plot(strikes_list, ivs_list)
    plt.xlabel("Strike Price")
    plt.ylabel("Implied Volatility")
    plt.title("Implied Volatility Skew")
    plt.show()
    return strikes_list, ivs_list

while(True):
    ticker_symbol = input("Enter your stock: \n").upper()
    exp_date = input("Enter expiration date (YYYY-MM-DD): \n")
    option_type = input("Enter option type: \n")
    try:
        strikes, ivs = get_implied_vols(ticker_symbol,exp_date,r = 0.05, option_type = option_type)
        break
    except (ValueError, IndexError):
        print("Something went wrong. Please check your ticker, date format, or option type.")
 