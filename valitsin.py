import random
import re

class Valitsin:
    def __init__(self):
        self.commands = { 'x vai y': self.makeDecision }

    def getCommands(self):
        return self.commands

    def makeDecision(self, bot, update, options):
        bot.sendMessage(chat_id=update.message.chat_id, text=random.sample([options.group(1), options.group(2)], 1)[0])

    def messageHandler(self, bot, update):
        msg = update.message
        if msg.text is not None:
            options = re.match(r"(^\S+) vai (\S+)$", msg.text.lower()) 
            if options:
                self.makeDecision(bot, update, options)
