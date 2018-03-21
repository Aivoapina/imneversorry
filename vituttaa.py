import requests
import urllib
import random

class Vituttaa:
    def __init__(self):
        self.commands = { 'vituttaa': self.getVitutus, 'viisaus': self.getViisaus }
        self.vituttaaUrl = 'https://fi.wikipedia.org/wiki/Toiminnot:Satunnainen_sivu'
        self.viisaudet = self.readViisaudet()

    def getCommands(self):
        return self.commands

    def readViisaudet(self):
        fs = open('viisaudet.txt', 'r')
        x = set()
        for line in fs.read().splitlines():
            x.add(line)
        return x

    def getViisaus(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text=random.sample(self.viisaudet, 1)[0])

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
