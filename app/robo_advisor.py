import requests
import json
import datetime

#Info Inputs

request_url ="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
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

for target_list in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
recent_high = max(high_prices)
#breakpoint()




#Info Outputs


print("-------------------------")
print("SELECTED SYMBOL: XYZ")
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
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")