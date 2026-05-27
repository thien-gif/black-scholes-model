import numpy as np
from scipy.stats import norm

def cal_d1(S, K , T, r, sigma):
    return (np.log(S/K) + (r + 0.5 * sigma ** 2)*T)/(sigma * np.sqrt(T))

def cal_d2(S, K, T, r, sigma):
    return cal_d1(S, K , T , r, sigma) - (sigma * np.sqrt(T))

def bs_call(S, K, T, r, sigma):
    d1 = cal_d1(S, K, T, r, sigma)
    d2 = cal_d2(S, K, T, r, sigma)
    return S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)

def bs_put(S, K, T, r, sigma):
    d1 = cal_d1(S, K, T, r, sigma)
    d2 = cal_d2(S, K, T, r, sigma)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# measures stock price
def delta_call(S, K, T, r, sigma):
    d1 = cal_d1(S, K, T, r, sigma)
    return norm.cdf(d1)
def delta_put(S, K, T, r, sigma):
    d1 = cal_d1(S, K, T, r, sigma)
    return norm.cdf(d1) - 1

# measures how is the delta changing
def gamma(S, K, T, r, sigma):
    d1 = cal_d1(S, K, T, r, sigma)
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))
# Δ option price when volatility moves by 1%
def vega(S, K, T, r, sigma):
    d1 = cal_d1(S, K, T, r, sigma)
    return S * np.sqrt(T)*norm.pdf(d1)

# measures options loses in value in one day
def theta_call(S, K, T, r, sigma):
    d1 = cal_d1(S, K, T, r, sigma)
    d2 = cal_d2(S, K, T, r, sigma)
    term1 = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
    term2 = r * K * np.exp(-r * T) * norm.cdf(d2)
    return (term1 - term2) / 365

def theta_put(S, K, T, r, sigma):
    d1 = cal_d1(S, K, T, r, sigma)
    d2 = cal_d2(S, K, T, r, sigma)
    term1 = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
    term2 = r * K * np.exp(-r * T) * norm.cdf(-d2)
    return (term1 + term2) / 365



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    # Example inputs
    S = 100      # current stock price
    K = 100      # strike price
    T = 1        # time to expiry in years
    r = 0.05     # risk-free rate
    sigma = 0.2  # volatility

    print("=" * 40)
    print("   BLACK-SCHOLES OPTIONS PRICER")
    print("=" * 40)
    print(f"  Stock Price (S):   ${S}")
    print(f"  Strike Price (K):  ${K}")
    print(f"  Time to Expiry:    {T} year")
    print(f"  Risk-Free Rate:    {r*100}%")
    print(f"  Volatility:        {sigma*100}%")
    print("=" * 40)

    print("\n  PRICES")
    print(f"  Call Price:  ${bs_call(S, K, T, r, sigma):.4f}")
    print(f"  Put Price:   ${bs_put(S, K, T, r, sigma):.4f}")

    print("\n  GREEKS")
    print(f"  Delta (call):  {delta_call(S, K, T, r, sigma):.4f}")
    print(f"  Delta (put):   {delta_put(S, K, T, r, sigma):.4f}")
    print(f"  Gamma:         {gamma(S, K, T, r, sigma):.4f}")
    print(f"  Vega:          {vega(S, K, T, r, sigma):.4f}")
    print(f"  Theta (call):  {theta_call(S, K, T, r, sigma):.4f}")
    print(f"  Theta (put):   {theta_put(S, K, T, r, sigma):.4f}")
    print("=" * 40)

    stock_prices = np.linspace(50, 150, 200)

    call_prices = [bs_call(s, K, T, r, sigma) for s in stock_prices]
    put_prices  = [bs_put(s, K, T, r, sigma)  for s in stock_prices]

    plt.figure(figsize=(10, 6))
    plt.plot(stock_prices, call_prices, label="Call Price", color="blue")
    plt.plot(stock_prices, put_prices,  label="Put Price",  color="red")

    plt.axvline(x=K, color="gray", linestyle="--", label="Strike Price (K)")
    plt.axhline(y=0, color="black", linestyle="-", linewidth=0.5)

    plt.title("Black-Scholes Option Prices vs Stock Price")
    plt.xlabel("Stock Price (S)")
    plt.ylabel("Option Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()