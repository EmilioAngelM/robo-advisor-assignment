import os 
import requests
import json
import datetime
import csv
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame
load_dotenv()

#Info Inputs
api_key = os.environ.get("AA_API_KEY")
ticker = input("Please input the stock ticker: ")




request_url =f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
response = requests.get(request_url)

#Validation
if type(ticker) == int:
    print("OOPS, wrong ticker. Please input a valid stock ticker!")
    exit()
if len(ticker) <1:
    print("OOPS, wrong ticker. Please input a valid stock ticker!")
    exit()
if len(ticker) > 5:
    print("OOPS, wrong ticker. Please input a valid stock ticker!")
    exit()
if "Error Message" in response.text: ##Miguel Castillo helped me think about this part of validation
    print("OOPS, wrong ticker. Please input a valid stock ticker!")
    exit()

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

with open(csv_file_path, "w") as csv_file: 
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() 
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp":date, 
            "open":daily_prices["1. open"],
            "high":daily_prices["2. high"],
            "low":daily_prices["3. low"],
            "close":daily_prices["4. close"],
            "volume":daily_prices["5. volume"],
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


if float(daily_prices["4. close"]) < 1.2*float(daily_prices["4. close"]):
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

#line chart 

for date in dates:
    daily_prices = tsd[date]
    line_data = [
        {"date": date, "stock_price_usd": daily_prices["4. close"]},
    #{"date": "2020-10-02", "stock_price_usd": 101.01},
    #{"date": "2020-10-03", "stock_price_usd": 120.20},
    #{"date": "2020-10-04", "stock_price_usd": 107.07},
    #{"date": "2020-10-05", "stock_price_usd": 142.42},
    #{"date": "2020-10-06", "stock_price_usd": 135.35},
    #{"date": "2020-10-07", "stock_price_usd": 160.60},
    #{"date": "2020-10-08", "stock_price_usd": 162.62},
    ]
#print(line_data) 

# initialize a new df object with our custom data
line_df = DataFrame(line_data)
#print(type(line_df))
line_df.head()
sns.lineplot(data=line_df, x="date", y="stock_price_usd")
plt.show()


