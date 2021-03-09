import os 
import requests
import json
import datetime
import csv
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame
from pandas import read_csv
load_dotenv()

#apikey reference
api_key = os.environ.get("AA_API_KEY")
#Info Inputs
stock_or_crypto = input("Would you like to search for a stock or for a cryptocurrency(Stock or Crypto)?: ")




if stock_or_crypto == "Stock":
    ticker = input("Please input a stock or cryptocurrency ticker: ")
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
    


    parsed_response = json.loads(response.text)


    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
    request_at = str(datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"))
    tsd = parsed_response["Time Series (Daily)"]
    dates = list(tsd.keys())
    latest_day = dates[0]
    latest_close = tsd[latest_day]["4. close"]

    def to_usd(my_price):
        return f"${my_price:,.2f}" 

    #max of all high prices and mins of all low prices

    #get the high price and low price from each day
    high_prices = []
    low_prices = []

    for date in dates:
        high_price = tsd[date]["2. high"]
        high_prices.append(float(high_price))
        low_price = tsd[date]["3. low"]
        low_prices.append(float(low_price))

    recent_high = max(high_prices)
    recent_low = min(low_prices)


    #Info outputs


    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")



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
                "volume":daily_prices["5. volume"]
                })

    

    print("-------------------------")
    print(f"SELECTED SYMBOL: {ticker}")
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    
    print("Request AT: "+request_at)
    print("-------------------------")
    
    print(f"LATEST DAY: {last_refreshed}")
   
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
   
    print(f"RECENT HIGH: {to_usd(float(recent_high))}")
   
    print(f"RECENT LOW: {to_usd(float(recent_low))}")
    print("-------------------------")


    if float(latest_close) < 1.2*float(recent_low):
        print("RECOMMENDATION: BUY!")
        print("RECOMMENDATION REASON: The latest closing price is less than 120% of the recent low price")
    else:
        print("RECOMMENDATION: DON'T BUY!")
        print("RECOMMENDATION REASON: The latest closing price is not less than 120% of the recent low price")
    print("-------------------------")
    
    print(f"WRITING DATA TO CSV: {csv_file_path}...")
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")



    #line chart 

    line_df = read_csv(csv_file_path)
    line_df.sort_values(by="timestamp", ascending=True, inplace=True)
    sns.lineplot(data=line_df, x="timestamp", y="close")
    plt.xlabel("Date", fontsize=15)
    plt.ylabel("Closing Price in USD", fontsize=15)
    plt.title(f"{ticker} Closing Price Over 100 Days", fontsize=20)
    plt.xticks(rotation=90,horizontalalignment="right",fontsize=5) #Miguel Castillo explained to me the xticks function
    plt.show()

elif stock_or_crypto == "Crypto":
        ticker = input("Please input a stock or cryptocurrency ticker: ")
        request_url=f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={ticker}&market=CNY&apikey={api_key}"
        response = requests.get(request_url)

        #Validation
        if type(ticker) == int:
            print("OOPS, wrong ticker. Please input a valid crypto ticker!")
            exit()
        if len(ticker) <1:
            print("OOPS, wrong ticker. Please input a valid crypto ticker!")
            exit()
        if len(ticker) > 5:
            print("OOPS, wrong ticker. Please input a valid crypto ticker!")
            exit()
        if "Error Message" in response.text: ##Miguel Castillo helped me think about this part of validation
            print("OOPS, wrong ticker. Please input a valid crypto ticker!")
            exit()
        
   

        parsed_response = json.loads(response.text)


        last_refreshed = parsed_response["Meta Data"]["6. Last Refreshed"]
        request_at = str(datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"))
        tsd = parsed_response["Time Series (Digital Currency Daily)"]
        dates = list(tsd.keys())
        latest_day = dates[0]
        latest_close = tsd[latest_day]["4b. close (USD)"]

        def to_usd(my_price):
            return f"${my_price:,.2f}" 

        #max of all high prices and mins of all low prices

        #get the high price and low price from each day
        high_prices = []
        low_prices = []

        for date in dates:
            high_price = tsd[date]["2b. high (USD)"]
            high_prices.append(float(high_price))
            low_price = tsd[date]["3b. low (USD)"]
            low_prices.append(float(low_price))

        recent_high = max(high_prices)
        recent_low = min(low_prices)
        

        #Info outputs

        
        csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
        csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

        

        with open(csv_file_path, "w") as csv_file: 
            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
            writer.writeheader() 
            for date in dates:
                daily_prices = tsd[date]
                writer.writerow({
                    "timestamp":date, 
                    "open":daily_prices["1b. open (USD)"],
                    "high":daily_prices["2b. high (USD)"],
                    "low":daily_prices["3b. low (USD)"],
                    "close":daily_prices["4b. close (USD)"],
                    "volume":daily_prices["5. volume"]
                    })

        

        print("-------------------------")
        print(f"SELECTED SYMBOL: {ticker}")
        print("-------------------------")
        print("REQUESTING STOCK MARKET DATA...")
        
        print("Request AT: "+request_at)
        print("-------------------------")
        
        print(f"LATEST DAY: {last_refreshed}")
        
        print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
        
        print(f"RECENT HIGH: {to_usd(float(recent_high))}")
        
        print(f"RECENT LOW: {to_usd(float(recent_low))}")
        print("-------------------------")


        if float(latest_close) < 1.2*float(recent_low):
            print("RECOMMENDATION: BUY!")
            print("RECOMMENDATION REASON: The latest closing price is less than 120% of the recent low price")
        else:
            print("RECOMMENDATION: DON'T BUY!")
            print("RECOMMENDATION REASON: The latest closing price is not less than 120% of the recent low price")
        print("-------------------------")
    
        print(f"WRITING DATA TO CSV: {csv_file_path}...")
        print("-------------------------")
        print("HAPPY INVESTING!")
        print("-------------------------")



        #line chart 

        line_df = read_csv(csv_file_path)
        line_df.sort_values(by="timestamp", ascending=True, inplace=True)
        sns.lineplot(data=line_df, x="timestamp", y="close")
        plt.xlabel("Date", fontsize=15)
        plt.ylabel("Closing Price in USD", fontsize=15)
        plt.title(f"{ticker} Closing Price Over Time", fontsize=20)
        plt.xticks(rotation=90,horizontalalignment="right",fontsize=5) #Miguel Castillo explained to me the xticks function
        plt.show()

else:
    print("Invalid Input. Please choose either 'Stock' or 'Crypto.'")
    exit()

