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
#=========================================================================================

#spinny
car_names = []
type1_data = []
car_runs = []
engine=[]
car_zpay = []
car_prices = []
car_locations = []
url_redirect=[]
img_redirect=[]
page_url=[]
#--------------------------------------------------------------
page_url.append("https://www.spinny.com/used-cars-in-delhi-ncr/s/")
page_url.append("https://www.spinny.com/used-cars-in-bangalore/s/")
page_url.append("https://www.spinny.com/used-cars-in-hyderabad/s/")
page_url.append("https://www.spinny.com/used-cars-in-mumbai/s/")
page_url.append("https://www.spinny.com/used-cars-in-pune/s/")
page_url.append("https://www.spinny.com/used-cars-in-delhi/s/")
page_url.append("https://www.spinny.com/used-cars-in-gurgaon/s/")
page_url.append("https://www.spinny.com/used-cars-in-noida/s/")
page_url.append("https://www.spinny.com/used-cars-in-ahmedabad/s/")
page_url.append("https://www.spinny.com/used-cars-in-chennai/s/")
page_url.append("https://www.spinny.com/used-cars-in-kolkata/s/")
page_url.append("https://www.spinny.com/used-cars-in-lucknow/s/")
page_url.append("https://www.spinny.com/used-cars-in-jaipur/s/")
page_url.append("https://www.spinny.com/used-cars-in-chandigarh/s/")
page_url.append("https://www.spinny.com/used-cars-in-coimbatore/s/")
page_url.append("https://www.spinny.com/used-cars-in-ghaziabad/s/")
page_url.append("https://www.spinny.com/used-cars-in-indore/s/")
page_url.append("https://www.spinny.com/used-cars-in-kochi/s/")
page_url.append("https://www.spinny.com/used-cars-in-surat/s/")
#===============================================================================
for iu in page_url:
    driver.get(iu)
    while True:
        height = driver.execute_script("return document.body.scrollHeight")
        for il in range(1,100,1):
            ni = il/100
            script = f"window.scrollTo(0, document.body.scrollHeight*{ni});"
            driver.execute_script(script)
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
    box=soup.find('div',class_='CarListingDesktop__carListingDesktopWrapper').find_all("div",class_="CarListingDesktop__carListingCarWrapper")
    for t in box:
        names = t.find("div", class_= "styles__yearAndMakeAndModelSection")
        if names == None:
            continue
        else:
            car_names.append(names.text)
    #========================================================================================
        types = t.find("ul", {"class": "styles__otherInfoSection"})
        li_tags = types.find_all("li")
        car_runs.append(li_tags[0].text.strip())
        engine.append(li_tags[1].text.strip())
        type1_data.append(li_tags[2].text.strip())
    #-------------------------------------------------------
        price = t.find("li", {"class": "styles__price"}).text
        car_prices.append(price)
    #===================================================================

        zprice=t.find("li",class_="styles__emiWrap")
        if zprice!=None:
            car_zpay.append(zprice.text)
        else:
            car_zpay.append('N/A')
    #=====================================================================================
        locations = t.find("div", {"class": "TestDriveAvailability__testDriveItem"}).find('div',class_='TestDriveAvailability__changeLocationColor')
        if locations !=None:
            car_locations.append(locations.text)
        else:
            car_locations.append('N/A')
        #==================================================================
        url_1=t.find("a",class_="styles__carImageContainer").get("href")
        url_redirect.append("https://www.spinny.com"+url_1)

        img =t.find("a",class_="styles__carImageContainer").find('img').get('src')
        img_redirect.append(img)
#============================================================================

try:
  create_table = "create table spinny_cars (Source varchar(255), Car_names varchar(255), Transmission varchar(255), Car_price varchar(255), Run_km varchar(255), Car_location varchar(255),Fuel_type varchar(255), Downpayment varchar(255), Url varchar(1500), Img varchar(1500))"
  cursor.execute(create_table)
  insert_query = "INSERT INTO spinny_cars (Source, Car_Names, Car_price,Transmission, Run_km, Car_location, Fuel_type, Downpayment, Url,Img) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
  data_to_insert = []
  for i in range(len(car_locations)):
      data_to_insert.append(("Spinny.com", car_names[i], car_prices[i], type1_data[i], car_runs[i], car_locations[i], engine[i], car_zpay[i], url_redirect[i], img_redirect[i]))

  cursor.executemany(insert_query, data_to_insert)
  connection.commit()
except:
  truncate = "truncate table spinny_cars"
  cursor.execute(truncate)
  insert_query = "INSERT INTO spinny_cars (Source, Car_Names, Car_price,Transmission, Run_km, Car_location, Fuel_type, Downpayment, Url,Img) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
  data_to_insert = []
  for i in range(len(car_locations)):
      data_to_insert.append(("Spinny.com", car_names[i], car_prices[i], type1_data[i], car_runs[i], car_locations[i], engine[i], car_zpay[i], url_redirect[i], img_redirect[i]))
  cursor.executemany(insert_query, data_to_insert)
  connection.commit()
driver.quit()
