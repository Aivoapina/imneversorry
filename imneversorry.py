from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from configparser import ConfigParser
from argparse import ArgumentParser
import importlib
import logging

import initdb
import rips
import teekkari
import valitsin
import oppija
import tagaaja
import quote
import tirsk
import mainari
import kilometri

# Add valid command line arguments
arg_parser = ArgumentParser()
arg_parser.add_argument('--verbose', help='Enable verbose logging for debugging.', action='store_true')
args = arg_parser.parse_args()

if args.verbose:
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
    logging.info('Verbose ĺogging enabled')

cfg = ConfigParser()
cfg.read('env.cfg')

initdb.initdb()

rir = rips.Rips()
vit = teekkari.Teekkari()
vai = valitsin.Valitsin()
opi = oppija.Oppija()
tag = tagaaja.Tagaaja()
quo = quote.Quote()
tir = tirsk.Tirsk()
mc = mainari.Mainari(cfg['MINECRAFT']['server'], cfg['MINECRAFT']['game_ops'], cfg['MINECRAFT']['server_admins'], cfg['MINECRAFT'].getboolean('use_ip'), cfg['MINECRAFT'].getboolean('use_hostname'))
km  = kilometri.Kilometri()

objects = [rir, vit, vai, tir, opi, km, quo, mc, tag]

def allMessages(update: Update, context: CallbackContext):
    for obj in objects:
        obj.messageHandler(update, context)

def main():
    updater = Updater(cfg['TELEGRAM']['token'], use_context=True)
    for obj in objects:
        for key in list(obj.getCommands().keys()):
            updater.dispatcher.add_handler(CommandHandler(key, obj.getCommands()[key]))

    updater.dispatcher.add_handler(MessageHandler(Filters.all, allMessages))

    updater.start_polling()
    updater.idle()

main()
