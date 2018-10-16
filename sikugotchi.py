import requests

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
            json = { 'siku': { 'name': 'Siku', 'creator': update.message.from_user.username } }
        )
        if r.status_code == 201:
            r.json()

    def delSikuHandler(self, bot, update, args):
        r = requests.post(
            'https://sikus.sivu.website/api/v1/siku/del',
            json = { 'killer': update.message.from_user.username }
        )
        if r.status_code == 200:
            r.json()
            bot.sendMessage(chat_id=update.message.chat_id, text='Rip')
        elif r.status_code == 404:
            bot.sendMessage(chat_id=update.message.chat_id, text='Sikut loppu')

    def sikuMapHandler(self, bot, update, args):
        bot.sendMessage(chat_id=update.message.chat_id, text='https://sikus.sivu.website')

    def feedSikuHandler(self, bot, update, args):
        bot.sendMessage(chat_id=update.message.chat_id, text='En tiedä vielä')
