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
url=f"https://www.quikr.com/cars/used+Maruti-Suzuki_Hyundai_Tata_Mahindra_Honda_Toyota_Ford_Renault_Chevrolet_Volkswagen_Mercedes-Benz_Skoda_Nissan_Audi_BMW_Kia_Fiat_MG-Motors_Jeep_Datsun_Mini_Mitsubishi_Land-Rover_Volvo_Hindustan-Motors_Isuzu_Force-Motors_Jaguar_Porsche_Premier_Ssangyong_Aston-Martin_Daewoo_Ferrari_Lexus_Opel_San+Petrol_Diesel_CNG_LPG_Hybrid_Electric+cars+all-india+z1399vbh"
car_names = []
info=[]
car_runs = []
fuel_type=[]
car_prices = []
car_locations = []
url_redirect=[]
img_url=[]
car_owner=[]
#===============================================================================
driver.get(url)
while True:
    height = driver.execute_script("return document.body.scrollHeight")
    for i in range(50,100,1):
        ni=i/100
        script = f"window.scrollTo(0, document.body.scrollHeight*{ni});"
        driver.execute_script(script)
    time.sleep(5)
    try:
        cross1=WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[2]/button[1]')))
        cross1.click()
    except:
        new_height = driver.execute_script("return document.body.scrollHeight")

        if height == new_height:
            break

for i in range(1,100,1):
            ni = i/100
            script = f"window.scrollTo(0, document.body.scrollHeight*{ni});"
            driver.execute_script(script)
            time.sleep(1)
#--------------------------------------------------------------------------
soup = BeautifulSoup(driver.page_source,'lxml')
box = soup.find_all("div",class_="car-info__footer")
for k in box:
#============================================================
    names = k.find("h2").text
    car_names.append(names)
#===============================================================
    types = k.find("div", {"class": "prime-features"})
    if types!=None:
        lim = types.text.split('/')
        if len(lim)>0:
            car_runs.append(lim[0])
        else:
            car_runs.append('N/A')
        if len(lim)>1:

            fuel_type.append(lim[1])
        else:
            fuel_type.append('N/A')
        if len(lim)>2:
            car_owner.append(lim[2])
        else:
            car_owner.append('N/A')

#==================================================================
    price = k.find_all("div", {"class": "price"})
    for m in price:
        n_price = m.text
        car_prices.append(n_price)
#===========================================================

#========================================================
utr= soup.find_all("div",class_="mdc-layout-grid__cell mdc-layout-grid__cell--span-4-desktop mdc-layout-grid__cell mdc-layout-grid__cell--span-12-phone")
for m in utr:
    ur= m.find('a',class_='qc-ads__card')
    if ur != None:
        url_redirect.append('https://www.quikr.com'+ur.get('href'))

        img_ur= ur.find('img',class_='lozad').get('src')
        img_url.append(img_ur)
    else:
        continue
    locations = m.find("footer", {"class": "qc-ads__card--footer"})
    location = locations.find("span").text
    car_locations.append(location)
#============================================================================
try:
  create_table = "create table quikr_cars (Source varchar(255), Car_names varchar(255), Car_price varchar(255), Run_km varchar(255), Car_location varchar(255), Car_owner varchar(255),Fuel_type varchar(255), Url varchar(1500), Img_Url varchar(1500))"
  cursor.execute(create_table)
  insert_query = "INSERT INTO quikr_cars (Source, Car_Names, Car_price, Run_km, Car_location, Car_owner, Fuel_type, Url, Img_Url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
  data_to_insert=[]
  for i in range(len(car_names)):
      data_to_insert.append(('quikr.com', car_names[i], car_prices[i], car_runs[i], car_locations[i],car_owner[i], fuel_type[i], url_redirect[i], img_url[i]))
  cursor.executemany(insert_query, data_to_insert)
  connection.commit()
except:
  truncate = "truncate table quikr_cars"
  cursor.execute(truncate)
  insert_query = "INSERT INTO quikr_cars (Source, Car_Names, Car_price, Run_km, Car_location, Car_owner, Fuel_type, Url, Img_Url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
  data_to_insert=[]
  for i in range(len(car_names)):
      data_to_insert.append(('quikr.com', car_names[i], car_prices[i], car_runs[i], car_locations[i],car_owner[i], fuel_type[i], url_redirect[i], img_url[i]))
  cursor.executemany(insert_query, data_to_insert)
  connection.commit()
#===========================================================================
driver.quit()
