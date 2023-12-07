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
#========================================================================================
#mahindrafirstchoice
car_names = []
type1_data = []
fuel_type = []
car_runs = []
car_owner=[]
car_prices = []
car_locations = []
url_redirect=[]
page_url=[]
img_redirect=[]

#--------------------------------------------------------------
page_url.append('https://www.mahindrafirstchoice.com/used-cars/Gurgaon')
page_url.append('https://www.mahindrafirstchoice.com/used-cars/noida')
page_url.append('https://www.mahindrafirstchoice.com/used-cars/Delhi')
page_url.append('https://www.mahindrafirstchoice.com/used-cars/Faridabad')
page_url.append('https://www.mahindrafirstchoice.com/used-cars/Ghaziabad')
page_url.append('https://www.mahindrafirstchoice.com/used-cars/Bangalore')
page_url.append('https://www.mahindrafirstchoice.com/used-cars/Chennai')
page_url.append('https://www.mahindrafirstchoice.com/used-cars/Pune')
page_url.append('https://www.mahindrafirstchoice.com/used-cars/Mumbai')
#===============================================================================
for i in page_url:
    driver.get(i)
    while True:
        height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if height == new_height:
            break

    for t in range(1,100,1):
      ni = t/100
      script = f"window.scrollTo(0, document.body.scrollHeight*{ni});"
      driver.execute_script(script)
      time.sleep(1)
    #--------------------------------------------------------------------------
    soup = BeautifulSoup(driver.page_source,'lxml')
    box=soup.find_all("div",class_="col-md-4 col-12 general-car")
    for n in box:
        names = n.find_all("div", class_= "buyer_header")
        for k in names:
            nam=k.find_all("a")
            n1=nam[0].h3.get_text().strip()
            n2=nam[1].h3.get_text().strip()
            car_names.append(n1+" "+n2)
    #======================================================================
        price = n.find_all("span", {"class": "car_price"})
        for k in price:
            pri = k.text
            car_prices.append(pri)
    #===============================================================================
        locations = n.find_all("span", {"class": "buyer_locations icon_set stock_location b"})
        for k in locations:
            lo = k.text
            car_locations.append(lo)
    #==========================================================================================
        types= n.find_all("ul",class_="spec-info-list")
        for k in types:
            li_tags=k.find_all("li")
            t1=li_tags[0].text.strip()
            car_runs.append(t1)
            t2=li_tags[2].text.strip()
            type1_data.append(t2)
            t3=li_tags[1].text.strip()
            fuel_type.append(t3)
            t4=li_tags[3].text.strip()
            car_owner.append(t4)
    #=========================================================================
        ur=n.find("a",class_="lnkstockdetail").get("href")
        url_redirect.append("https://www.mahindrafirstchoice.com"+ur)


        img_element = n.find("img",class_='lazyload').get('src')
        img_redirect.append(img_element)

#============================================================================
try:
  create_table = "create table mahindra_cars (Source varchar(255), Car_names varchar(255), Car_price varchar(255), Design varchar(255),Run_km varchar(255), Fuel_type varchar(255), Owner varchar(255), Location varchar(255),Url varchar(1500),Img varchar(1500))"
  cursor.execute(create_table)
  insert_query = "INSERT INTO  mahindra_cars (Source, Car_Names, Car_price,Design, Run_km, Fuel_type, Owner, location, Url,Img) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"
  data_to_insert=[]
  for i in range(len(car_names)):
    data_to_insert.append(("mahindrafirstchoice.com", car_names[i], car_prices[i], type1_data[i], car_runs[i], fuel_type[i],car_owner[i],car_locations[i], url_redirect[i], img_redirect[i]))
  cursor.executemany(insert_query, data_to_insert)
  connection.commit()

except:
  truncate = "truncate table mahindra_cars"
  cursor.execute(truncate)
  insert_query = "INSERT INTO  mahindra_cars (Source, Car_Names, Car_price,Design, Run_km, Fuel_type, Owner, location, Url,Img) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"
  data_to_insert=[]
  for i in range(len(car_names)):
    data_to_insert.append(("mahindrafirstchoice.com", car_names[i], car_prices[i], type1_data[i], car_runs[i], fuel_type[i],car_owner[i],car_locations[i], url_redirect[i],img_redirect[i]))
  cursor.executemany(insert_query, data_to_insert)
  connection.commit()

driver.quit()
