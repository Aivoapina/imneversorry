import sqlite3 as sq

def initdb(db='bot.db'):
    conn = sq.connect(db)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA encoding='UTF-8'")
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS Rip('
        'rip text primary key not null,'
        'type text,'
        'created date,'
        'channel integer,'
        'creator text)')

    c.execute('CREATE TABLE IF NOT EXISTS Ripinfo('
        'id integer primary key autoincrement,'
        'rip text references Rip(rip) not null,'
        'ripinfo text,'
        'creator text)')

    c.execute('CREATE TABLE IF NOT EXISTS Viisaus('
        'viisaus text primary key)')

    c.execute('CREATE TABLE IF NOT EXISTS Oppi('
        'keyword text primary key not null,'
        'definition text not null,'
        'created date,'
        'channel integer,'
        'creator text)')

    conn.commit()
    conn.close()
