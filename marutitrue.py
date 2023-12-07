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
#=======================================================================================
#marutisuzukitruevalue
page_url=[]
car_names=[]
car_yr=[]
fuel_type=[]
car_locations=[]
car_prices = []
car_runs=[]
url_redirect=[]
img_redirect=[]
#=======================================================
for i in range(1,835,1):
    t = f'https://marutisuzukitruevalue.com/used-cars-in-greater-noida/{i}#carAge=0%2C35&CarCityRange=100000&page={i}'
    page_url.append(t)
#=====================================================================
for t in page_url:
    driver.get(t)
    time.sleep(5)
    ni = 90/100
    script = f"window.scrollTo(0, document.body.scrollHeight*{ni});"
    driver.execute_script(script)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source,'lxml')
    boxee =soup.find_all('div',class_='col')
    for k in boxee:
        names=k.find('div',class_='leftSec')
        car_names.append(names.text)
        utr=names.find('a').get('href')
        url_redirect.append('https://marutisuzukitruevalue.com'+utr)
        #===================================================
        loca=k.find('div',class_='location').text.split('|')
        car_locations.append(loca[0])
        #==========================================
        type=k.find('div',class_='yearTxt').text.split('|')
        car_yr.append(type[0])
        fuel_type.append(type[1])
        car_runs.append(type[2])
        #=====================================================
        pri=k.find('div',class_='priceTxt').text.replace('Calculate EMI','').replace('Select for Smart Finance','')
        car_prices.append(pri)
        #=================================
        im = k.find('div','carImgBx').a.find_all('img')
        img_ur = im[1].get('src')
        img_redirect.append(img_ur)
#======================================================================================
try:
  create_table = "create table marutisuzukitruevalue_cars (Source varchar(255), Car_names varchar(255), Car_price varchar(255), Run_km varchar(255), Fuel_type varchar(255), Location varchar(255),Url varchar(1500),Img varchar(1500))"
  cursor.execute(create_table)
  insert_query = "INSERT INTO  marutisuzukitruevalue_cars (Source, Car_Names, Car_price, Run_km, Fuel_type, Location, Url,Img) VALUES ( %s, %s, %s, %s, %s, %s, %s,%s)"
  data_to_insert=[]
  for i in range(len(car_names)):
    data_to_insert.append(("marutisuzukitruevalue.com", car_names[i], car_prices[i], car_runs[i], fuel_type[i],car_locations[i], url_redirect[i],img_redirect[i]))
  cursor.executemany(insert_query, data_to_insert)
  connection.commit()
except:
  truncate = "truncate table marutisuzukitruevalue_cars"
  cursor.execute(truncate)
  insert_query = "INSERT INTO  marutisuzukitruevalue_cars (Source, Car_Names, Car_price, Run_km, Fuel_type, Location, Url,Img) VALUES ( %s, %s, %s, %s, %s, %s, %s,%s)"
  data_to_insert=[]
  for i in range(len(car_names)):
    data_to_insert.append(("marutisuzukitruevalue.com", car_names[i], car_prices[i], car_runs[i], fuel_type[i],car_locations[i], url_redirect[i],img_redirect[i]))
  cursor.executemany(insert_query, data_to_insert)
  connection.commit()
driver.quit()
