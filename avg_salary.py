import pandas as pd
import requests
import numpy as np


def avg_salary_csv():
    url = r'https://ru-geld.de/pl/salary/europe.html#average'
    req = requests.get(url)
    avg_salary = pd.read_html(req.text)
    avg_salary = avg_salary[1]
    avg_salary.to_csv('data/avg_salary.csv')
