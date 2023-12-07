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
#==========================================================================
car_names = []
type1_data = []
type2_data = []
car_runs = []
car_owner=[]
engine=[]
num_plate=[]
car_zpay = []
car_infos = []
car_prices = []
car_ori_prices = []
car_locations = []
url_redirect=[]
img_redirect=[]
page_url=[]
#=======================================================
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=2&pinId=110001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=2378&pinId=400001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=4709&pinId=560001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=3686&pinId=500001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=1692&pinId=380001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=5&pinId=122001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=5732&pinId=600001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=2423&pinId=411001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=134&pinId=201301")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=132&pinId=201001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=290&pinId=226001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=2130&pinId=302001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=777&pinId=700001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=6356&pinId=682001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=2598&pinId=422001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=2713&pinId=440001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=6105&pinId=641001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=2920&pinId=450001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=8184&pinId=800001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=1605&pinId=394101")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=769&pinId=134101")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=666&pinId=141001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=33&pinId=124001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=1606&pinId=360001")
page_url.append("https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&storeCityId=1674&pinId=390001")


#===============================================================================
for t in page_url:
#--------------------------------------------------------------
    driver.get(t)
    while True:
        height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
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
    names = soup.find_all("h2", class_= "_2lmIw")
    types = soup.find_all("ul", {"class": "_1hOnS"})
    runs = soup.find_all("ul", {"class": "_13yb6"})
    zpay = soup.find_all("div", {"class": "_1Em-A"})
    price = soup.find_all("div", {"class": "_18ToE"})
    locations = soup.find_all("span", {"class": "_3DYbK"})
    url_1=soup.find_all("a",class_="_2kfVy")
    #============================================================================
    for k in names:
        name = k.text
        car_names.append(name)
    #--------------------------------------------------------------------------------------------------
    for ul_tag in types:
        li_tags = ul_tag.find_all("li")
        if li_tags[0] is None:
            li_0="Not Available"
            type1_data.append(li_0)
        else:
            type1_data.append(li_tags[0].text.strip())
        if li_tags[2] is None:
            type2_data.append('N/A')
        else:
            type2_data.append(li_tags[2].text.strip())
    #-----------------------------------------------------------------------------------------------------
    for k in runs:
        run = k.find_all("li")
        if run[0] is None:
            run_0 = "Not Available"
            car_runs.append(run_0)
        else:
            car_runs.append(run[0].text.strip())
        #========================================
        if run[1] is None:
            run_1="Not Available"
            car_owner.append(run_1)
        else:
            car_owner.append(run[1].text.strip())
        #========================================
        if run[2] is None:
            run_2="Not Available"
            engine.append(run_2)
        else:
            engine.append(run[2].text.strip())
        #========================================
        if run[3] is None:
            run_3 = "Not Available"
            num_plate.append(run_3)
        else:
            num_plate.append(run[3].text.strip())
    #====================================================================================================================
    for k in zpay:
        pay = k.strong.text
        if pay is None:
            pay_new="Not Available"
            car_zpay.append(pay_new)
        else:
            car_zpay.append(pay)
    #=====================================================================================================================================================
    for k in price:
        n_price = k.span.text
        if n_price is None:
            price_up="Not Available"
            car_prices.append(price_up)
        else:
            car_prices.append(n_price)
    #=================================================================================================================================
    for k in price:
        prices = k.p
        if prices is None:
            price_n = "Not Available"
            car_ori_prices.append(price_n)
        else:
            price_n=prices.text
            car_ori_prices.append(price_n)
    #=========================================================================================================================================
    for k in locations:
        location = k.text
        if location=='':
            car_locations.append('N/A')
        else:
            car_locations.append(location)
    #---------------------------------------------------------------------------------------------------------------
    for k in url_1:
        url_n=k.get("href")
        url_redirect.append(url_n)
        img1=k.find('div').span.img
        if img1 != None:
            img_redirect.append(img1.get('src'))
        else:
            img_redirect.append('N/A')
    print("-------------------")
#---------------------------------------------------------------------------------------------------------------
for m in range(len(car_names)):
  car_info = car_names[m] + ' ' + type1_data[m]
  car_infos.append(car_info)
#--------------------------------
print(img_redirect)
print(len(img_redirect))
print(len(car_names))

try:
  create_table = "create table cars24_cars (Source varchar(255), Car_names varchar(255), Transmission varchar(255), Price_before_discount varchar(255), Car_price varchar(255), Run_km varchar(255), Car_location varchar(255), Car_owner varchar(255),Fuel_type varchar(255), Downpayment varchar(255), Num_plate varchar(255), Url varchar(1500),Img varchar(1500))"
  cursor.execute(create_table)
  insert_query = "INSERT INTO cars24_cars (Source, Car_Names,Price_before_discount, Car_price,Transmission, Run_km, Car_location, Car_owner, Fuel_type,Downpayment,Num_plate, Url,Img) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)"
  data_to_insert = []
  for i in range(len(car_locations)):
      data_to_insert.append(("cars24.com", car_infos[i], car_ori_prices[i], car_prices[i], type2_data[i], car_runs[i], car_locations[i], car_owner[i], engine[i], car_zpay[i], num_plate[i], url_redirect[i],img_redirect[i]))

  cursor.executemany(insert_query, data_to_insert)
  connection.commit()
except:
  truncate = "truncate table cars24_cars"
  cursor.execute(truncate)
  insert_query = "INSERT INTO cars24_cars (Source, Car_Names,Price_before_discount, Car_price,Transmission, Run_km, Car_location, Car_owner, Fuel_type,Downpayment,Num_plate, Url,Img) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)"
  data_to_insert = []
  for i in range(len(car_locations)):
      data_to_insert.append(("cars24.com", car_infos[i], car_ori_prices[i], car_prices[i], type2_data[i], car_runs[i], car_locations[i], car_owner[i], engine[i], car_zpay[i], num_plate[i], url_redirect[i],img_redirect[i]))
  cursor.executemany(insert_query, data_to_insert)
  connection.commit()

driver.quit()
