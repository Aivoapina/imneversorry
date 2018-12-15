import requests
import urllib
import random
import re
import db

class Teekkari:
    def __init__(self):
        self.commands = { 'vituttaa': self.getVitutus, 'viisaus': self.getViisaus, 'hakemus': self.handleHakemus, 'pekkauotila': self.getVittuilu, 'diagnoosi': self.getDiagnoosi, 'maitonimi': self.getMaitonimi, 'helveten' : self.getHelveten, 'pizza': self.getPizza, 'kalanimi': self.getKalanimi }
        self.vituttaaUrl = 'https://fi.wikipedia.org/wiki/Toiminnot:Satunnainen_sivu'
        self.urbaaniUrl = 'https://urbaanisanakirja.com/random/'
        self.slangopediaUrl = 'http://www.slangopedia.se/slumpa/'
        self.viisaudet = db.readViisaudet()
        self.sanat = db.readSanat()
        self.diagnoosit = db.readDiagnoosit()
        self.maidot = db.readMaidot()
        self.nimet = db.readNimet()
        self.kalat = db.readKalat()
        self.vihanneet = db.readVihanneet()
        self.planetoidit = db.readPlanetoidit()
        self.kulkuneuvot = db.readKulkuneuvot()

    def getCommands(self):
        return self.commands

    def getVittuilu(self, bot, update, args=''):
        if random.randint(0, 4) == 0:
            bot.sendMessage(chat_id=update.message.chat_id, text='TÖRKEÄÄ SOLVAAMISTA')
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text='vittuilu'+random.sample(self.sanat, 1)[0][0])

    def handleHakemus(self, bot, update, args=''):
        if random.randint(0, 9) == 0:
            bot.sendMessage(chat_id=update.message.chat_id, text='hyy-vä')
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text='tapan sut')

    def getViisaus(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text=random.sample(self.viisaudet, 1)[0][0])

    def getVitutus(self, bot, update, args=''):
        r = requests.get(self.vituttaaUrl)
        url = urllib.parse.unquote_plus(r.url).split('/')
        vitutus = url[len(url)-1].replace('_', ' ') + " vituttaa"
        bot.sendMessage(chat_id=update.message.chat_id, text=vitutus)

    def getDiagnoosi(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text=random.sample(self.diagnoosit, 1)[0][0])

    def getMaitonimi(self, bot, update, args=''):
        maitoNimi = random.sample(self.maidot, 1)[0][0] + "-" + random.sample(self.nimet, 1)[0][0]
        bot.sendMessage(chat_id=update.message.chat_id, text=maitoNimi)

    def getKalanimi(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text=random.sample(self.kalat, 1)[0][0])

    def getMoponimi(self, bot, update, args=''):
        kurkku = random.sample(self.vihanneet, 1)[0][0]
        mopo = random.sample(self.kulkuneuvot, 1)[0][0]
        kuu = random.sample(self.planetoidit, 1)[0][0]
        mopoNimi = kurkku + ("", "-")[kurkku[-1:] == mopo[0] and mopo[0] in ('a', 'e', 'i', 'o', 'u', 'y', 'ä', 'ö')] + mopo + " eli " + kuu + ("", "-")[kuu[-1:] == 'e'] + 'eläin ' + kurkku + 'maasta'
        bot.sendMessage(chat_id=update.message.chat_id, text=mopoNimi)

    def getHalo(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text=random.choice(['Halo', 'Halo?', 'Halo?!']))

    def getPizza(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text='Ananas kuuluu pizzaan!')

    def getNoppa(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text='Heitit ' + str(random.randint(1, 6)) + ' ja ' + str(random.randint(1, 6)) + '.')

    def getUrbaani(self):
        webpage = urllib.request.urlopen(self.urbaaniUrl).read().decode("utf-8")
        title = str(webpage).split('<title>')[1].split('</title>')[0]
        sana = title.split(" |")[0]
        return sana

    def getSlango(self):
        r = requests.get(self.slangopediaUrl)
        url = urllib.parse.unquote_plus(r.url, encoding='ISO-8859-1').split('/')
        return str(url[-1].split('=')[-1].lower())

    def getVitun(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text=self.getUrbaani().capitalize() + " vitun " + self.getUrbaani())

    def getVaalikone(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text='Äänestä: ' + str(random.randint(1,424) + 1))

    def getHelveten(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id,
            text=self.getSlango().capitalize() + ' jävla ' + self.getSlango().lower() )

    def messageHandler(self, bot, update):
        msg = update.message
        if msg.text is not None:
            if 'vituttaa' in msg.text.lower():
                self.getVitutus(bot, update)
            elif 'viisaus' in msg.text.lower():
                self.getViisaus(bot, update)
            elif 'pekkauotila' in msg.text.lower():
                self.getVittuilu(bot, update)
            elif 'hakemus' in msg.text.lower():
                self.handleHakemus(bot, update)
            elif 'diagno' in msg.text.lower():
                self.getDiagnoosi(bot, update)
            elif re.match(r'^halo', msg.text.lower()):
                self.getHalo(bot, update)
            elif re.match(r'^noppa', msg.text.lower()):
                self.getNoppa(bot, update)
            elif re.match(r'^vitun', msg.text.lower()):
                self.getVitun(bot, update)
            elif re.match(r'^helveten', msg.text.lower()):
                self.getHelveten(bot, update)
            elif re.match(r'^/maitonimi', msg.text.lower()):
                self.getMaitonimi(bot, update)
            elif re.match(r'^/kurkkumoponimi', msg.text.lower()):
                self.getMoponimi(bot, update)
