import requests
import db
import random

from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('env.cfg')

headers = {'Authorization': cfg['TELEGRAM']['sikugotchi_token']}

class Sikugotchi:
    def __init__(self):
        self.commands = { 'addsiku': self.addSikuHandler,
                          'delsiku': self.delSikuHandler,
                          'feedsiku': self.feedSikuHandler,
                          'sikumap': self.sikuMapHandler }
        self.vihanneet = db.readVihanneet()
        self.planetoidit = db.readPlanetoidit()
        self.kulkuneuvot = db.readKulkuneuvot()

    def getCommands(self):
        return self.commands

    def addSikuHandler(self, bot, update, args):
        kurkku = random.sample(self.vihanneet, 1)[0][0]
        mopo = random.sample(self.kulkuneuvot, 1)[0][0]
        kuu = random.sample(self.planetoidit, 1)[0][0]
        sikuNimi = kurkku + ("", "-")[kurkku[-1:] == mopo[0] and mopo[0] in ('a', 'e', 'i', 'o', 'u', 'y', 'ä', 'ö')] + mopo + " eli " + kuu + ("", "-")[kuu[-1:] == 'e'] + 'eläin ' + kurkku + 'maasta'

        r = requests.post(
            'https://sikus.sivu.website/api/v1/siku/add',
            json={'siku': {'name': sikuNimi, 'creator': update.message.from_user.username}},
            headers=headers
        )
        if r.status_code == 201:
            bot.sendMessage(chat_id=update.message.chat_id, text='Lisätty ' + r.json()['name'])

    def delSikuHandler(self, bot, update, args):
        r = requests.post(
            'https://sikus.sivu.website/api/v1/siku/del',
            json = { 'killer': update.message.from_user.username },
            headers=headers
        )
        if r.status_code == 200:
            bot.sendMessage(chat_id=update.message.chat_id, text='Rip ' + r.json()['name'])
        elif r.status_code == 404:
            bot.sendMessage(chat_id=update.message.chat_id, text='Sikut loppu :(')

    def sikuMapHandler(self, bot, update, args):
        bot.sendMessage(chat_id=update.message.chat_id, text='https://sikus.sivu.website')

    def feedSikuHandler(self, bot, update, args):
        r = requests.post(
            'https://sikus.sivu.website/api/v1/siku/feed',
            headers=headers
        )
        if r.status_code == 200:
            r.json()
            bot.sendMessage(chat_id=update.message.chat_id, text='Ruokittu ' + r.json()['name'])
        elif r.status_code == 404:
            bot.sendMessage(chat_id=update.message.chat_id, text='Ei sikuja mitä ruokkia :(')
