'''
    Integrator - A flask-based personal web app to Integrate financial and other
        relevant information.

    Todo:
        - Use PhantomJS instead of Firefox
        - Add JS to web page to automatically refresh the page.
        - Use Markdown and prettify the HTML output
        - Store account data in a sqlite3 database so reloading doesn't necessarily fetch

    Creates a web page that will auto-update to get bank information.
    It will then display that data meaningfully.
'''

from os import environ
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from decimal import *
import time
from flask import Flask
import sqlite3

'''
    An entire person's online banking account.
    Has more 'accounts' (savings/checking etc.) can be attached
    to this AccountSummarizer.
'''
class AccountSummarizer():
    def __init__(self, account_tuples):
        self.accounts = [Account(tpl) for tpl in account_tuples]
        self.time = time.time()

    def count(self):
        return len(self.accounts)

    def available(self):
        return sum([acc.available for acc in self.accounts])

    def total(self):
        return sum([acc.total for acc in self.accounts])

'''
    A single bank account. Either checking or savings.
'''
class Account():
    def __init__(self, tpl):
        self.data = tpl
        self.name = tpl[0]
        self.available = tpl[1]
        self.total = tpl[2]

    def recent_transactions():
        pass

'''
    Log into, then scrape NECU's website for account information.
    The username and password are retrieved from environmental variables.
'''
def fetch_necu_accounts():
    # Login in to my necu account with selenium/firefox
    necu_url = 'https://www.netteller.com/login2008/Authentication/Views/Login.aspx?returnUrl=%2fnecu'
    browser = webdriver.Firefox()
    browser.get(necu_url)

    username_box = browser.find_element_by_name('ctl00$PageContent$Login1$IdTextBox')
    username_box.send_keys(environ.get('NECU_Account') + Keys.RETURN)
    browser.implicitly_wait(10)

    password_box = browser.find_element_by_name('ctl00$PageContent$Login1$PasswordTextBox')
    password_box.send_keys(environ.get('NECU_Password') + Keys.RETURN)
    browser.implicitly_wait(10)

    try:
        browser.find_element_by_id('ctl00_ctl26_retailSecondaryMenuAccountTransactionsMenuItemLinkButton').send_keys(Keys.RETURN)
        browser.implicitly_wait(10)
    except: pass

    # Scraping code,  gets the balances of my checking and savings accounts.
    melements = browser.find_elements_by_class_name('POMoneyTableData')
    money_amounts = [Decimal(melement.get_attribute('innerHTML')[1:]) for melement in melements]

    # Get to the downloads page
    downloads = browser.find_element_by_id('ctl00_ctl27_retailSecondaryMenuAccountTransactionsMenuItemLinkButton')
    downloads.send_keys(Keys.RETURN)
    browser.implicitly_wait(10)
    dl = browser.find_element_by_id('ctl00_ctl26_retailTransactionsTertiaryMenuDownloadMenuItemLinkButton')
    dl.send_keys(Keys.RETURN)
    browser.implicitly_wait(10)

    ac = browser.find_element_by_id('ctl00_PageContent_ctl00_Template_accountsDropDownList')
    ac.send_keys(Keys.DOWN)

    rng = browser.find_element_by_id('ctl00_PageContent_ctl00_Template_rangeDropDownList')
    rng.send_keys(Keys.DOWN)

    form = browser.find_element_by_id('ctl00_PageContent_ctl00_Template_formatDropDownList')
    for i in range(0, 7):
        form.send_keys(Keys.DOWN)

    submit_button = browser.find_element_by_id('ctl00_PageContent_ctl00_Template_submitButton')
    submit_button.send_keys(Keys.RETURN)

    accounts = []
    accounts.append(('Savings', money_amounts[0], money_amounts[1]))
    accounts.append(('Checking', money_amounts[2], money_amounts[3]))

    return AccountSummarizer(accounts)

'''
    Print out a summary of a person's NECU account information
    out to the console.
'''
def cli_account_summary(accounts):
    print('## NECU Accounts Information')
    print('      (' + str(accounts.count()) + ') accounts found')
    for account in accounts.accounts:
        print('         {} account: Available ${} | Total: ${}'.format(account.name, account.available, account.total))
    print('     Total available money: ${}'.format(accounts.available()))
    print('     Total money: ${}'.format(accounts.total()))
    print('## End NECU Accounts Information')

# Initialize Flask
print('Starting Integrator | OS user account name: \'{}\''.format(environ.get('USERNAME')))
app = Flask(__name__)

''' Check when the local copy of the NECU account info was last updated.
    If it was over 1 minute ago, contact NECU and update it again. '''
def ping_necu():
    global accounts
    need_fetch = False

    # Refresh data every minute
    if accounts.time < time.time() - 60: 
        need_fetch = True

    if need_fetch:
        print('Cache expired, updating NECU data...')
        accounts = fetch_necu_accounts()
    else:
        print('No fetch needed: {} {}'.format(accounts.time, time.time()))

'''
    The main page of the web app.
'''
@app.route('/')
def integrator():
    page = ''
    ping_necu()
    for account in accounts.accounts:
        page += '{}: <b>${}</b> available, ${} present<br>\n'.format(account.name, account.available, account.total)
    page += 'Total available: <b>${}</b><br>'.format(accounts.available())
    page += 'Total present: ${}<p>'.format(accounts.total())
    return page + '<font size="144"><b>${}</b></font>'.format(accounts.available())

print('Contacting NECU and downloading account info...')
accounts = fetch_necu_accounts()
print('Startup NECU fetch completed.')
cli_account_summary(accounts) # Print out info to the console
app.run(debug=False, host='0.0.0.0', port=80)
