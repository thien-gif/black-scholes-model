# Black-Scholes-model
A Python implementation of the Black-Scholes-Merton model for pricing European call and put options, including all the major Greeks.
## What it does
- Calculate call and put option prices using the Black-Scholes-Merton formula
- Computes the Greeks: Delta, Gamma, Vega, and Theta
- Plots option prices vs stock price using matplotlib
## Inputs
Parameter:
- S: Current stock price
- K: Strike price
- T: Time to expiry (in years)
- r: Risk-free interest rate
- sigma: volatility of the underlying asset
## How to run
bash
pip install numpy scipy matplotlib
python3 pricer.py

## Key Findings
When computing implied volatility across strikes for AAPL and TSLA (expiration 2026-08-21), 
two distinct volatility patterns emerged:

- **AAPL** displays an upward volatility skew — implied volatility increases steadily as strike price rises. This suggests the market prices higher uncertainty into OTM call options, possibly reflecting demand for upside exposure.

- **TSLA** displays a volatility smile — IV is elevated on both ends and dips near the at-the-money strike (~$400). This is consistent with TSLA's reputation as a high-volatility stock where traders buy both OTM puts (downside protection) and OTM calls (speculative upside bets).

These patterns confirm that implied volatility is not constant across strikes — a direct violation of BSM's assumption of constant volatility.

## References
- Hull, J. C. *Options, Futures, and Other Derivatives* (8th ed.), Chapters 14 & 18
