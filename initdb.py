import sqlite3 as sq

def initdb(db='bot.db'):
    conn = sq.connect(db)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA encoding='UTF-8'")
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS Rip('
        'rip text not null,'
        'type text,'
        'created date,'
        'channel integer not null,'
        'creator text,'
        'primary key (rip, channel) )')

    c.execute('CREATE TABLE IF NOT EXISTS Ripinfo('
        'id integer primary key autoincrement,'
        'rip text references Rip(rip) not null,'
        'ripinfo text,'
        'creator text)')

    c.execute('CREATE TABLE IF NOT EXISTS Viisaus('
        'viisaus text primary key)')

    c.execute('CREATE TABLE IF NOT EXISTS Sana('
        'sana text)')

    c.execute('CREATE TABLE IF NOT EXISTS Oppi('
        'keyword text not null,'
        'definition text not null,'
        'created date,'
        'channel integer not null,'
        'creator text,'
        'primary key (keyword, channel))')

    c.execute('CREATE TABLE IF NOT EXISTS Quote('
        'quote text not null,'
        'quotee text not null,'
        'created date,'
        'channel integer,'
        'creator text,'
        'primary key(quote, channel))')

    c.execute('CREATE TABLE IF NOT EXISTS Diagnoosi('
        'diagnoosi text)')

    c.execute('CREATE TABLE IF NOT EXISTS Maito('
        'maito text)')

    c.execute('CREATE TABLE IF NOT EXISTS Nimi('
        'nimi text)')

    c.execute('CREATE TABLE IF NOT EXISTS Kalat('
        'kala text)')

    c.execute('CREATE TABLE IF NOT EXISTS Vihannes('
        'nimi text)')

    c.execute('CREATE TABLE IF NOT EXISTS Kulkuneuvo('
        'nimi text)')

    c.execute('CREATE TABLE IF NOT EXISTS Planetoidi('
        'nimi text)')

    c.execute('CREATE TABLE IF NOT EXISTS Linnut('
        'nimi text)')

    c.execute('CREATE TABLE IF NOT EXISTS Arvonimet('
        'nimi text)')

    c.execute('CREATE TABLE IF NOT EXISTS Sotilasnimet('
        'nimi text)')

    c.execute('CREATE TABLE IF NOT EXISTS Ennustus('
        'rivi text)')

    conn.commit()
    conn.close()
