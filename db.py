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

def readSanat():
    with cursor() as cur:
        cur.execute('SELECT sana from Sana')
        rows = cur.fetchall()
        return set(rows)

def upsertOppi(keyword, definition, channel, creator):
    with cursor() as cur:
        date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute('INSERT OR REPLACE INTO Oppi values(?, ?, ?, ?, ?)',
        (keyword, definition, date, channel, creator))

def findOppi(keyword, channel):
    with cursor() as cur:
        cur.execute('SELECT definition FROM Oppi WHERE keyword=? and channel=?', (keyword, channel))
        return cur.fetchone()

def countOpis(channel):
    with cursor() as cur:
        cur.execute('SELECT COUNT(*) AS count FROM Oppi WHERE channel=?', (channel,))
        count = cur.fetchone()
        return count

def randomOppi(channel):
    with cursor() as cur:
        cur.execute('SELECT keyword, definition FROM Oppi WHERE channel=? ORDER BY RANDOM() LIMIT 1', (channel,))
        return cur.fetchone()
