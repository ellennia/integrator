#!/usr/bin/python
# -*- encoding: UTF-8 -*-

'''
    Integrator : main.py 
        A flask-based 'one-page' personal web app to integrate financial and other
        relevant information. This file in particular is the main Python script, 
        from which the application starts. Primarily contains web related code. 
        Starts a server on: http://localhost:80.

    Todo:
        - 1. Store account data in a sqlite3 database so reloading script doesn't necessarily require fetch. (SQLAlchemy?).
        - Weather: Use OpenWeatherMap in weather.py to fetch weather information. Has very simple Python API
        - Transactions: Fetch transactions from NECU. By extension, make sound when transaction occurs. Need to have PhantomJS download the file
        - Gas prices: Get gas prices somehow. AAA?
        - Etc: Rely more on /api
        - Scrape grocery data from Hannaford website
''' 

# Python standard library imports
from decimal import *
from datetime import datetime
from os import environ # Used to fetch personal information that shouldn't be hardcoded into this code.
import markdown # Used to format some of the home page.
import thread # Threads used to run website scrape code in parallel with web frontend.
import sqlite3 # Actually not currently used here at all. Will remove if it is not in the future.
import time
import json

# Third party libraries imports
from flask import Flask, Markup, render_template
from selenium import webdriver
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from forex_python.converter import CurrencyRates # From fixer.io, updated every day at 3PM

# Local (project) imports
from cache import *
from weather import *
from alarm import *
from work import *
import necu

print('Starting Integrator [Imports successful] ; OS user account name: \'{}\''.format(environ.get('USERNAME')))
app = Flask(__name__) # Initialize Flask

engine = create_engine('sqlite:///necu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

loaded_data = False
requests = 0
alarms = []

'''
    The main page
'''
@app.route('/')
def integrator():
    global requests
    global loaded_data
    global cache

    if loaded_data:
        requests += 1
        cache.ping()
        frame = cache.present()
        account_name = 'Ellen'

        page = '' # NECU account information
        # Markdown
        for account in frame.accounts:
            page += '+ {}, ${}, ${}<br>\n'.format(account.name, account.available, account.total)
        page += 'Total: ${}<p>\n'.format(frame.total())

        page2 = '' # Forex/fixer.io data, and page load data
        cr = CurrencyRates(force_decimal = True)
        euro_conv = cr.convert('USD', 'EUR', frame.available())
        yen_conv = cr.convert('USD', 'JPY', frame.available())
        page2 += '+ Euro: {}\n + Yen: {}\n'.format(euro_conv, yen_conv)

        dataset_1_necu = Markup(markdown.markdown(page))
        dataset_2_forex = Markup(markdown.markdown(page2))
        return render_template('home.html', 
                user = account_name, 
                balance = str(frame.available()),
                data = dataset_1_necu,
                forex_data = dataset_2_forex,
                rcount = str(requests),
                fcount = str(cache.framecount())
                )
    else:
        return render_template('cold.html')

'''
    Data retrieve and submit function.
'''
@app.route('/api', methods = ['POST'])
def info_fetcher():
    function = '' # Post or get
    label = '' # The piece of data being retrieved
    internal_api(label)


def internal_api(query):
    # Returns the newest Frame, jsonified
    if query == 'necu':
        cache.ping()
        return cache.present().jsonify()

    # Returns a JSON representation of the current weather from OpenWeatherMap.
    elif query == 'weather':
        return get_weather('Dover, NH')

    return 'Unknown query'

#def threadd():
#    app.run(debug=False, host='0.0.0.0', port=80)
#thread.start_new_thread(threadd,())

def nescrape():
    global loaded_data
    global cache

    print('Starting Webdriver/PhantomJS...')
    browser = webdriver.PhantomJS('../tools/phantomjs.exe')
    print('Webdriver started.')
    cache = Cache(browser)
    print('Cache initialized.')

    weather = internal_api('weather')
    print(weather)

    # NECU stuff
    start_time = time.time()
    print('Contacting NECU and downloading account info...')

    frame = necu.fetch_accounts(
            browser, 
            True, 
            (environ.get('NECU_Account'), environ.get('NECU_Password'))
            )
    session.add(frame)
    session.commit()
    cache.add_frame(frame)

    loaded_data = True
    end_time = time.time()
    print('Initialization NECU fetch completed. Time: {} seconds'.format(end_time - start_time))
    cache.present().summary('NECU') # Prints out account info to the console.
thread.start_new_thread(nescrape,())

print('Web server starting.')
app.run(debug=False, host='0.0.0.0', port=80)
