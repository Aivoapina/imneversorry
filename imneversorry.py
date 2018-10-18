from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from configparser import ConfigParser
import importlib

import initdb
import rips
import teekkari
import valitsin
import oppija
import quote
import sikugotchi

cfg = ConfigParser()
cfg.read('env.cfg')

initdb.initdb()

rir = rips.Rips()
vit = teekkari.Teekkari()
vai = valitsin.Valitsin()
opi = oppija.Oppija()
quo = quote.Quote()
sik = sikugotchi.Sikugotchi()

objects = [rir, vit, vai, opi, quo, sik]

def allMessages(bot, update):
    for obj in objects:
        obj.messageHandler(bot, update)

def main():
    updater = Updater(cfg['TELEGRAM']['token'])
    for obj in objects:
        for key in list(obj.getCommands().keys()):
            updater.dispatcher.add_handler(CommandHandler(key, obj.getCommands()[key], pass_args=True))

    updater.dispatcher.add_handler(MessageHandler(Filters.all, allMessages))

    updater.start_polling()
    updater.idle()

main()
