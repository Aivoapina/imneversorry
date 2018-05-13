import re
import db

class Oppija:
    def __init__(self):
        self.commands = { 'opi': self.learnHandler }

    def getCommands(self):
        return self.commands

    def defineTerm(self, bot, update, question):
        definition = db.findOppi(question.group(2))

        if definition is not None:
            bot.sendMessage(chat_id=update.message.chat_id, text=(question.group(2) + ': ' + definition[0]))
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text='En tiedä')

    def learnHandler(self, bot, update, args):
        if len(args) < 2:
            bot.sendMessage(chat_id=update.message.chat_id, text='Usage: /opi <asia> <määritelmä>')
            return
        keyword, definition = args[0], ' '.join(args[1:])
        self.learn(bot, update, keyword, definition)

    def learn(self, bot, update, keyword, definition):
        chat_id = update.message.chat.id
        db.upsertOppi(keyword, definition, chat_id, update.message.from_user.username)

    def messageHandler(self, bot, update):
        msg = update.message
        if msg.text is not None:
            # Matches messages in format "?? something"
            question = re.match(r"^(\?\?)\s(\S+)$", msg.text.lower()) 
            if question:
                self.defineTerm(bot, update, question)
