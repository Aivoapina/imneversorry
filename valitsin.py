import random
import re
import datetime
import json
import hashlib

class Valitsin:
    def __init__(self):
        self.commands = {}

    def getCommands(self):
        return self.commands

    def makeDecision(self, bot, update, options):
        now = datetime.datetime.now()
        data = [
            update.message.from_user.id,
            now.day,
            now.month,
            now.year,
            options.group(1),
            options.group(2)
        ]
        seed = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
        rigged = random.Random(seed)
        if random.randint(0, 49) == 0:
            answers = ['Molemmat :D', 'Ei kumpaakaan >:(']
            bot.sendMessage(chat_id=update.message.chat_id, text=random.sample(answers, 1)[0])
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text=rigged.sample([options.group(1), options.group(2)], 1)[0])

    def messageHandler(self, bot, update):
        msg = update.message
        if msg.text is not None:
            options = re.match(r"(^\S+) vai (\S+)$", msg.text.lower())
            if options:
                self.makeDecision(bot, update, options)
