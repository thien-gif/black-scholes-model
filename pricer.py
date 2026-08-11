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

def bs_price(S,K,T,r,sigma, option_type='call'):
    if option_type == 'call':
        return bs_call(S,K,T,r,sigma)
    elif option_type == 'put':
        return bs_put(S,K,T,r,sigma)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

#Newton's method, x_n+1 = x_n - f(x_n)/f'(x_n)
def implied_volatility(market_price, S, K , T, r, option_type='call', tol=1e-6, max_iter=100):
    sigma = 0.2 #initial guess, 20% is a reasonable starting point for most equities
    for i in range(max_iter):
        price = bs_price(S,K,T, r, sigma, option_type)
        v = vega(S,K, T,r, sigma) #f'(x_n)
        if abs(v)< 1e-10:
            raise ValueError("Vega near Zero, Newton-Raphson unstable")
        diff = price - market_price
        if(abs(diff)< tol):
            return sigma
        sigma = sigma - diff / v
    raise ValueError(f"did not converge after {max_iter} iterations")

def pnl_approximation(S,K,T, r, sigma, delta_S, delta_sigma, option_type = 'call'):
    g = gamma(S,K,T,r,sigma)
    v = vega(S,K,T,r,sigma)
    if (option_type == 'call'):
        d = delta_call(S, K, T, r, sigma)
    elif(option_type == 'put'):
        d = delta_put(S, K, T, r, sigma)
    pnl = d * delta_S + (g/2)*(delta_S)**2+ v*delta_sigma
    return pnl

if __name__ == "__main__":
    pnl = pnl_approximation(100, 100, 0.25, 0.05, 0.2, 5, 0.01)
    print(f"Estimated P&L: {pnl:.4f}")



    