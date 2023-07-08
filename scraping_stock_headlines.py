from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
import csv

s = HTMLSession()


def take_ticker():
    ticker_temp = input("Enter ticker: ")
    response_temp = s.get(f"https://finviz.com/quote.ashx?t={ticker_temp}&p=d")
    if response_temp.status_code != 200:
        take_ticker()
    return response_temp, ticker_temp


response, ticker = take_ticker()
soup = BeautifulSoup(response.text, "html.parser")

link_and_headline_matches = soup.find_all("a", attrs={"class": "tab-link-news"})
time_matches = soup.find_all("td", attrs={"width": "130", "align": "right"})
stock_data = []

for i in range(len(time_matches)):
    stock_dict = {
        "Date": time_matches[i].text[-17:-10],
        "Headline": link_and_headline_matches[i].text,
    }
    stock_data.append(stock_dict)

with open(f"{ticker}.csv", "w", newline="") as file:
    amzfields = ["Date", "Headline"]
    writer = csv.DictWriter(file, fieldnames=amzfields)
    writer.writeheader()
    writer.writerows(stock_data)
