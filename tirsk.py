from telegram import Update
from telegram.ext import CallbackContext
import random
from utils import banCheck

class Tirsk:
    isTirsk  = lambda self: random.random() < self.tirsk_prob
    rndTirsk = lambda self: random.choice(("tirsk", "Tirsk", "tirsk :D", "(tirsk)", "[tirsk]"))

    def __init__(self, tirsk_prob = 0.0001):
        self.tirsk_prob = tirsk_prob

    def getCommands(self):
        return dict()

    def sendTirsk(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        context.bot.sendMessage(chat_id=chat_id, text=self.rndTirsk())

    @banCheck
    def messageHandler(self, update: Update, context: CallbackContext):
        if self.isTirsk():
            self.sendTirsk(update, context)
