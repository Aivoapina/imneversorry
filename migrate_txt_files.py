import sqlite3 as sq
import initdb

initdb.initdb()

conn = sq.connect('bot.db')
c = conn.cursor()

"""
fs = open('viisaudet.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT INTO Viisaus(viisaus) values(?)", (line,))

fs.close()

fs = open('rips.txt', 'r')

for line in fs.read().splitlines():
    sline = line.split(';')
    c.execute("INSERT INTO Rip(type, rip) values(?, ?)", (sline[0], ';'.join(sline[1:])))

fs.close()

fs = open('kaloja.txt', 'r')

for line in fs.read().splitlines():
    #strline = str(line)
    c.execute("INSERT INTO Kalat(kala) values(?)", (line,))

fs = open('maidot.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT INTO Maito(maito) values(?)", (line,))

fs = open('nimet.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT INTO Nimi(nimi) values(?)", (line,))

fs = open('vihanneet.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT INTO Vihannes(nimi) values(?)", (line,))

fs = open('kulkuneuvot.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT INTO Kulkuneuvo(nimi) values(?)", (line,))

fs = open('planetoidit.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT INTO Planetoidi(nimi) values(?)", (line,))
"""
fs = open('lintuslangi.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT INTO Linnut(nimi) values(?)", (line,))

fs.close()

conn.commit()
