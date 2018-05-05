import sqlite3 as sq
import datetime as dt

from contextlib import contextmanager

@contextmanager
def cursor():
    try:
        conn = sq.connect('bot.db')
        cur = conn.cursor()
        yield cur
        conn.commit()
    finally:
        conn.close()


def addRip(type, rip, channel, creator):
    with cursor() as cur:
        date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute('INSERT INTO Rip values(?, ?, ?, ?, ?)',
        (rip, type, date, channel, creator))

def delRip(delrip):
    with cursor() as cur:
        cur.execute('DELETE FROM Rip WHERE type = ? and rip = ?', (delrip))


def readRips():
    with cursor() as cur:
        cur.execute('SELECT type, rip, channel from Rip')
        rows = cur.fetchall()
        data = {}
        for row in rows:
            type, rip, channel = row
            if channel not in data:
                data[channel] = set()
            data[channel].add((type, rip))
        return data

def readViisaudet():
    with cursor() as cur:
        cur.execute('SELECT viisaus from Viisaus')
        rows = cur.fetchall()
        return set(rows)
