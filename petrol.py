import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

"""
oil price: https://pl.investing.com/commodities/brent-oil-historical-data 
pln to usd: https://www.nbp.pl/kursy/Archiwum/archiwum_tab_a_2022.csv
diesel price: https://www.lotos.pl/145/type,oil_eurodiesel/dla_biznesu/hurtowe_ceny_paliw/archiwum_cen_paliw
95 price: https://www.lotos.pl/145/type,oil_95/dla_biznesu/hurtowe_ceny_paliw/archiwum_cen_paliw
"""

col_names_petrol = ['unnamed', 'date', 'price95', 'excise95', 'Fuelsurcharge95']
petrol_df = pd.read_csv('data/petrol95.csv', parse_dates=['date'], names=col_names_petrol, index_col='date',
                        usecols=col_names_petrol[1:], decimal=',', header=0, thousands=' ')

col_names_diesel = ['unnamed', 'date', 'price_diesel', 'excise_diesel', 'Fuelsurcharge_diesel']
diesel_df = pd.read_csv('data/euro_diesel.csv', parse_dates=['date'], names=col_names_diesel, index_col='date',
                        usecols=col_names_diesel[1:], decimal=',', header=0, thousands=' ')

col_names_oil = ["date", "last", "open", "maximum", "minimum", "vol", "change"]
oil_df = pd.read_csv('data/oil.csv', names=col_names_oil, usecols=['date', 'open'], index_col='date',
                     parse_dates=['date'],
                     decimal=',', thousands=' ', header=0, dayfirst=True)

usd_df = pd.read_csv('data/exchange.csv', parse_dates=['date'], index_col='date')

petrol_df['oil'] = oil_df.open
petrol_df['usd'] = usd_df.usd
petrol_df['diesel'] = diesel_df['price_diesel']
petrol_df['Fuelsurcharge95'] = petrol_df['Fuelsurcharge95'] / 100
# Filling Nan with the closest values
petrol_df = petrol_df.fillna(method="bfill")
petrol_df = petrol_df.fillna(method="ffill")

country_fuel_df = pd.read_csv('data/country_fuels_price.csv', header=None)
country_fuel_df.drop([0, 1], inplace=True)
country_fuel_df = country_fuel_df[[1, 3]]
country_fuel_df.rename(columns={1: "Kraj", 3: 'PB95 PLN'}, inplace=True)
country_fuel_df.set_index('Kraj', inplace=True)
country_fuel_df['PB95 PLN'] = pd.to_numeric(country_fuel_df['PB95 PLN'])
country_fuel_df['PB95 PLN'] = country_fuel_df['PB95 PLN'] / 1000
country_fuel_df.sort_values('PB95 PLN', inplace=True, ascending=False)

avg_salary_df = pd.read_csv('data/avg_salary.csv')
avg_salary_df.drop(['Unnamed: 0', 'Skrót', 'Nr.'], axis=1, inplace=True)
avg_salary_df.set_index('Kraj UE', inplace=True)
avg_salary_df['cena benzyny'] = country_fuel_df

avg_salary_df = avg_salary_df.replace(regex=[' zł', "'"], value='')
avg_salary_df['Miesięczne wynagrodzenie brutto, złotych *'] = pd.to_numeric(
    avg_salary_df['Miesięczne wynagrodzenie brutto, złotych *'])
avg_salary_df['siła nabywcza'] = round(
    avg_salary_df['Miesięczne wynagrodzenie brutto, złotych *'] / avg_salary_df['cena benzyny']).astype(int)


def draw_ppp_fuel_eu_bar():
    avg_salary_df.sort_values('siła nabywcza', inplace=True, ascending=False)
    fig, ax = plt.subplots(figsize=(32, 10), dpi=100)
    colors = ['r' if _ == 'Polska' else 'c' for _ in avg_salary_df.index]
    avg_salary_df['siła nabywcza'].plot(kind='bar', color=colors, width=0.9)
    x = np.arange(len(avg_salary_df))
    ax.tick_params(which='major', labelsize=20)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_xticks(x)
    plt.ylabel('Ile można zatankować PB95 w litrach\n za miesięczne wynagrodzenie brutto', fontsize=15)

    plt.tight_layout()
    ax.set(xlabel=None)
    fig.savefig('ppp_fuel_bar.png')


