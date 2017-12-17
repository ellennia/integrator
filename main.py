'''
    Integrator - A flask-based personal web app to Integrate financial and other
        relevant information.

    Todo:
        - Use PhantomJS instead of Firefox
        - Add JS to web page to automatically refresh the page every 10 seconds, or at least the data.
        - Use Markdown and prettify the HTML output.
        - Store account data in a sqlite3 database so reloading doesn't necessarily fetch (SQLAlchemy)

    Creates a web page that will auto-update to get bank information.
    It will then display that data meaningfully.
'''

from os import environ
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
    for account in summarizer.accounts:
        print('         {} account: Available ${} | Total: ${}'.format(account.name, account.available, account.total))
    print('     Total available money: ${}'.format(summarizer.available()))
    print('     Total money: ${}'.format(summarizer.total()))
    print('## End NECU Accounts Information')

class Cache():
    def __init__(self):
        self.frames = []

    def add_frame(self, summ):
        self.frames.append(summ)

    def last_update(self):
        return self.present().time

    def present(self):
        return self.frames[len(self.frames) - 1]

    def ping(self):
        global login_info

        need_fetch = False

        # If it has been a minute since the current cached date was retrieved,
        # sets the boolean to indicate that new data is needed.
        if self.last_update() < time.time() - 60: 
            need_fetch = True

        # If cache was marked expired, it loads website data again to renew the cache.
        if need_fetch:
            print('Cache expired, updating NECU data...')
            self.add_frame(fetch_necu_accounts(False, login_info))
            print('Frame count: {}'.format(len(self.frames)))
        else:
            print('No fetch needed: {} {}'.format(self.last_update(), time.time()))

cache = Cache()

print('Starting Integrator | OS user account name: \'{}\''.format(environ.get('USERNAME')))
login_info = (environ.get('NECU_Account'), environ.get('NECU_Password'))
app = Flask(__name__) # Initialize Flask
print('Contacting NECU and downloading account info...')
cache.add_frame(fetch_necu_accounts(True, login_info))
print('Startup NECU fetch completed.')
cli_account_summary(cache.present()) # Prints out info to the console

'''
    The main page of the web app.
'''
@app.route('/')
def integrator():
    page = ''
    cache.ping()
    frame = cache.present()

    page += '<h2>Account details:</h2>'
    for account in frame.accounts:
        page += '{}: <b>${}</b> available, ${} present<br>\n'.format(account.name, account.available, account.total)
    page += 'Total available: <b>${}</b><br>'.format(frame.available())
    page += 'Total present: ${}<p>'.format(frame.total())
    return page + '<hr><center><font size="144"><b>Ellen\'s accounts total: ${}</b></font></center><hr>'.format(frame.available())

app.run(debug=False, host='0.0.0.0', port=80)
