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
"""

fs = open('icd.txt', 'r')

for line in fs.read().splitlines():
    c.execute("INSERT INTO Diagnoosi(diagnoosi) values(?)", (line,))

fs.close()

conn.commit()
