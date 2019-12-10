import sqlite3 as sq
import initdb

initdb.initdb()

conn = sq.connect('bot.db')
c = conn.cursor()

fs = open('resources/icd.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Diagnoosi(diagnoosi) values(?)", (line,))

fs.close()

fs = open('resources/viisaudet.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Viisaus(viisaus) values(?)", (line,))

fs.close()

fs = open('resources/kaloja.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Kalat(kala) values(?)", (line,))

fs.close()

fs = open('resources/maidot.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Maito(maito) values(?)", (line,))

fs.close()

fs = open('resources/nimet.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Nimi(nimi) values(?)", (line,))

fs.close()

fs = open('resources/vihanneet.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Vihannes(nimi) values(?)", (line,))

fs.close()

fs = open('resources/kulkuneuvot.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Kulkuneuvo(nimi) values(?)", (line,))

fs.close()

fs = open('resources/planetoidit.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Planetoidi(nimi) values(?)", (line,))

fs.close()

fs = open('resources/lintuslangi.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Linnut(nimi) values(?)", (line,))

fs.close()

fs = open('resources/sotilasarvot.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Arvonimet(nimi) values(?)", (line,))

fs.close()

fs = open('resources/sotilasnimet.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Sotilasnimet(nimi) values(?)", (line,))

fs.close()

fs = open('resources/ennustus.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Ennustus(rivi) values(?)", (line,))

fs.close()

fs = open('resources/nakutukset.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Nakutukset(nakutus) values(?)", (line,))

fs.close()

conn.commit()
