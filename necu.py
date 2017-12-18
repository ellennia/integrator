#!/usr/bin/python
# -*- encoding: UTF-8 -*-

'''
    'Bank driver'- fetches information from NECU accounts.
'''

from os import environ
from decimal import *
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import cache

def login_necu(browser, login_info):
    # Login in to my necu account with selenium/firefox, and go to the home page.
    necu_url = 'https://www.netteller.com/login2008/Authentication/Views/Login.aspx?returnUrl=%2fnecu'
    browser.get(necu_url)
    username_box = browser.find_element_by_name('ctl00$PageContent$Login1$IdTextBox')
    username_box.send_keys(login_info[0] + Keys.RETURN)
    browser.implicitly_wait(10)
    password_box = browser.find_element_by_name('ctl00$PageContent$Login1$PasswordTextBox')
    password_box.send_keys(login_info[1] + Keys.RETURN)
    browser.implicitly_wait(10)
 
    try:
        browser.find_element_by_id('ctl00_ctl26_retailSecondaryMenuAccountTransactionsMenuItemLinkButton').send_keys(Keys.RETURN)
        browser.implicitly_wait(10)
    except: pass

'''
    Log into, then scrape NECU's website for account information.
    The username and password are retrieved from environmental 
    variables in main.py.

    Returns an Frame object with all the detected Accounts inside.
'''
def fetch_accounts(browser, do_login, login_info):
    if do_login:
        login_necu(browser, login_info)
    else:
        browser.refresh()

    # Scraping code, gets the balances of my checking and savings accounts from the home page.
    melements = browser.find_elements_by_class_name('POMoneyTableData')
    money_amounts = [Decimal(melement.get_attribute('innerHTML')[1:]) for melement in melements]
    accounts = []
    accounts.append(('Savings', money_amounts[0], money_amounts[1]))
    accounts.append(('Checking', money_amounts[2], money_amounts[3]))
    return cache.Frame(accounts)

def fetch_account_summary(browser):
    # Get to the Transactions page
    downloads = browser.find_element_by_id('ctl00_ctl27_retailSecondaryMenuAccountTransactionsMenuItemLinkButton')
    downloads.send_keys(Keys.RETURN)
    browser.implicitly_wait(10)
    # Go to the Transaction Downloads
    dl = browser.find_element_by_id('ctl00_ctl26_retailTransactionsTertiaryMenuDownloadMenuItemLinkButton')
    dl.send_keys(Keys.RETURN)
    browser.implicitly_wait(10)

    # Select the account that data will be retrieved for
    ac = browser.find_element_by_id('ctl00_PageContent_ctl00_Template_accountsDropDownList')
    ac.send_keys(Keys.DOWN)

    # Select the date range to pull from (Since last statement)
    rng = browser.find_element_by_id('ctl00_PageContent_ctl00_Template_rangeDropDownList')
    rng.send_keys(Keys.DOWN)

    # Select 'TXT' as the selected format
    form = browser.find_element_by_id('ctl00_PageContent_ctl00_Template_formatDropDownList')
    for i in range(0, 7):
        form.send_keys(Keys.DOWN)

    # Press enter on the download button
    submit_button = browser.find_element_by_id('ctl00_PageContent_ctl00_Template_submitButton')
    submit_button.send_keys(Keys.RETURN)

