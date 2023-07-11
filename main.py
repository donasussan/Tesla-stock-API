import random

import requests
import pytz
import os
from twilio.rest import Client
import datetime
import math
from datetime import datetime, timedelta

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
TWILIO_SID = "AC643d14847fd604250d043b17b48a6112"
TWILIO_AUTH_TOKEN = "58a3bbbc91f3e8d85b076c75efa35e00"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

#TODO 2. - Get the day before yesterday's closing stock price

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation


    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
parameters_stock = {
    "function":"TIME_SERIES_DAILY_ADJUSTED",
    "symbol": "TSLA",
    "apikey": "1M5P75X440FXD72F"
}
response_stock = requests.get(url="https://www.alphavantage.co/query", params=parameters_stock)
data = response_stock.json()

us_time_zone = pytz.timezone('US/Eastern')
us_datetime = datetime.now(us_time_zone)
#today_date = us_datetime.date()
today_date = '2023-07-07'
#print(today_date)
yesterday = us_datetime - timedelta(days=1)
# Extract the date from the datetime object
#yesterday_date = yesterday.date()
yesterday_date = '2023-07-06'
#print(yesterday_date)

day_before = yesterday - timedelta(days=1)
#day_before_date = day_before.date()
day_before_date = '2023-07-05'
#print(day_before_date)

yesterday_stock_data = float(data["Time Series (Daily)"][f"{yesterday_date}"]["4. close"])
print("Yesterdays closing price:", yesterday_stock_data)
day_before_stock_data = float(data["Time Series (Daily)"][f"{day_before_date}"]["4. close"])
print("Day-before's closing price:", day_before_stock_data)
increment=0
difference = yesterday_stock_data-day_before_stock_data
if difference > 0:
   increment = ((yesterday_stock_data - day_before_stock_data) / day_before_stock_data) * 100
   increment= round(increment, 2)
   print("The increment is" ,increment, "%")

decrement = 0
if difference < 0:
   decrement = ((day_before_stock_data - yesterday_stock_data) / day_before_stock_data) * 100
   decrement = round(decrement, 2)
   print("The decrement is",decrement,"%")
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").


    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 


if increment>0.2:

    parameters_news = {
        "q": "Tesla",
        "sortBy": 'popularity',
        "apiKey": "779677d967a94d05b96915da5e5d6200"
    }
    response_news = requests.get(url="https://newsapi.org/v2/everything", params=parameters_news)
    response_news.raise_for_status()
    news_data = response_news.json()
    # Get the first three news articles
    first_three_news = news_data["articles"][:1]

    # Print the titles of the first three news articles

    formatted_articles = []
    for news in first_three_news:
        titles = (news["title"])
        description = (news["description"])
    formatted_articles = [
        f"The increment in Tesla stock is {increment}%.\n\n"
        f"📰 Headline: {titles}\n"
        f"📝 Brief: {description}"
    ]
    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 


    client = Client(TWILIO_SID,TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
                             body=article,
                             from_='+14849788500',
                             to='+917736221137'
                         )

    print(message.sid)



if decrement>0.2:

    parameters_news = {
        "q": "Tesla",
        "sortBy": 'popularity',
        "apiKey": "779677d967a94d05b96915da5e5d6200"
    }
    response_news = requests.get(url="https://newsapi.org/v2/everything", params=parameters_news)
    response_news.raise_for_status()
    news_data = response_news.json()
    # Get the first three news articles
    first_three_news = news_data["articles"][1:3]

    # Print the titles of the first three news articles

    for article in first_three_news:
        titles = (article["title"])
        description = (article["description"])
    formatted_articles = [
        f"The decrement in Tesla stock is {decrement}%.\n\n"
        f"📰 Headline: {titles}\n"
        f"📝 Brief: {description}"
    ]
    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    # to send a separate message with each article's title and description to your phone number.

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='+14849788500',
            to='+919072546104'
        )

    print(message.sid)
    print("Your SMS has been sucessfully sent :))")


