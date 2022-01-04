import sqlite3 as sq
import datetime as dt

from contextlib import contextmanager
from rapidfuzz import fuzz
from rapidfuzz import process

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

def searchOppi(keyword, user, channels):
    search = '%' + keyword + '%'
    results = []
    for channel in channels:
        with cursor() as cur:
            cur.execute('SELECT keyword, definition FROM Oppi WHERE (keyword LIKE ? OR definition LIKE ?) AND channel=? LIMIT 50', (search, search, channel))
            results = results + [(item[0], item[1]) for item in cur.fetchall()]
    opis = {}
    keys = []
    for item in results:
        opis[item[0]] = item[1]
        keys.append(item[0])
    keys = list(set(keys))
    fuzzed = process.extract(keyword, keys, limit=50)
    output = []
    for item in fuzzed:
        output.append((item[0], opis[item[0]]))
    return output

def getChannels():
    with cursor() as cur:
        cur.execute('SELECT DISTINCT channel FROM Oppi')
        return [item[0] for item in cur.fetchall()]

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

def readDiagnoositFxx():
    with cursor() as cur:
        cur.execute('SELECT diagnoosi_fxx from DiagnoosiFxx')
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

def readKasvinimet():
    with cursor() as cur:
        cur.execute('SELECT nimi from Kasvinimet')
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

def addUrheilu(uid, chatid, km, lajinnimi, date):
    with cursor() as cur:
        query = ("INSERT INTO Urheilut (uid, chatid, km, type, date) VALUES (?, ?, ?, "
                    "(SELECT l.id FROM Urheilulajit AS l WHERE l.nimi = ?), ?)")
        params = (uid, chatid, km, lajinnimi, date)

        cur.execute(query, params)

def getKayttajanUrheilut(uid, chatid, earliest_date):
    with cursor() as cur:
        query = ("SELECT up.lajinnimi AS lajinnimi, SUM(up.km) AS km, SUM(up.pisteet) AS pisteet "
                     "FROM UrheilutPisteilla AS up "
                     "WHERE up.uid = ? AND up.chatid = ? AND up.date >= ? "
                     "GROUP BY up.lajinnimi, up.uid")
        params = (uid, chatid, earliest_date)

        cur.execute(query, params)
        return cur.fetchall()

def getTopUrheilut(chatid, lajinnimi, earliest_date, limit):
    with cursor() as cur:
        query = ("SELECT uid, km from (SELECT up.uid AS uid, SUM(up.km) AS km "
                     "FROM UrheilutPisteilla AS up "
                     "WHERE up.chatid = ? AND up.date >= ? AND up.lajinnimi = ? "
                     "GROUP BY up.lajinnimi, up.uid) "
                     "ORDER BY km DESC LIMIT ?")
        params = (chatid, earliest_date, lajinnimi, limit)

        cur.execute(query, params)
        return cur.fetchall()

def getPisteet(chatid, earliest_date, limit):
    with cursor() as cur:
        query = ("SELECT uid, pisteet from (SELECT up.uid AS uid, SUM(up.pisteet) AS pisteet "
                     "FROM UrheilutPisteilla AS up "
                     "WHERE up.chatid = ? AND up.date >= ? "
                     "GROUP BY up.uid) "
                     "ORDER BY pisteet DESC LIMIT ?")
        params = (chatid, earliest_date, limit)

        cur.execute(query, params)
        return cur.fetchall()

def lisaaUrheilulaji(nimi, kerroin):
    with cursor() as cur:
        cur.execute("INSERT INTO Urheilulajit (nimi, kerroin) VALUES (?, ?) ON CONFLICT (nimi) DO UPDATE SET kerroin = ?",
            (nimi, kerroin, kerroin))

def readSelitykset():
    with cursor() as cur:
        cur.execute('SELECT kortti, selitys, rev from Korttiselitykset')
        rows = cur.fetchall()
        return (rows)
