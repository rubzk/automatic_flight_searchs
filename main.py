import os
import pandas
import selenium
import time

import requests
import lxml.html as lh
import pandas as pd


##-----------Web Page and ChromeDriver Path-------------##

turismocity = 'https://www.turismocity.com.ar/'
CHROMEDRIVER_LOCATION="C:\\Users\\tertola\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Python 3.7\\chromedriver.exe"


##------------Select the Origin City input box-----------##

CLICK_INPUT_ORIGIN_CITY = '//*[@id="flights-tab-container"]/form/div[2]/div/div[2]/div/div/div/span'
INPUT_TEXT_FROM_CITY = '//*[@id="flights-tab-container"]/form/div[2]/div/div[2]/div/div/span/span/span[1]/input'

##------------Select the destination City Input box---------##

CLICK_INPUT_DESTINATION_CITY = '//*[@id="flights-tab-container"]/form/div[2]/div/div[3]/div/div/div/span/span'
INPUT_TEXT_DESTINATION_CITY = '//*[@id="flights-tab-container"]/form/div[2]/div/div[3]/div/div/span/span/span[1]/input'

destination = 'Rio de Janeiro, Brasil'


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


if __name__ == '__main__':
  driver = define_driver(CHROMEDRIVER_LOCATION)
  open_webpage(driver,turismocity)
  click_element_by_xpath(driver,CLICK_INPUT_ORIGIN_CITY)
  send_keys_by_xpath(driver,INPUT_TEXT_FROM_CITY,'Buenos Aires, Argentina')
  click_element_by_xpath(driver,CLICK_INPUT_DESTINATION_CITY)
  send_keys_by_xpath(driver,INPUT_TEXT_DESTINATION_CITY,destination)
  wait_presence_of_element_by_xpath(driver, DATE_NOT_DECIDED_YET)
  click_element_by_xpath(driver, DATE_NOT_DECIDED_YET)
  click_element_by_xpath(driver, SEARCH_BUTTON)
  wait_presence_of_element_by_xpath(driver, LOG_IN_AD)
  click_element_by_xpath(driver, LOG_IN_AD)
  url = driver.current_url
  page = requests.get(url)
  doc = lh.fromstring(page.content)
  tr_elements = doc.xpath('//tr')
  #Create empty list
  col=[]
  i=0
  #For each row, store each first element (header) and an empty list
  for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    print (i,name)
    col.append((name,[]))



