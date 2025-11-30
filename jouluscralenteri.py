from telegram import Update 
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

import datetime
import db
import random
import re

SANTA_SEED = 0xDEADBEEF

RE_SCRANLINE = r'.*[Ss]cran [👍👎].*'

def getScran(id):
    t = db.getScran(id)
    return {
        'text': t[0],
        'upvotes': t[1],
        'downvotes': t[2],
        'img_path': t[3]
    }

class Jouluscralenteri:

    def __init__(self):
        self.commands = {
            'luukku': self.luukkuHandler,
        }
        self.rigged = random.Random(SANTA_SEED)
        n_scrans = db.countScrans()
        scran_ids = range(1, n_scrans) # AUTOINCREMENT in SQLite starts at id 1
        luukku_ids_left = self.rigged.sample(scran_ids, k=24)
        luukku_ids_right = self.rigged.sample(scran_ids, k=24)
        self.luukut = [
            [getScran(left), getScran(right)]
            for (left, right) in zip(luukku_ids_left, luukku_ids_right)
        ]
        self.emojit = ('❄️', '☃️', '☕', '🍫', '️🛷', '🎇', '🎄', '✨', '🎅')


    def getCommands(self):
        return self.commands
    
    async def sendScran(self, context, chat_id, scran, extra_text=''):
        img_link = scran['img_path']
        parts = scran['text'].split('<br>')
        message = '\n'.join([p for p in parts if not re.match(RE_SCRANLINE, p)])
        message += extra_text
        await context.bot.sendPhoto(chat_id=chat_id, photo = img_link, caption=message, parse_mode=ParseMode.HTML, has_spoiler=False)

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
        
        #luukku_is_legal = day >= 1 and day <= min(24, current_day) and current_month == 12
        luukku_is_legal = day >= 1 and day <= 24

        chat_id = update.message.chat_id
        if luukku_is_legal:
            index = day - 1
            scran_left, scran_right = self.luukut[index]
            emoji = self.rigged.choice(self.emojit)
            message = f'<b>Päivän {day} suukkuluukku {emoji}\n</b>Vaan kumpi onkaan herkumpi?'

            print(scran_left['img_path'])
            await context.bot.sendMessage(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)
            await self.sendScran(context, chat_id, scran_left, extra_text='\nDEBUG LEFT')
            await self.sendScran(context, chat_id, scran_right, extra_text='\nDEBUG RIGHT')

            # Trigger vote
        else:
            await context.bot.sendMessage(chat_id=chat_id, text='Eipäs kurkita luukkuja >:(')

