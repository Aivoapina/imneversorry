import requests
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

    def getCommands(self):
        return self.commands

    def addSikuHandler(self, bot, update, args):
        r = requests.post(
            'https://sikus.sivu.website/api/v1/siku/add',
            json={'siku': {'name': 'Siku', 'creator': update.message.from_user.username}},
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
