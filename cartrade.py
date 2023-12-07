import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import mysql.connector
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dve-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
options.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome(options=options)
connection = mysql.connector.connect(
    host = '<HOSTNAME>',
    user= '<USERNAME>',
    password = '<PASSWORD>',
    database = '<DATABASENAME>'
    )
cursor = connection.cursor()

#================================================================================
#cartrade
page_url=[]
car_names = []
fuel_type = []
car_runs = []
car_zpay = []
car_prices = []
car_ori_prices = []
car_locations = []
url_redirect=[]
img_redirect=[]
uidT=[]
uidO=[]

m='https://www.cartrade.com/buy-used-cars/p-1/#so=-1&sc=-1&city=1721'
driver.get(m)
soup = BeautifulSoup(driver.page_source,'lxml')
urlch = soup.find('div',class_='sidefltr').find('div',class_='leftbar').find('select',class_='selectcity').find_all('optgroup')
uT = urlch[0].find_all('option')
for k in uT:
    idT = k.get('filterid')
    if idT=='-1':
        continue
    else:
        uidT.append(idT)
uO = urlch[1].find_all('option')
for m in uO:
    idO = m.get('filterid')
    uidO.append(idO)

for ml in uidT:
    for i in range(1,250,1):
        t = f'https://www.cartrade.com/buy-used-cars/p-{i}/#so=-1&sc=-1&city={ml}'
        page_url.append(t)

for ml in uidO:
    for i in range(1,2,1):
        t = f'https://www.cartrade.com/buy-used-cars/p-{i}/#so=-1&sc=-1&city={ml}'
        page_url.append(t)

for t in page_url:
        driver.get(t)
        time.sleep(1)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source,'lxml')
        names= soup.find_all("h2",class_="h2heading truncate")
        for k in names:
            tup=k.text
            car_names.append(tup)
            tp=k.find('a').get('href')
            url_redirect.append('https://www.cartrade.com'+tp)
        #----------------------------------------------------------------------------
        prices=soup.find_all("div",class_="cr_prc")
        for k in prices:
            price_text = k.get_text(strip=True)
            price = price_text.replace('\t','').replace('Make\nOffer', '').split('₹')
            if len(price) < 3:
                car_ori_prices.append("Not Available")
            else:
                car_ori_prices.append(price[2])
            car_prices.append(price[1])
        #==================================================================================
        emi = soup.find_all('div',class_='details_out')
        for k in emi:
            zp=k.find("span",class_="pull-left font_13 color-grey")
            if zp !=None:
                zup=zp.a.text
                car_zpay.append(zup)
            else:
                car_zpay.append('N/A')
        #----------------------------------------------------------
        types=soup.find_all('div',class_='info_cr_new')
        for k in types:
            typ = k.find_all('li')
            car_runs.append(typ[0].text)
            fuel_type.append(typ[2].text)
            car_locations.append(typ[4].text)
        img_box= soup.find_all('div',class_='blk_grid_img_new')
        for k in img_box:
            img_ck = k.find('span', attrs={'data-role': 'click-tracking'})
            img_new= img_ck.img.get('src')
            img_redirect.append(img_new)

try:
  create_table = "create table cartrade_cars (Source varchar(255), Car_names varchar(255), Price_before_discount varchar(255), Car_price varchar(255), Run_km varchar(255), Fuel_type varchar(255), Downpayment varchar(255), Location varchar(255),Url varchar(1500),Img varchar(1500))"
  cursor.execute(create_table)
  insert_query = "INSERT INTO cartrade_cars (Source, Car_Names, Price_before_discount, Car_price, Run_km, Fuel_type, Downpayment, Location, Url,Img) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"
  data_to_insert=[]
  for i in range(len(car_names)):
    data_to_insert.append(("cartrade.com", car_names[i], car_ori_prices[i], car_prices[i], car_runs[i], fuel_type[i],car_zpay[i],car_locations[i],url_redirect[i],img_redirect[i]))
  cursor.executemany(insert_query, data_to_insert)
  connection.commit()
except:
  truncate = "truncate table cartrade_cars"
  cursor.execute(truncate)
  insert_query = "INSERT INTO cartrade_cars (Source, Car_Names, Price_before_discount, Car_price, Run_km, Fuel_type, Downpayment, Location, Url,Img) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"
  data_to_insert=[]
  for i in range(len(car_names)):
    data_to_insert.append(("cartrade.com", car_names[i], car_ori_prices[i], car_prices[i], car_runs[i], fuel_type[i],car_zpay[i],car_locations[i],url_redirect[i],img_redirect[i]))
  cursor.executemany(insert_query, data_to_insert)
  connection.commit()

driver.quit()
