from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, InlineQueryHandler
from configparser import ConfigParser
from argparse import ArgumentParser
import importlib
import logging
import ast
import initdb
import rips
import teekkari
import valitsin
import oppija
import tagaaja
import quote
import quotedle
import tirsk
import mainari
import kilometri
import tarot
import kattely
import kissa
import noppa
import joulukalenteri

# Add valid command line arguments
arg_parser = ArgumentParser()
arg_parser.add_argument(
    '--verbose', help='Enable verbose logging for debugging.', action='store_true')
args = arg_parser.parse_args()

if args.verbose:
    logging.basicConfig(format="%(levelname)s: %(message)s",
                        level=logging.DEBUG)
    logging.info('Verbose ĺogging enabled')

cfg = ConfigParser()
cfg.read('env.cfg')

BANNED_CHANNELS = ast.literal_eval(cfg['TELEGRAM']['banned_channels'])

initdb.initdb()

rir = rips.Rips()
vit = teekkari.Teekkari(cfg['MISC'].getboolean('use_local_vitun'))
vai = valitsin.Valitsin()
opi = oppija.Oppija()
tag = tagaaja.Tagaaja()
quo = quote.Quote()
que = quotedle.Quotedle()
tir = tirsk.Tirsk()
kis = kissa.Kissa()
mc = mainari.Mainari(cfg['MINECRAFT']['server'], cfg['MINECRAFT']['game_ops'], cfg['MINECRAFT']
                     ['server_admins'], cfg['MINECRAFT'].getboolean('use_ip'), cfg['MINECRAFT'].getboolean('use_hostname'))
km = kilometri.Kilometri()
tar = tarot.Tarot()
kat = kattely.Kattelija()
nop = noppa.Noppa()
jou = joulukalenteri.Joulukalenteri()

objects = [rir, vit, vai, tir, opi, km, quo, que, mc, tag, tar, kis, kat, nop, jou]


def allMessages(update: Update, context: CallbackContext):
    for obj in objects:
        obj.messageHandler(update, context)


def main():
    updater = Updater(cfg['TELEGRAM']['token'], use_context=True)
    for obj in objects:
        for key in list(obj.getCommands().keys()):
            updater.dispatcher.add_handler(
                CommandHandler(key, obj.getCommands()[key], ~Filters.chat(BANNED_CHANNELS)))

    updater.dispatcher.add_handler(MessageHandler(
        ~Filters.chat(BANNED_CHANNELS), allMessages))

    updater.dispatcher.add_handler(InlineQueryHandler(opi.inlineQueryHandler))

    updater.start_polling()
    updater.idle()


main()
