#!/usr/bin/python
# -*- encoding: UTF-8 -*-

'''
    Integrator : main.py - 
        A flask-based personal web app to Integrate financial and other
        relevant information. This file in particular is the main Python
        script, from which the application starts. Primarily contains web
        related code.

    Todo:
        - Use PhantomJS instead of Firefox
        - Add JS to web page to automatically refresh the page every 10 seconds, or at least the data.
        - Use Markdown and prettify the HTML output.
        - Store account data in a sqlite3 database so reloading doesn't necessarily fetch (SQLAlchemy)

    Functions planned to be added to the home page:
        - A big clock that is realtime
        - Instant translation of account balances to Euro and Yen using forex-python
        - Fetch weather data from somewhere
        - Fetch commodity prices, such as oil
''' 

from os import environ
from decimal import *
import time
import sqlite3
import markdown

from flask import Flask, Markup, render_template

from necu import *
from cache import *

print('Starting Integrator (Import successful) | OS user account name: \'{}\''.format(environ.get('USERNAME')))
app = Flask(__name__) # Initialize Flask
cache = Cache()

'''
    The main page of the web app.
'''
@app.route('/')
def integrator():
    cache.ping()
    frame = cache.present()

    # Markdown
    page = '### Integrator Webapp\n'
    page += '## Ellen\'s NECU Account Details\n'
    for account in frame.accounts:
        page += '+ {}: ${} available, ${} present<br>\n'.format(account.name, account.available, account.total)
    page += 'Total available: <b>${}</b><br>\n'.format(frame.available())
    page += 'Total present: ${}<p>\n'.format(frame.total())
    page += '# Time: {}\n'.format(time.time())
    page += '# Ellen\'s Balance ${}\n'.format(frame.available())
    page += '#### Forex data (equivalents): Euro: {} - Yen: {}'.format('0', '0')
    markdown_portion = markdown.markdown(page)
    # End markdown

    #template = render_template('home.html')
    #somehow combine template and markdown, don't recall how

    return '<title>Integrator</title><body><center>' + markdown_portion

'''
    Data retrival and submit function
'''
@app.route('/api', methods = ['POST'])
def info_fetcher():
    function = '' # Post or get
    label = '' # The piece of data being retrieved

    if label == 'necu_data':
        cache.ping()
        return cache.present().jsonify()
    elif label == 'weather_data':
        pass
        #weather.ping()
        #return weather.jsonify()
    return 'Unknown label'

# NECU stuff
print('Contacting NECU and downloading account info...')
login_info = (environ.get('NECU_Account'), environ.get('NECU_Password'))
cache.add_frame(fetch_necu_accounts(True, login_info))
print('Startup NECU fetch completed.')
cache.present().summary('NECU') # Prints out account info to the console.

app.run(debug=False, host='0.0.0.0', port=80)
