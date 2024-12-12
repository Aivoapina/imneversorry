from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

import datetime
import db
import random

class Joulukalenteri:

    def __init__(self):
        self.commands = {
            'luukku': self.luukkuHandler,
        }
        self.luukut = db.readJoulukalenteri()
        self.emojit = ('❄️', '☃️', '☕', '🍫', '️🛷', '🎇', '🎄', '✨', '🎅')
        self.jesterit = ('🎪', '🤪', '🤡', '👁👄👁', '🃏')
        self.rigged = random.Random()


    def getCommands(self):
        return self.commands

    async def luukkuHandler(self, update: Update, context: CallbackContext):
        now = datetime.datetime.now()
        current_day = now.day
        current_month = now.month
        if len(context.args) < 1:
            day = current_day
        else:
            try:
                day = int(context.args[0])
            except:
                day = current_day
        
        # Send the 25th luukku (just a normal luukku) if kurkkija is unlucky
        # Or just because.
        luukku_is_legal = day >= 1 and day <= min(24, current_day) and current_month == 12
        jestered = random.randint(0, 23 if luukku_is_legal else 4) == 0
        
        chat_id = update.message.chat_id
        if jestered or luukku_is_legal:
            index = 24 if jestered else day - 1
            img_link = self.luukut[index][0]
            emoji = self.rigged.choice(self.jesterit if jestered else self.emojit)
            message = f'<b>Päivän {day} luukku {emoji}\n</b>'
            await context.bot.sendPhoto(chat_id=chat_id, photo = img_link, caption=message, parse_mode=ParseMode.HTML, has_spoiler=True)
        else:
            await context.bot.sendMessage(chat_id=chat_id, text='Eipäs kurkita luukkuja >:(')

