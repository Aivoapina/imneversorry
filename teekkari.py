import requests
import urllib
import random
import re
import db

class Teekkari:
    def __init__(self):
        self.commands = { 'vituttaa': self.getVitutus, 'viisaus': self.getViisaus, 'hakemus': self.handleHakemus, 'pekkauotila': self.getVittuilu, 'diagnoosi': self.getDiagnoosi }
        self.vituttaaUrl = 'https://fi.wikipedia.org/wiki/Toiminnot:Satunnainen_sivu'
        self.viisaudet = db.readViisaudet()
        self.sanat = db.readSanat()
        self.diagnoosit = db.readDiagnoosit()

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
        
    def getHalo(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text=random.choice(['Halo', 'Halo?', 'Halo?!']))
        
    def getNoppa(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text='Heitit ' + str(random.randint(1, 6)) + ' ja ' + str(random.randint(1, 6)) + '.')

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
            elif 'diagnoosi' in msg.text.lower():
                self.getDiagnoosi(bot, update)
            elif 'halo' in msg.text.lower():
                if re.match(r'^halo$', msg.text.lower()):
                    self.getHalo(bot, update)
            elif 'noppa' in msg.text.lower():
                if re.match(r'^noppa$', msg.text.lower()):
                    self.getNoppa(bot, update)
