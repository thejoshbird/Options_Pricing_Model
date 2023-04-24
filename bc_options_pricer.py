import yfinance as yf
import math

def black_scholes_option(S, K, T, r, sigma, option_type):
    d1 = (math.log(S/K) + (r + sigma**2/2)*T) / (sigma*math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)
    N1 = 0.5 * (1 + math.erf(d1/math.sqrt(2)))
    N2 = 0.5 * (1 + math.erf(d2/math.sqrt(2)))
    if option_type == "call":
        C = S*N1 - K*math.exp(-r*T)*N2
        return C
    elif option_type == "put":
        P = K*math.exp(-r*T)*N2 - S*N1
        return P
    else:
        raise ValueError("Invalid option type. Enter 'call' or 'put'.")

# Stock symbol
symbol = input("Enter the stock symbol: ").upper()

# Current price of the stock

stock = yf.Ticker(symbol)
S = stock.info['regularMarketPreviousClose']

# Current risk-free interest rate
r = yf.Ticker('^TNX').info['regularMarketPrice'] / 100

# Metrics
try:
    K = float(input("Enter the strike price: "))
except ValueError:
    print("Input must be a number!")
    
try:
    T = float(input("Enter the time to expiration in years: "))
except ValueError:
    print("Input must be a number!")

option_type = input("Enter the option type (call or put): ").lower()
    
# Calculating sigma ie standard deviation of a stock over time
hist = stock.history(period="1y")
returns = (hist['Close'] / hist['Close'].shift(1)).apply(math.log)
mean_return = returns.mean()
std_return = returns.std()
sigma = std_return * math.sqrt(252)

# Calculate the value of the option
option_price = black_scholes_option(S, K, T, r, sigma, option_type)

# Print the result
print(f"\nThe price of the {option_type} option for {symbol} is:", option_price)
