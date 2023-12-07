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

#===========================================================================================


#cardekho

car_names = []
type1_data = []
type2_data = []
type3_data = []
car_runs = []
engine=[]
num_plate=[]
car_zpay = []
car_prices = []
total_column = []
url_r=[]
img_url=[]
page_url=[]
#==============================================================
page_url.append("https://www.cardekho.com/used-cars+in+ahmedabad")
page_url.append("https://www.cardekho.com/used-cars+in+bangalore")
page_url.append("https://www.cardekho.com/used-cars+in+mumbai")
page_url.append("https://www.cardekho.com/used-cars+in+jaipur")
page_url.append("https://www.cardekho.com/used-cars+in+gurgaon")
page_url.append("https://www.cardekho.com/used-cars+in+delhi-ncr")
page_url.append("https://www.cardekho.com/used-cars+in+chennai")
page_url.append("https://www.cardekho.com/used-cars+in+pune")
page_url.append("https://www.cardekho.com/used-cars+in+hyderabad")
page_url.append("https://www.cardekho.com/used-cars+in+kolkata")
page_url.append("https://www.cardekho.com/used-cars+in+agra")
page_url.append("https://www.cardekho.com/used-cars+in+lucknow")
page_url.append("https://www.cardekho.com/used-cars+in+chandigarh")
page_url.append("https://www.cardekho.com/used-cars+in+kanpur")
page_url.append("https://www.cardekho.com/used-cars+in+bhubaneswar")
page_url.append("https://www.cardekho.com/used-cars+in+dehradun")
page_url.append("https://www.cardekho.com/used-cars+in+rajkot")
page_url.append("https://www.cardekho.com/used-cars+in+surat")
page_url.append("https://www.cardekho.com/used-cars+in+vadodara")
page_url.append("https://www.cardekho.com/used-cars+in+ludhiana")

#===============================================================================
for t in page_url:
    driver.get(t)
    #-----------------------------------------------------------------
    while True:
        height = driver.execute_script("return document.body.scrollHeight")
        for i in range(0,100,1):
            ni = i/100
            script = f"window.scrollTo(0, document.body.scrollHeight*{ni});"
            driver.execute_script(script)
            if i >90:
                time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if height == new_height:
            break
    for t in range(1,100,1):
      ni = t/100
      script = f"window.scrollTo(0, document.body.scrollHeight*{ni});"
      driver.execute_script(script)
      time.sleep(1)
    print("--------------------------------------------------------------------------")
    soup = BeautifulSoup(driver.page_source,'lxml')
    column = soup.find_all("div",class_="ClsBox")
    #====================================================================
    for l in column:
        col = l.find_all("div",class_="gsc_col-xs-12 gsc_col-sm-6 gsc_col-md-4 cardColumn")
        if col != None:
            for j in col:
                total_column.append(j)
    #--------------------------------------------------------------------------------------------------------------
                names = j.find_all("h3", class_= "title")
                for k in names:
                    name = k.a.text
                    car_names.append(name)
                    url_n=k.a.get("href")
                    url_t="https://www.cardekho.com"+url_n
                    url_r.append(url_t)
    #---------------------------------------------------------------------------------------------
                types = j.find_all("div", {"class": "dotsDetails"})
                for ul_tag in types:
                    div_tag=ul_tag.text
                    pieces = [piece.strip() for piece in div_tag.split('•')]
                    type_1=pieces[0]
                    type_3=pieces[1]
                    type_2=pieces[2]
                    type1_data.append(type_1)
                    type2_data.append(type_2)
                    type3_data.append(type_3)
    #============================================================
                img_= j.find_all("div",class_="imagebox hover")
                for im in img_:
                    ur=im.find("img").get("src")
                    img_url.append(ur)
    #===========||=====================================================================
                zpay = j.find_all("div", {"class": "emitext hover"})
                for k in zpay:
                    pay = k
                    if pay is None:
                        pay_new="Not Available"
                        car_zpay.append(pay_new)
                    else:
                        car_zpay.append(pay.text)
    #===========||=======================================================
                price = j.find_all("div", {"class": "Price hover"})
                for k in price:
                    n_price = k.text
                    if n_price is None:
                        price_up="Not Available"
                        car_prices.append(price_up)
                    else:
                        car_prices.append(n_price)
    #---------------------------------------------------------------------------------------------------------------
try:
  create_table = "create table cardekho_cars (Source varchar(255), Car_names varchar(255), Transmission varchar(255), Car_price varchar(255), Run_km varchar(255), Fuel_type varchar(255), Downpayment varchar(255), Url varchar(1500), Img_Url varchar(1500))"
  cursor.execute(create_table)
  insert_query = "INSERT INTO cardekho_cars (Source, Car_Names, Car_price,Transmission, Run_km, Fuel_type, Downpayment, Url, Img_Url) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s,%s)"
  data_to_insert=[]
  for i in range(len(car_names)):
    data_to_insert.append(("cardekho.com", car_names[i], car_prices[i], type2_data[i], type1_data[i], type3_data[i],car_zpay[i],url_r[i],img_url[i]))
  cursor.executemany(insert_query, data_to_insert)
  connection.commit()
  print("Data inserted successfully")
except:
  truncate = "truncate table cardekho_cars"
  cursor.execute(truncate)

  insert_query = "INSERT INTO cardekho_cars (Source, Car_Names, Car_price,Transmission, Run_km, Fuel_type, Downpayment, Url, Img_Url) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s,%s)"
  data_to_insert=[]
  for i in range(len(car_names)):
    data_to_insert.append(("cardekho.com", car_names[i], car_prices[i], type2_data[i], type1_data[i], type3_data[i],car_zpay[i],url_r[i],img_url[i]))
  cursor.executemany(insert_query, data_to_insert)
  connection.commit()
  print("Data inserted successfully")

driver.quit()
