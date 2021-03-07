import os 
import requests
import json
import datetime
import csv
from dotenv import load_dotenv

load_dotenv()

#Info Inputs
api_key = os.environ.get("AA_API_KEY")
ticker = input("Please input the stock ticker: ")

#if type(ticker) == int or float:
#    print("OOPS, wrong ticker. Please input a valid stock ticker!")
#    exit()
if len(ticker) <1:
    print("OOPS, wrong ticker. Please input a valid stock ticker!")
    exit()
if len(ticker) > 5:
    print("OOPS, wrong ticker. Please input a valid stock ticker!")
    exit()



request_url =f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
response = requests.get(request_url)

#print(type(response))
#print(response.status_code)
#print(response.text)

parsed_response = json.loads(response.text)


last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
request_at = str(datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"))
tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys())
latest_day = dates[0]
latest_close = tsd[latest_day]["4. close"]

def to_usd(my_price):
    return f"${my_price:,.2f}" 

#max of all high prices

#get the high price from each day
high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)
#breakpoint()





#Info Outputs

#Info outputs

#csv_file_path = "data/prices.csv" # a relative filepath
csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

#csv_file_path = os.path.join(os.path.dirname(__file__), "..\data\prices.csv")

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date, 
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"],
            })

     
  
print("-------------------------")
print(f"SELECTED SYMBOL: {ticker}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
#print("REQUEST AT: 2018-02-20 02:00pm")
print("Request AT: "+request_at)
print("-------------------------")
#print("LATEST DAY: 2018-02-20")
print(f"LATEST DAY: {last_refreshed}")
#print("LATEST CLOSE: $100,000.00")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
#print("RECENT HIGH: $101,000.00")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
#print("RECENT LOW: $99,000.00")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")

#figure out the 20% above thing
if daily_prices["4. close"] < (daily_prices["4. close"]):
    print("RECOMMENDATION: BUY!")
    print("RECOMMENDATION REASON: The latest closing price is less than 120% of the recent low price")
else:
    print("RECOMMENDATION: DON'T BUY!")
    print("RECOMMENDATION REASON: The latest closing price is not less than 120% of the recent low price")
print("-------------------------")
#print("WRITING DATA TO CSV")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


