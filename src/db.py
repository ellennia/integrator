import sqlite3

import cache

conn = sqlite3.connect('necu.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS frames (id int, time text)')
c.execute('CREATE TABLE IF NOT EXISTS accounts (id int, frame_id int, name text, available text, total text)')

print('Created tables.')

'''
    Todo: Need Frame/Account classes to auto-generate/track IDs
'''
def write_frame(frame):
    global c

    f_id = frame.id
    c.execute("INSERT INTO frames ('{}', '{}')".format(f_id, str(frame.time))

    for account in frame.accounts:
        data = account.data
        c.execute("INSERT INTO accounts ('{}', '{}', '{}', '{}', '{}')"
            .format(account.id, f_id, data.name, data.available, data.total)

