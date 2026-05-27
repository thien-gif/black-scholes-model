# Black-Scholes-model
A Python implementation of the Black-Scholes-Merton model for pricing European call and put options, including all the major Greeks.
## What it does
- Calculate call and put option prices using the Black-Scholes-Merton formula
- Computes the Greeks: Delta, Gamma, Vega, and Theta
- Plots option prices vs stock price using matplotlib
## Inputs
Parameter
S: Current stock price
K: Strike price
T: Time to expiry (in years)
r: Risk-free interest rate
sigma: volatility of the underlying asset
## How to run
bash
pip install numpy scipy matplotlib
python3 pricer.py

## References
- Hull, J. C. *Options, Futures, and Other Derivatives* (8th ed.), Chapters 14 & 18
