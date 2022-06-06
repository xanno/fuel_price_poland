import pandas as pd
import requests
import numpy as np


def read_petrol_price_country():
    url = r'https://www.cargopedia.pl/europejskie-ceny-paliw'
    req = requests.get(url)
    country_petrol_df = pd.read_html(req.text)

    country_petrol_df = country_petrol_df[0]
    # country_petrol_df.drop([0], inplace=True)

    country_petrol_df.to_csv('data/country_fuels_price.csv')


read_petrol_price_country()