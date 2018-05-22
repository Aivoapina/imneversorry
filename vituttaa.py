import requests
import urllib
import random

import db

class Vituttaa:
    def __init__(self):
        self.commands = { 'vituttaa': self.getVitutus, 'viisaus': self.getViisaus, 'hakemus': self.handleHakemus }
        self.vituttaaUrl = 'https://fi.wikipedia.org/wiki/Toiminnot:Satunnainen_sivu'
        self.viisaudet = db.readViisaudet()

    def getCommands(self):
        return self.commands

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

    def messageHandler(self, bot, update):
        msg = update.message
        if msg.text is not None:
            if 'vituttaa' in msg.text.lower():
                self.getVitutus(bot, update)
            elif 'viisaus' in msg.text.lower():
                self.getViisaus(bot, update)
            elif 'hakemus' in msg.text.lower():
                self.handleHakemus(bot, update)
