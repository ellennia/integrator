from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import environ

'''
    Currently will not work because it requires a cell
    phone text code to be entered when the selenium
    webdriver bot connects- it has no cookies in the browser
    and therefore thinks this is a 'new computer' every time.
'''
def pay_car_bill():
    url = 'https://dcu.org'
    browser = webdriver.Firefox()
    browser.get(url)

    username_box = browser.find_element_by_name('userid')
    password_box = browser.find_element_by_name('password')

    username_box.send_keys(environ.get('DCU_Account'))
    password_box.send_keys(environ.get('DCU_Password') + Keys.RETURN)

    browser.implicitly_wait(10)

    accounts = browser.find_element_by_class('home-link-text')
    accounts.send_keys(Keys.RETURN)

pay_car_bill()
