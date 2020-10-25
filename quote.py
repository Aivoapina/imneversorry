import random

import db

class Quote:
    def __init__(self):
        self.commands = { 'addq': self.addQuote,
                        'quote': self.getQuote,
                        'quotes': self.quotesCountHandler }

    def getCommands(self):
        return self.commands

    def addQuote(self, bot, update, args):
        if len(args) < 2:
            bot.sendMessage(chat_id=update.message.chat.id, text='Usage: /addq <quotee> <quote>')
        else:
            quotee = args[0].strip('@')
            quote = ' '.join(args[1:])
            if quote[0] == '"' and quote[len(quote) - 1] == '"':
                quote = quote[1:len(quote) - 1]
            db.insertQuote(quote, quotee, update.message.chat.id, update.message.from_user.username)

    def quotesCountHandler(self, bot, update, args):
        if len(args) == 0:
            count = db.countQuotes(update.message.chat.id)
        else:
            quotee = args[0].strip('@')
            quotes = db.findQuotes(update.message.chat.id, quotee)
            count = len(quotes)

        bot.sendMessage(chat_id=update.message.chat.id, text=str(count) + ' quotes')

    def getQuote(self, bot, update, args):
        if len(args) == 0:
            quotes = db.findQuotes(update.message.chat.id)
        else:
            quotee = args[0].strip('@')
            quotes = db.findQuotes(update.message.chat.id, quotee)
        quote = random.sample(quotes, 1)[0]

        formated_quote = '"{}" - {}'.format(*quote)
        bot.sendMessage(chat_id=update.message.chat.id, text=formated_quote)
