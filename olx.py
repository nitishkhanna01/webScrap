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
page_url=[]
car_names = []
type1_data = []
car_runs = []
car_prices = []
car_locations = []
url_redirect=[]
updt=[]
img_redirect=[]

page_url.append('https://www.olx.in/cars_c84?filter=petrol_eq_petrol')
page_url.append('https://www.olx.in/cars_c84?filter=petrol_eq_diesel')
page_url.append('https://www.olx.in/cars_c84?filter=petrol_eq_lpg')
page_url.append('https://www.olx.in/cars_c84?filter=petrol_eq_cng')
page_url.append('https://www.olx.in/cars_c84?filter=petrol_eq_electric')
for ut in page_url:
    driver.get(ut)
    while True:
        height = driver.execute_script("return document.body.scrollHeight")
        for i in range(80,100,1):
            ni = i/100
            script = f"window.scrollTo(0, document.body.scrollHeight*{ni});"
            driver.execute_script(script)
            try:
                time.sleep(2)
                load_more_button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-aut-id='btnLoadMore']"))
                )
                load_more_button.click()
                time.sleep(2)
            except:
                pass
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
    names = soup.find_all("div", class_= "_2Gr10")
    types = soup.find_all("div", {"class": "_21gnE"})
    price = soup.find_all("span", {"class": "_1zgtX"})
    locations = soup.find_all("div", {"class": "_3VRSm"})
    url_1=soup.find_all("li",class_="_3V_Ww")
    #============================================================================
    for k in names:
        name = k.text
        car_names.append(name)
#--------------------------------------------------------------------------------------------------
    for ul_tag in types:
        div_tag=ul_tag.text.split('-')
        type_1=div_tag[0]
        if len(div_tag)>1:
            type_2=div_tag[1]
            car_runs.append(type_2)
        else:
            car_runs.append('N/A')
        type1_data.append(type_1)
#=====================================================================================================================================================
    for k in price:
        n_price = k.text
        if n_price is None:
            price_up="Not Available"
            car_prices.append(price_up)
        else:
            car_prices.append(n_price)
#=========================================================================================================================================
    for k in locations:
        location = k.contents[0].strip()
        if location is None:
            location_new= "Not Available"
            car_locations.append(location_new)
        else:
            car_locations.append(location)
        date = k.find('span').text.strip()
        updt.append(date)
#---------------------------------------------------------------------------------------------------------------
    for k in url_1:
        url_n=k.a.get("href")
        url_redirect.append("https://www.olx.in"+url_n)

    img = soup.find_all('figure',class_='_3UrC5')
    for k in img:
        img_r=k.find('img').get('src')
        img_redirect.append(img_r)
#---------------------------------------------------------------------------------------------------------------

try:
  create_table = "create table olx_cars (Source varchar(255), Car_names varchar(255), Model_Year varchar(255), Car_price varchar(255), Run_km varchar(255), Car_location varchar(255), Url varchar(1500),Img varchar(1500))"
  cursor.execute(create_table)
  insert_query = "INSERT INTO olx_cars (Source, Car_Names, Model_Year, Car_price, Run_km, Car_location, Url, Img) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
  data_to_insert = []
  for i in range(len(car_locations)):
      data_to_insert.append(("olx.com", car_names[i], type1_data[i], car_prices[i], car_runs[i], car_locations[i], url_redirect[i], img_redirect[i]))

  cursor.executemany(insert_query, data_to_insert)
  connection.commit()
except:
  truncate = "truncate table olx_cars"
  cursor.execute(truncate)
  insert_query = "INSERT INTO olx_cars (Source, Car_Names, Model_Year, Car_price, Run_km, Car_location, Url, Img) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
  data_to_insert = []
  for i in range(len(car_locations)):
      data_to_insert.append(("olx.com", car_names[i], type1_data[i], car_prices[i], car_runs[i], car_locations[i], url_redirect[i], img_redirect[i]))
  cursor.executemany(insert_query, data_to_insert)
  connection.commit()

driver.quit()
