import random

import db

class Quote:
    def __init__(self):
        self.commands = { 'addquote': self.addQuote,
                        'quote': self.getQuote }

    def getCommands(self):
        return self.commands

    def addQuote(self, bot, update, args):
        if len(args) < 2:   
            bot.sendMessage(chat_id=update.message.chat.id, text='Usage: /addquote <quotee> <quote>')
        else:
            quotee = args[0]
            quote = ' '.join(args[1:])
            if quote[0] == '"' and quote[len(quote) - 1] == '"':
                quote = quote[1:len(quote) - 1]
            quotee.replace('@', '')
            db.insertQuote(quote, quotee, update.message.chat.id, update.message.from_user.username)
            
        
    def getQuote(self, bot, update, args):
        if len(args) == 0:
            quotes = db.findQuotes(update.message.chat.id)
        else:
            quotee = args[0]
            if quotee[0] == '@':
                quotee = quotee[1:]
            quotes = db.findQuotes(update.message.chat.id, quotee)
            print(quotes)
        quote = random.sample(quotes, 1)[0]
        
        formatedQuote = '"{}" - {}'.format(*quote)
        bot.sendMessage(chat_id=update.message.chat.id, text=formatedQuote)
