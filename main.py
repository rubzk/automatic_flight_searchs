import os
import pandas
import selenium
import time
import sqlite3
from datetime import datetime

import requests
import lxml.html as lh
import pandas as pd


##-----------Web Page and ChromeDriver Path-------------##

turismocity = 'https://www.turismocity.com.ar/'


##------------Select the Origin City input box-----------##

CLICK_INPUT_ORIGIN_CITY = '//*[@id="flights-tab-container"]/form/div[2]/div/div[2]/div/div/div/span'
INPUT_TEXT_FROM_CITY = '//*[@id="flights-tab-container"]/form/div[2]/div/div[2]/div/div/span/span/span[1]/input'

##------------Select the destination City Input box---------##

CLICK_INPUT_DESTINATION_CITY = '//*[@id="flights-tab-container"]/form/div[2]/div/div[3]/div/div/div/span/span'
INPUT_TEXT_DESTINATION_CITY = '//*[@id="flights-tab-container"]/form/div[2]/div/div[3]/div/div/span/span/span[1]/input'

destination = ['Rio de Janeiro, Brasil','Madrid','New York','Los Angeles','Tokyo','Amsterdam',  ## Seteo destinos que quiero que el scraper busque
                'Paris']

##-----------I did'nt decide the date yet button------------##

DATE_NOT_DECIDED_YET = '//*[@id="flights-tab-container"]/form/div[2]/div/div[5]/div/div/div'


##-----------Search button-------------------##

SEARCH_BUTTON = '//*[@id="flights-tab-container"]/form/div[5]/div/input'

##-----------Log in Ad----------------##

LOG_IN_AD = '//*[@id="modalLoginImagePopUp"]/div[1]/a/i'




def define_driver(chromedriver_location):
  from selenium import webdriver
  driver = webdriver.Chrome(chromedriver_location)
  return driver


def open_webpage(driver,webpage):
    from selenium import webdriver
    driver.get(webpage)


def send_keys_by_xpath(driver,element_xpath,keys_to_send):
  from selenium import webdriver
  element = driver.find_element_by_xpath(element_xpath)
  element.send_keys(keys_to_send)
  time.sleep(1)
  element.send_keys(u'\ue007')
  time.sleep(0.5)


def click_element_by_xpath(driver,element_xpath):
  from selenium import webdriver
  element = driver.find_element_by_xpath(element_xpath)
  element.click()

def click_element_by_selector(driver, element_selector):
  from selenium import webdriver
  element = driver.find_element_by_css_selector(element_selector)
  element.click()

def wait_presence_of_element_by_xpath(driver,element_xpath):
  from selenium.webdriver.support import expected_conditions as EC
  from selenium.webdriver.support.ui import WebDriverWait
  from selenium.webdriver.common.by import By
  wait = WebDriverWait(driver, 100)
  element = wait.until(EC.element_to_be_clickable((By.XPATH,element_xpath)))


def get_flights_tables(url,destino):
  page = requests.get(url)
  doc = lh.fromstring(page.content)
  tr_elements = doc.xpath('//tr')
  file = []
  col=[]
  i=0
  #For each row, store each first element (header) and an empty list
  for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    col.append((name,[]))

  for j in range (1,len(tr_elements)):
    T = tr_elements[j]
    if len(T) != 7:
      break
    i = 0

    for t in T.iterchildren():

      data=t.text_content()
      if i >0:
        try:
          data=int(data)
        except:
          pass
      col[i][1].append(data)
      i+=1


  dict = {title: column for (title,column) in col}
  df=pd.DataFrame(dict)
  df.columns = ['IDA','VUELTA','ESTADIA','DURACION','ESCALAS','AEROLINEAS','PRECIO']
  df['IDA'] = df['IDA'].map(lambda x: x.lstrip('Lun.MarMiÃ©JuevVieDomSÃ¡b.')) ## Elimino caracteres no deseados
  df['VUELTA'] = df['VUELTA'].map(lambda x: x.lstrip('Lun.MarMiÃ©JuevVieDomSÃ¡b.'))
  df['ESTADIA']=df['ESTADIA'].str.rstrip('dias')
  df['PRECIO']=df['PRECIO'].str.lstrip('$')
  df = df.assign(DESTINY=[destino]*(len(df.index)))
  df = df.assign(SEARCH_DATE=[datetime.today().strftime('%Y-%m-%d')]*(len(df.index)))


  return df

def save_file(filename,datos):
  datos.to_excel(os.environ['USERPROFILE'] + '\\Desktop\\'+filename+".xlsx",header=True, index=False)



def create_connection(db_file):
    """ create a database connection to a SQLite database """

    conn = sqlite3.connect(db_file)
    print(sqlite3.version)


    return conn



if __name__ == '__main__':



  for destinos in destination:
        chromedriver_location = os.environ.get('ChromeDriverLocation')
        driver = define_driver(chromedriver_location)
        open_webpage(driver,turismocity)
        click_element_by_xpath(driver,CLICK_INPUT_ORIGIN_CITY)
        wait_presence_of_element_by_xpath(driver, INPUT_TEXT_FROM_CITY )
        send_keys_by_xpath(driver,INPUT_TEXT_FROM_CITY,'Buenos Aires, Argentina')
        click_element_by_xpath(driver,CLICK_INPUT_DESTINATION_CITY)
        send_keys_by_xpath(driver,INPUT_TEXT_DESTINATION_CITY,destinos)
        wait_presence_of_element_by_xpath(driver, DATE_NOT_DECIDED_YET)
        click_element_by_xpath(driver, DATE_NOT_DECIDED_YET)
        click_element_by_xpath(driver, SEARCH_BUTTON)
        wait_presence_of_element_by_xpath(driver, LOG_IN_AD)
        click_element_by_xpath(driver, LOG_IN_AD)
        conn = create_connection(os.environ.get("DB_Connection"))
        url = driver.current_url
        df = get_flights_tables(url,destinos)
        df.to_sql(name='flights', con=conn, if_exists='append', index=False)
        driver.close()
  p2 = pd.read_sql('select  * FROM flights ORDER BY PRECIO, DESTINY ASC LIMIT 10', conn)
  p2.to_sql(name='daily_f', con=conn, if_exists='replace', index=False)
  print(p2)
