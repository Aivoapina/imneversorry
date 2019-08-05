from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from configparser import ConfigParser
from argparse import ArgumentParser
import importlib
import logging
import random

import initdb
import rips
import teekkari
import valitsin
import oppija
import quote
import mainari

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
quo = quote.Quote()
mc = mainari.Mainari(cfg['MINECRAFT']['server'], cfg['MINECRAFT']['game_ops'], cfg['MINECRAFT']['server_admins'], cfg['MINECRAFT']['use_ip'])

objects = [rir, vit, vai, opi, quo, mc]

def allMessages(bot, update, job_queue):
    job = job_queue.run_repeating(pongTime, 1, context=update)
    for obj in objects:
        obj.messageHandler(bot, update)

def pongTime(bot, job):
    if random.randint(0, 86400) == 0:
        job.context.message.reply_text("BEERPONG TIME!")

def main():
    updater = Updater(cfg['TELEGRAM']['token'])
    for obj in objects:
        for key in list(obj.getCommands().keys()):
            updater.dispatcher.add_handler(CommandHandler(key, obj.getCommands()[key], pass_args=True))

    updater.dispatcher.add_handler(MessageHandler(Filters.all, allMessages, pass_job_queue=True))

    updater.start_polling()
    updater.idle()

main()
