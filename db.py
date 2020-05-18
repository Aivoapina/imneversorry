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

def insertQuote(quote, quotee, channel, creator):
    with cursor() as cur:
        date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute('INSERT INTO Quote values(?, ?, ?, ?, ?)',
        (quote, quotee, date, channel, creator))

def findQuotes(channel, quotee=None):
    with cursor() as cur:
        if quotee is not None:
            cur.execute('SELECT quote, quotee FROM Quote WHERE channel=? AND upper(quotee) = upper(?)', (channel, quotee))
            return cur.fetchall()
        else:
            cur.execute('SELECT quote, quotee FROM Quote WHERE channel=?', (channel,))
            return cur.fetchall()

def countQuotes(channel):
    with cursor() as cur:
        cur.execute('SELECT count(quote) FROM Quote WHERE channel=?', (channel,))
        return cur.fetchone()[0]

def readDiagnoosit():
    with cursor() as cur:
        cur.execute('SELECT diagnoosi from Diagnoosi')
        rows = cur.fetchall()
        return set(rows)

def readMaidot():
    with cursor() as cur:
        cur.execute('SELECT maito from Maito')
        rows = cur.fetchall()
        return set(rows)

def readNimet():
    with cursor() as cur:
        cur.execute('SELECT nimi from Nimi')
        rows = cur.fetchall()
        return set(rows)

def readKalat():
    with cursor() as cur:
        cur.execute('SELECT kala from Kalat')
        rows = cur.fetchall()
        return set(rows)

def readVihanneet():
    with cursor() as cur:
        cur.execute('SELECT nimi from Vihannes')
        rows = cur.fetchall()
        return set(rows)

def readPlanetoidit():
    with cursor() as cur:
        cur.execute('SELECT nimi from Planetoidi')
        rows = cur.fetchall()
        return set(rows)

def readKulkuneuvot():
    with cursor() as cur:
        cur.execute('SELECT nimi from Kulkuneuvo')
        rows = cur.fetchall()
        return set(rows)

def readLinnut():
    with cursor() as cur:
        cur.execute('SELECT nimi from Linnut')
        rows = cur.fetchall()
        return set(rows)

def readSotilasarvot():
    with cursor() as cur:
        cur.execute('SELECT nimi from Arvonimet')
        rows = cur.fetchall()
        return set(rows)

def readSotilasnimet():
    with cursor() as cur:
        cur.execute('SELECT nimi from Sotilasnimet')
        rows = cur.fetchall()
        return set(rows)

def readEnnustukset():
    with cursor() as cur:
        cur.execute('SELECT rivi from Ennustus')
        rows = cur.fetchall()
        return set(rows)

def readNakutukset():
    with cursor() as cur:
        cur.execute('SELECT nakutus from Nakutukset')
        rows = cur.fetchall()
        return set(rows)

def readDefinitions(channel):
    with cursor() as cur:
        cur.execute('SELECT definition, keyword from Oppi where channel=?', (channel, ))
        rows = cur.fetchall()
        return rows

def upsertTag(tag, target, channel, creator):
    with cursor() as cur:
        date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute('INSERT OR REPLACE INTO Tagit values(?, ?, ?, ?, ?)',
        (tag, target, channel, creator, date))

def findTagged(tag, channel):
    with cursor() as cur:
        cur.execute('SELECT target FROM Tagit WHERE tag=? and channel=?', (tag, channel))
        rows = cur.fetchall()
        return rows

def findTargetTags(target, channel):
    with cursor() as cur:
        cur.execute('SELECT tag FROM Tagit WHERE target=? and channel=?', (target, channel))
        rows = cur.fetchall()
        return rows

def __maybeAddKmNick(nick, cur):
    cur.execute('SELECT EXISTS (SELECT * FROM KilometriNikit WHERE name = ?) as found', (nick,))
    rows = cur.fetchall()
    exists = rows[0][0]
    if (not exists):
        cur.execute('INSERT INTO Kilometrinikit VALUES(?, ?)', (None, nick))
        uid = cur.lastrowid
    else:
        cur.execute('SELECT id FROM KilometriNikit WHERE name = ?', (nick,))
        uid = cur.fetchall()[0][0]

    return uid

def addKavely(nick, km, date):
    with cursor() as cur:
        uid = __maybeAddKmNick(nick, cur)
        cur.execute('INSERT INTO Kavelyt VALUES(?, ?, ?)', (uid, km, date))

def __getSport(cur, table, nick, earliest_date):
    query = ('SELECT km FROM %s event '
                'INNER JOIN KilometriNikit nick '
                'ON event.uid = nick.id AND nick.name = ? AND event.date >= ?' %
                table)
    params = (nick, earliest_date)

    cur.execute(query, params)
    return cur.fetchall()

def __getSportTopN(cur, table, earliest_date, limit):
    query = ('SELECT name, km from ('
                'SELECT nick.name AS name, SUM(event.km) AS km FROM %s AS event '
                'INNER JOIN KilometriNikit AS nick ON nick.id = event.uid AND event.date >= ? '
                'GROUP BY nick.id) '
             'ORDER BY km DESC LIMIT ?' %
             table)
    params = (earliest_date, limit)

    cur.execute(query, params)
    return cur.fetchall()

def getKavelyt(nick, earliest_date):
    with cursor() as cur:
        return __getSport(cur, "Kavelyt", nick, earliest_date)

def getTopKavelyt(earliest_date, limit):
    with cursor() as cur:
        return __getSportTopN(cur, "Kavelyt", earliest_date, limit)
