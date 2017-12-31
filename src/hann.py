from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()
print 'Webdriver started'
url = 'http://www.hannaford.com/custserv/locate_store.cmd'
browser.get(url)

elms = browser.find_element_by_class_name('input-text')
elms.send_keys('03820' + Keys.RETURN)
browser.implicitly_wait(10)

elms = browser.find_elements_by_class_name('shopNow')
elms[0].send_keys(Keys.RETURN)

browser.implicitly_wait(10)

search = browser.find_element_by_class_name('keyword-text')
search.send_keys('corn meal' + Keys.RETURN)

browser.implicitly_wait(10)

names = []
for name in browser.find_elements_by_class_name('productName'):
    names.append(name.get_attribute('innerHTML'))

weights = []
for name in browser.find_elements_by_class_name('overline'):
    weights.append(name.get_attribute('innerHTML'))

for i in range(0, len(names)):
    print(names[i] + ': ' + weights[i])
