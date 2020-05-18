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

def __addEvent(cur, table, uid, km, date):
    cur.execute('INSERT INTO %s VALUES(?, ?, ?)' % table, (uid, km, date))

def __getSport(cur, table, uid, earliest_date):
    query = ('SELECT SUM(km) FROM %s AS event '
                'WHERE event.uid = ? AND event.date >= ?' %
                table)
    params = (uid, earliest_date)

    cur.execute(query, params)
    return cur.fetchall()[0][0]

def __getSportTopN(cur, table, earliest_date, limit):
    query = ('SELECT uid, km from ('
                'SELECT event.uid AS uid, SUM(event.km) AS km FROM %s AS event '
                'WHERE event.date >= ? GROUP BY event.uid) '
             'ORDER BY km DESC LIMIT ?' %
             table)
    params = (earliest_date, limit)

    cur.execute(query, params)
    return cur.fetchall()

def getPisteet(mults_tables, earliest_date, limit):
    with cursor() as cur:
        subs = ("SELECT uid, km * %.1f AS score, date FROM %s" % m_t for m_t in mults_tables)
        table_unions = " UNION ALL ".join(subs)
        user_scores  = "SELECT uid, SUM(score) AS score FROM (%s) WHERE date > ? GROUP BY uid" % table_unions
        query        = "SELECT uid, score FROM (%s) ORDER BY score DESC LIMIT ?" % user_scores

        params = (earliest_date, limit)
        cur.execute(query, params)
        return cur.fetchall()

def addUrheilu(uid, km, date, table):
    with cursor() as cur:
        __addEvent(cur, table, uid, km, date)

def getKavelyt(uid, earliest_date):
    with cursor() as cur:
        return __getSport(cur, "Kavelyt", uid, earliest_date)

def getJuoksut(uid, earliest_date):
    with cursor() as cur:
        return __getSport(cur, "Juoksut", uid, earliest_date)

def getPyorailyt(uid, earliest_date):
    with cursor() as cur:
        return __getSport(cur, "Pyorailyt", uid, earliest_date)

def getTopKavelyt(earliest_date, limit):
    with cursor() as cur:
        return __getSportTopN(cur, "Kavelyt", earliest_date, limit)

def getTopJuoksut(earliest_date, limit):
    with cursor() as cur:
        return __getSportTopN(cur, "Juoksut", earliest_date, limit)

def getTopPyorailyt(earliest_date, limit):
    with cursor() as cur:
        return __getSportTopN(cur, "Pyorailyt", earliest_date, limit)
