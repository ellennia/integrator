#!/usr/bin/python
# -*- encoding: UTF-8 -*-

'''
    Structure

    Classes:
        - class Frame
        - class Account
        - class Cache
'''

import time

import necu

'''
    An entire persons online banking account.
    Has more accounts (savings/checking etc.) can be attached
    to this Frame.
'''
class Frame():
    def __init__(self, account_data):
        self.accounts = [Account(tpl) for tpl in account_data]
        self.time = time.time()

    def count(self):
        return len(self.accounts)

    def available(self):
        return sum([acc.available for acc in self.accounts])

    def total(self):
        return sum([acc.total for acc in self.accounts])

    '''
        Prints a summary of a person's NECU account information
        from one account frame to the output stream.
    '''
    def summary(self, institution):
        print('## {} Accounts Information'.format(institution))
        print('      (' + str(self.count()) + ') accounts found')

        for account in self.accounts:
            print('         {} account: Available ${} | Total: ${}'
                    .format(account.name, account.available, account.total))

        print('     Total available money: ${}'.format(self.available()))
        print('     Total money: ${}'.format(self.total()))
        print('## End {} Accounts Information'.format(institution))

'''
    A single bank account. Either checking or savings.
'''
class Account():
    def __init__(self, data):
        self.data = data
        self.name = data[0]
        self.available = data[1]
        self.total = data[2]
        self.transactions = []
        self.fetched_transactions = False

    def recent_transactions(self):
        if self.fetched_transactions == False:
            pass
        return self.transactions

'''
    Store a collection of Frames.
    This is so the program can look back at account history every time.
    Should add a new frame roughly every minute when connected to
    the Internet.
'''
class Cache():
    def __init__(self, browser):
        self.frames = []
        self.browser = browser # This is neccessary to manipulate the NECU browser

    '''
        Adds a new frame to the cache.
    '''
    def add_frame(self, summ):
        self.frames.append(summ)

    '''
        Returns the most recently added frame.
    '''
    def present(self):
        return self.frames[len(self.frames) - 1]

    '''
        Returns the Unix time that the cache was 
        last updated.
    '''
    def last_update(self):
        return self.present().time

    '''
        Returns the number of frames stored in this
        database.
    '''
    def framecount(self):
        return len(self.frames)

    ''' Returns whether or not the user's total available balance
        has gone up or down since the previous frame.

        -1 equals down
        0 equals stayed the same
        1 equals risen
    '''
    def trend(self):
        if self.framecount <= 2:
            return 0
        else:
            prev = self.frames[len(self.frames - 2)]
            curr = self.present()

            difference = curr.available() - prev.available()
            if difference == 0: return 0
            else: return difference / abs(difference)

    '''
        Checks whether a new frame has been added to the cache
        in the last minute.

        If one hasn't been, then ask the bank driver for another.
    '''
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
            self.add_frame(necu.fetch_accounts(self.browser, False, ('is', 'ignored')))
            print('Frame count: {}'.format(len(self.frames)))
        else:
            print('No fetch needed: {} seconds elapsed since last fetch (60 needed)'.format(time.time() - self.last_update()))

