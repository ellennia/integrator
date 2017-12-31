from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def go_to_episode(count):
    browser = webdriver.Firefox()
    print 'Webdriver started'
    url = 'https://www.hulu.com/sailor-moon'
    browser.get(url)
    browser.implicitly_wait(10)

    elms = browser.find_elements_by_class_name('next')
    print len(elms)
    for i in range(0, 10):
        elms[1].send_keys(Keys.RETURN)
        browser.implicitly_wait(10)


go_to_episode(111)
