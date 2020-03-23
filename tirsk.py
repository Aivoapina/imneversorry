import random

class Tirsk:
    isTirsk  = lambda self: random.random() < self.tirsk_prob
    rndTirsk = lambda self: random.choice(("tirsk", "Tirsk", "tirsk :D", "(tirsk)", "[tirsk]"))

    def __init__(self, tirsk_prob = 0.0001):
        self.tirsk_prob = tirsk_prob

    def getCommands(self):
        return dict()

    def sendTirsk(self, bot, update):
        chat_id = update.message.chat.id
        bot.sendMessage(chat_id=chat_id, text=self.rndTirsk())

    def messageHandler(self, bot, update):
        if self.isTirsk():
            self.sendTirsk(bot, update)
