import sqlite3 as sq
import initdb

initdb.initdb()

conn = sq.connect('bot.db')
c = conn.cursor()

fs = open('resources/icd.txt', 'r', encoding='utf-8')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Diagnoosi(diagnoosi) values(?)", (line,))

fs.close()

fs = open('resources/icd_fxx.txt', 'r', encoding='utf-8')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO DiagnoosiFxx(diagnoosi_fxx) values(?)", (line,))

fs.close()

fs = open('resources/viisaudet.txt', 'r', encoding='utf-8')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Viisaus(viisaus) values(?)", (line,))

fs.close()

fs = open('resources/kaloja.txt', 'r', encoding='utf-8')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Kalat(kala) values(?)", (line,))

fs.close()

fs = open('resources/maidot.txt', 'r', encoding='utf-8')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Maito(maito) values(?)", (line,))

fs.close()

fs = open('resources/nimet.txt', 'r', encoding='utf-8')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Nimi(nimi) values(?)", (line,))

fs.close()

fs = open('resources/vihanneet.txt', 'r', encoding='utf-8')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Vihannes(nimi) values(?)", (line,))

fs.close()

fs = open('resources/kulkuneuvot.txt', 'r', encoding='utf-8')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Kulkuneuvo(nimi) values(?)", (line,))

fs.close()

fs = open('resources/planetoidit.txt', 'r', encoding='utf-8')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Planetoidi(nimi) values(?)", (line,))

fs.close()

fs = open('resources/lintuslangi.txt', 'r', encoding='utf-8')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Linnut(nimi) values(?)", (line,))

fs.close()

fs = open('resources/sotilasarvot.txt', 'r', encoding='utf-8')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Arvonimet(nimi) values(?)", (line,))

fs.close()

fs = open('resources/sotilasnimet.txt', 'r', encoding='utf-8')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Sotilasnimet(nimi) values(?)", (line,))

fs.close()

fs = open('resources/kasvinimet.txt', 'r', encoding='utf-8')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Kasvinimet(nimi) values(?)", (line,))

fs.close()

fs = open('resources/ennustus.txt', 'r', encoding='utf-8')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Ennustus(rivi) values(?)", (line,))

fs.close()

fs = open('resources/nakutukset.txt', 'r', encoding='utf-8')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Nakutukset(nakutus) values(?)", (line,))
fs.close()

fs = open('resources/selitykset.txt', 'r', encoding='utf-8')

for line in fs.read().splitlines():
    c.execute("INSERT OR IGNORE INTO Korttiselitykset(kortti, selitys, rev) values(?,?,?)", (line.split("@@@")[0], line.split("@@@")[1], line.split("@@@")[2]))
fs.close()

conn.commit()
