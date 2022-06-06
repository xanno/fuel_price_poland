from avg_salary import avg_salary_csv
from fuel_price_countries import read_petrol_price_country
from petrol import *
from petrol_read_html import read_petrol_price
from currency_exchange import usd_pln
import itertools
import threading
import time
import sys
from PIL import Image

done = False


# here is the animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rdrawing ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')


t = threading.Thread(target=animate)
t.start()
# read_petrol_price()
# usd_pln()
# read_petrol_price_country()
# avg_salary_csv()
draw_petrol_oil_plot()
draw_petrol_tax_pie()

draw_country_petrol_bar()

img = Image.open('tax.png')
img.show()
img = Image.open('petrol_oil.png')
img.show()
# time.sleep(10)
done = True
