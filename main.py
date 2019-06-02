import os
import pandas
import selenium
import time


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
    


if __name__ == '__main__':
	driver = define_driver(CHROMEDRIVER_LOCATION)
	open_webpage(driver,turismocity)
	click_element_by_xpath(driver,CLICK_INPUT_ORIGIN_CITY)
	send_keys_by_xpath(driver,INPUT_TEXT_FROM_CITY,'Buenos Aires, Argentina')
	click_element_by_xpath(driver,CLICK_INPUT_DESTINATION_CITY)
	send_keys_by_xpath(driver,INPUT_TEXT_DESTINATION_CITY,destination)
	click_element_by_xpath(driver, DATE_NOT_DECIDED_YET)
	click_element_by_xpath(driver, SEARCH_BUTTON)