def draw_country_petrol_bar():
    fig, ax = plt.subplots(figsize=(32, 10), dpi=100)
    colors = ['r' if _ == 'Polska' else 'c' for _ in country_fuel_df.index]
    country_fuel_df['PB95 PLN'].plot(kind='bar', color=colors, width=0.9)
    x = np.arange(len(country_fuel_df))
    ax.tick_params(axis='x', which='major', labelsize=20)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_xticks(x)
    plt.yticks(color='w')
    plt.tight_layout()
    ax.set(xlabel=None)
    y = round(country_fuel_df['PB95 PLN'], 2)
    for i in range(len(country_fuel_df)):
        plt.text(i, y[i], y[i], ha='center', fontsize=15)
    fig.savefig('country_bar.png')


def draw_petrol_tax_plot():
    price_without_tax = petrol_df['price95'] - petrol_df['excise95'] - petrol_df['Fuelsurcharge95']
    fig, ax = plt.subplots(figsize=(30, 10), dpi=100)
    txt_l = "Sources: nbp.pl, lotos.pl, investing.com"
    plt.figtext(0.5, 0.01, s=txt_l, ha="center", fontsize=14)
    plt.rcParams.update({'font.size': 30})
    plt.tick_params(labelsize=25)
    # plt.title("Fuel price", fontsize=30)
    x = petrol_df.index
    y = price_without_tax / 1000
    ax.plot(x, y, 'r', label='PB95 price without tax', linewidth=4)
    y = petrol_df['price95'] / 1000
    ax.plot(x, y, 'y', label='PB95 full price', linewidth=4)
    ax.legend()
    plt.tight_layout()
    fig.savefig('tax_line.png')


def draw_petrol_tax_pie():
    tax_df = petrol_df.copy()
    mask = (tax_df.index.year > 2021) & (tax_df.index.month > 2)
    tax_df = tax_df[mask]
    labels = 'Cena', 'Cło', 'Opłata paliwowa\nMarża\nOpłata emisyjna', "vat"
    excise = tax_df['excise95'].mean()
    fuel_surcharge = tax_df['Fuelsurcharge95'].mean() / 10
    vat = tax_df['price95'].mean() * 0.08
    emission_tax = tax_df['price95'].mean() * 0.015
    margin = tax_df['price95'].mean() * 0.013
    price_without_tax = tax_df['price95'].mean() - excise - fuel_surcharge - vat
    - emission_tax - margin
    surcharges = emission_tax + fuel_surcharge + margin
    sizes = [price_without_tax, excise, surcharges, vat]
    explode = (0, 0.1, 0.1, 0.1)
    fig, ax1 = plt.subplots(figsize=(14, 14), dpi=100)
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=75)
    ax1.axis('equal')
    txt_l = "Sources: nbp.pl, lotos.pl, investing.com"
    plt.figtext(0.5, 0.01, s=txt_l, ha="center", fontsize=14)
    plt.tight_layout()
    fig.savefig('tax.png')


def draw_petrol_oil_plot():
    pp_df = petrol_df.copy()
    mask = (petrol_df.index.year > 2021) & (petrol_df.index.month > 1)
    pp_df = pp_df[mask]
    pp_df['oilPLN'] = pp_df.oil * pp_df.usd
    pp_df.oilPLN = pp_df.oilPLN / pp_df.iloc[-1].oilPLN
    pp_df.price95 = pp_df.price95 / pp_df.iloc[-1].price95
    pp_df.diesel = pp_df.diesel / pp_df.iloc[-1].diesel

    fig, ax = plt.subplots(figsize=(30, 10), dpi=100)
    plt.yticks(color='w')
    txt_l = "Sources: nbp.pl, lotos.pl, investing.com"
    plt.figtext(0.5, 0.01, s=txt_l, ha="center", fontsize=14)
    plt.rcParams.update({'font.size': 30})
    plt.tick_params(labelsize=25)
    # plt.title("fuels to crude  oil price", fontsize=30)
    x = pp_df.index
    y = pp_df.price95
    ax.plot(x, y, 'r', label='PB 95', linewidth=4)
    y = pp_df.oilPLN
    ax.plot(x, y, 'b--', label='crude oil PLN', linewidth=4)
    y = pp_df.diesel
    ax.plot(x, y, 'y', label='diesel', linewidth=4)
    ax.legend()
    plt.tight_layout()

    fig.savefig('petrol_oil.png')
