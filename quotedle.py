import enum
from telegram import Update
from telegram.ext import CallbackContext
import random

import db


GREEN = '🟩'
YELLO = '🟨'
BLACK = '⬛️'


def makeGuessString(guess, correct):
    n_chars_guess = len(guess)
    n_chars_correct = len(correct)
    string = [BLACK for _ in guess]

    n_chars_in_correct = {c: correct.count(c) for c in set(correct)}
    green_indices = [i for i, c in enumerate(guess) if i < n_chars_correct and c == correct[i]]
    green_chars = [guess[i] for i in green_indices]
    for c in green_chars:
        n_chars_in_correct[c] -= 1

    for i, c in enumerate(guess):
        if i in green_indices: 
            string[i] = GREEN
        elif c in correct and n_chars_in_correct[c] > 0:
            n_chars_in_correct[c] -= 1
            string[i] = YELLO
    
    return ''.join(string)


class Quotedle:

    def __init__(self):
        self.commands = {
            'quotedle': self.quotedleHandler,
            'qarvaa': self.guessHandler
        }

        self.correctQuote = {}
        self.guesses = {}
        self.maxQuoteeChars = 50
        self.defaultQuote = ['tapan kaikki', 'imneversorry']
        self.maxGuess = 6

    def getCommands(self):
        return self.commands
    
    def resetGame(self, chat_id):
        quotes = db.findQuotes(chat_id)
        if len(quotes) > 0:
            quote = list(random.sample(quotes, 1)[0])
        else:
            quote = self.defaultQuote
        if len(quote[1]) > self.maxQuoteeChars:
            quote = self.defaultQuote
        quote[1] = quote[1].lower()

        self.correctQuote[chat_id] = quote
        self.guesses[chat_id] = []

    def quotedleHandler(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        if chat_id not in self.correctQuote or chat_id not in self.guesses:
            self.resetGame(chat_id)

        message = 'Arvaa kenen quote: \"{}\"?'.format(self.correctQuote[chat_id][0])
        context.bot.sendMessage(chat_id=chat_id, text=message)

    def guessHandler(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        if len(context.args) < 1:
            return
        if len(context.args[0]) > self.maxQuoteeChars:
            context.bot.send_message(chat_id=chat_id, text=':D')
            return

        if chat_id not in self.correctQuote or chat_id not in self.guesses:
            context.bot.sendMessage(chat_id=chat_id, text='Peli ei käynnissä, aloitetaan uusi peli!')
            self.quotedleHandler(update, context)
            return

        guess_string = makeGuessString(context.args[0].lower(), self.correctQuote[chat_id][1])
        self.guesses[chat_id].append(guess_string)

        if context.args[0].lower() == self.correctQuote[chat_id][1]:
            self.endGame(context, chat_id, True)
            self.resetGame(chat_id)
        elif len(self.guesses[chat_id]) >= self.maxGuess:
            self.endGame(context, chat_id, False)
            self.resetGame(chat_id)
        else:
            context.bot.send_message(chat_id=chat_id, text=guess_string)
        
    def endGame(self, context, chat_id, victory):
        if victory:
            context.bot.sendMessage(chat_id=chat_id, text='Onnea, löysit quoten lausujan :3')
        else:
            context.bot.sendMessage(chat_id=chat_id, text='Pahus, et löytänyt quoten lausujaa :(')
        guessStack = '\n'.join(self.guesses[chat_id])
        message = '/quotedle - {:s}, {:d}/{:d}\n{:s}'.format(self.correctQuote[chat_id][1], len(self.guesses[chat_id]), self.maxGuess, guessStack)
        context.bot.sendMessage(chat_id=chat_id, text=message)
        
    def messageHandler(self, update: Update, context: CallbackContext):
        return
        
