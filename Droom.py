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
#========================================================================
url=f'https://droom.in/cars/used?bucket=car&category=Car&condition=used&include_premium=1&max_listing_age=365&min_listing_age=1&most_recent=1&need_filters=1&page=1&rows_per_page=24&selling_format=fixed_price&show_make_model=1&status=active'
car_names = []
fuel_type=[]
model_year=[]
typ_1data=[]
car_runs = []
car_prices = []
car_ori_pri=[]
car_locations = []
url_redirect=[]
data_to_insert = []
img_redirect=[]
driver.get(url)
time.sleep(30)
try:
    cross1=WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[3]/div/button')))
    cross1.click()
except:
    pass
time.sleep(5)
try:
    cross2 = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[1]/button")))
    driver.execute_script("arguments[0].scrollIntoView(true);", cross2)
    driver.execute_script("arguments[0].focus();", cross2)
    driver.execute_script("arguments[0].click();", cross2)

except:
    pass
while True:
    height = driver.execute_script("return document.body.scrollHeight")
    for i in range(50,100,1):
        ni = i/100
        script = f"window.scrollTo(0, document.body.scrollHeight*{ni});"
        driver.execute_script(script)
        try:
            cross5=WebDriverWait(driver, 1).until(
                                EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[4]/button")))
            cross5.click()
        except:
            try:
                cross2 = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[1]/button")))
                driver.execute_script("arguments[0].scrollIntoView(true);", cross2)
                driver.execute_script("arguments[0].focus();", cross2)
                driver.execute_script("arguments[0].click();", cross2)

            except:
                pass
        time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if height == new_height:
        break
#--------------------------------------------------------------------------
for i in range(1,100,1):
            ni = i/100
            script = f"window.scrollTo(0, document.body.scrollHeight*{ni});"
            driver.execute_script(script)
            time.sleep(1)
#--------------------------------------------------------------------------
soup = BeautifulSoup(driver.page_source,'lxml')

box=soup.find_all('div','grid')
for k in box:
    names = k.find('div',class_='card-body').find("h3").find('a')
    car_names.append(names.text)
    url1= names.get('href')
    url_redirect.append(url1)
#============================================================================
    price=k.find('div',class_='card-body').find('div',class_='MuiGrid-root MuiGrid-container').find('div').find('div')
    caror=price.find('del')
    if caror !=None:
        car_ori_pri.append(caror.text)
    else:
        car_ori_pri.append('N/A')
    car_prices.append('₹'+price.span.text)

#===================================================================================
    type1 = k.find('div',class_='card-body').find_all('div')
    ty = type1[4].find_all('div')
    car_runs.append(ty[0].text)
    tp = ty[0].text
    car_locations.append(ty[2].text)
    model_year.append(ty[4].text)
    fuel_type.append(ty[6].text)
    if len(ty)>9:
        typ_1data.append(ty[8].text)
    else:
        typ_1data.append('N/A')

    img = k.find('figure').find('img',class_='card-img-top').get('src')
    img_redirect.append(img)
#---------------------------------------------------------------------------------------------------------------
try:
  create_table = "create table droom_cars (Source varchar(255), Car_names varchar(255), Price_withoutDiscount varchar(255), Car_price varchar(255), Run_km varchar(255), Car_location varchar(255), Model_year varchar(255), Fuel_type varchar(255), Transmission varchar(255), Url varchar(1500),Img varchar(1500))"
  cursor.execute(create_table)
  insert_query = "INSERT INTO droom_cars (Source, Car_Names, Price_withoutdiscount, car_price, Run_km, Car_location, Model_year, Fuel_type, Transmission, Url, Img) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  for i in range(len(car_names)):
      data_to_insert.append(('droom.in', car_names[i], car_ori_pri[i], car_prices[i], car_runs[i], car_locations[i], model_year[i], fuel_type[i], typ_1data[i], url_redirect[i], img_redirect[i]))
  cursor.executemany(insert_query, data_to_insert)
  connection.commit()
  print("Data inserted successfully")
except:
  truncate = "truncate table droom_cars"
  cursor.execute(truncate)
  insert_query = "INSERT INTO droom_cars (Source, Car_Names, Price_withoutdiscount, car_price, Run_km, Car_location, Model_year, Fuel_type, Transmission, Url, Img) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  for i in range(len(car_names)):
      data_to_insert.append(('droom.in', car_names[i], car_ori_pri[i], car_prices[i], car_runs[i], car_locations[i], model_year[i], fuel_type[i], typ_1data[i], url_redirect[i], img_redirect[i]))
  cursor.executemany(insert_query, data_to_insert)
  connection.commit()
  print("Data inserted successfully")
driver.quit()
