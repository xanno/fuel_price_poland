import numpy as np
import pandas as pd
import requests


def read_petrol_price():
    url = r'https://www.lotos.pl/145/type,oil_95/dla_biznesu/hurtowe_ceny_paliw/archiwum_cen_paliw'
    req = requests.get(url)

    petrol_df = pd.read_html(req.text)
    petrol_df = petrol_df[0]
    petrol_df.to_csv('petrol95.csv')

    url = r'https://www.lotos.pl/145/type,oil_eurodiesel/dla_biznesu/hurtowe_ceny_paliw/archiwum_cen_paliw'
    req = requests.get(url)

    petrol_df = pd.read_html(req.text)
    petrol_df = petrol_df[0]
    petrol_df.to_csv('data/euro_diesel.csv')
