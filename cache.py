import time

from necu import *

'''
    An entire person's online banking account.
    Has more 'accounts' (savings/checking etc.) can be attached
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
    def __init__(self):
        self.frames = []

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
            prevtwo = self.frames[len(self.frames - 2)]
            prev = self.present()

            difference = prev.available() - prevtwo.available()
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
            self.add_frame(fetch_necu_accounts(False, login_info))
            print('Frame count: {}'.format(len(self.frames)))
        else:
            print('No fetch needed: {} {}'.format(self.last_update(), time.time()))

