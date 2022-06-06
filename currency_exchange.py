import pandas as pd


def usd_pln():
    url = 'https://www.nbp.pl/kursy/Archiwum/archiwum_tab_a_2022.csv'

    f = lambda x: (x.replace(",", "."))
    df = pd.read_csv(url, delimiter=';', encoding='Windows-1250', usecols=['data', '1USD'],
                     converters={'1USD': f})

    df.drop([0], inplace=True)
    df.drop(df.tail(3).index, inplace=True)

    df['data'] = df['data'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))

    df.rename(columns={'data': 'date', '1USD': 'usd'}, inplace=True)
    df["usd"] = df['usd'].astype('float')
    df.set_index('date', inplace=True)
    df.to_csv('data/exchange.csv')
