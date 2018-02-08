from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from configparser import ConfigParser
import importlib

import rips

cfg = ConfigParser()
cfg.read('env.cfg')

rir = rips.Rips()

updater = Updater(cfg['TELEGRAM']['token'])
for key in list(rir.getCommands().keys()):
    updater.dispatcher.add_handler(CommandHandler(key, rir.getCommands()[key], pass_args=True))

updater.dispatcher.add_handler(MessageHandler(Filters.all, rir.messageHandler))

updater.start_polling()
updater.idle()
