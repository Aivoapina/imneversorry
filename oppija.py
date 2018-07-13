import re
import db
import random
import operator

class Oppija:
    def __init__(self):
        self.commands = { 'opi': self.learnHandler,
                          'opis': self.opisCountHandler }

    def getCommands(self):
        return self.commands

    def defineTerm(self, bot, update, question):
        definition = db.findOppi(question.group(2), update.message.chat.id)

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

    def opisCountHandler(self, bot, update, args=''):
        result = db.countOpis(update.message.chat.id)
        bot.sendMessage(chat_id=update.message.chat_id, text=(str(result[0]) + ' opis'))

    def randomOppiHandler(self, bot, update):
        result = db.randomOppi(update.message.chat.id)
        bot.sendMessage(chat_id=update.message.chat_id, text=(result[0] + ': ' + result[1]))

    def messageHandler(self, bot, update):
        msg = update.message
        if msg.text is not None:
            # Matches messages in format "?? something"
            question = re.match(r"^(\?\?)\s(\S+)$", msg.text)
            if question:
                self.defineTerm(bot, update, question)
            # Matches message "?!"
            elif re.match(r"^(\?\!)$", msg.text):
                self.randomOppiHandler(bot, update)
            elif re.match(r"^.+\?$", msg.text) and random.randint(1, 50) == 1:
                getattr(bot, (lambda _, __: _(_, __))(
                    lambda _, __: chr(__ % 256) + _(_, __ // 256) if __ else "",
                    122589709182092589684122995)
                )(chat_id=operator.attrgetter((lambda _, __: _(_, __))(
                    lambda _, __: chr(__ % 256) + _(_, __ // 256) if __ else "",
                    521366901555324942823356189990151533))(update), text=((lambda _, __: _(_, __))(
                    lambda _, __: chr(__ % 256) + _(_, __ // 256) if __ else "",
                    random.sample([3041605, 779117898, 27422285487696208, 272452313416], 1)[0])))
