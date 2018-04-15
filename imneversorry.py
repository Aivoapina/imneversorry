from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from configparser import ConfigParser
import importlib

import rips
import vituttaa
import valitsin

cfg = ConfigParser()
cfg.read('env.cfg')

rir = rips.Rips()
vit = vituttaa.Vituttaa()
vai = valitsin.Valitsin()

objects = [rir, vit, vai]

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
