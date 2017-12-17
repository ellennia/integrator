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

from decimal import *
import time
import sqlite3

from flask import Flask

from necu import *

'''
    Print out a summary of a person's NECU account information
    out to the console.
'''
def cli_account_summary(summarizer):
    print('## NECU Accounts Information')
    print('      (' + str(summarizer.count()) + ') accounts found')
    for account in accounts.summarizer:
        print('         {} account: Available ${} | Total: ${}'.format(account.name, account.available, account.total))
    print('     Total available money: ${}'.format(summarizer.available()))
    print('     Total money: ${}'.format(summarizer.total()))
    print('## End NECU Accounts Information')


print('Starting Integrator | OS user account name: \'{}\''.format(environ.get('USERNAME')))
app = Flask(__name__) # Initialize Flask

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
