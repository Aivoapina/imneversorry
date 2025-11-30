from telegram import Update , Poll
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

import datetime
import db
import random
import re

SANTA_SEED = 0xDEADBEED

RE_SCRANLINE = r'.*[Ss]cran [👍👎].*'

SYMBOL_LEFT = '🅰️'
SYMBOL_RIGHT = '🅱️'

def getScran(id):
    t = db.getScran(id)
    return {
        'text': t[0],
        'upvotes': t[1],
        'downvotes': t[2],
        'img_path': t[3]
    }


def get_scran_name(scran):
    parts = scran['text'].split('<br>')
    return parts[0][:min(80, len(parts[0]))].replace('&amp;', '&')


def scoreScran(scran):
    return scran['upvotes'] - scran['downvotes']


def scoreEmoji(score):
    if score > 0:
        return '👍'
    elif score < 0:
        return '👎'
    else:
        return '🐸'


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
        self.polls = [None] * 24
        self.joulu_emojit = ('❄️', '☃️', '🤶', '🎁', '️🛷', '🎇', '🎄', '✨', '🎅')
        self.herkku_emojit = ('😋', '🤤', '🍴', '😍', '💦', '🫦')


    def getCommands(self):
        return self.commands
    
    async def sendScran(self, context, chat_id, scran, extra_text=''):
        img_link = scran['img_path']
        parts = scran['text'].split('<br>')
        message = '\n'.join([p for p in parts if not re.match(RE_SCRANLINE, p)])
        message += extra_text
        await context.bot.sendPhoto(chat_id=chat_id, photo = img_link, caption=message, parse_mode=ParseMode.HTML, has_spoiler=False)

    async def sendPoll(self, context, chat_id, scran_left, scran_right, day):
        score_left = scoreScran(scran_left)
        score_right = scoreScran(scran_right)
        winner_id = 0 if score_left > score_right else 1

        message = (f'{self.rigged.choice(self.joulu_emojit)} Päivän {day} suukkuluukku {self.rigged.choice(self.herkku_emojit)}\n'
            f'Herkkua on siinä monenlaista {self.rigged.choice(self.herkku_emojit)}\n'
            'Vaan kumpi onkaan herkumpi?')

        name_left = get_scran_name(scran_left)
        name_right = get_scran_name(scran_right)

        options = [f'{SYMBOL_LEFT} {name_left}', f'{SYMBOL_RIGHT} {name_right}']
        messageObj = self.polls[day]
        if messageObj is None:
            messageObj = await context.bot.send_poll(
                chat_id,
                message,
                options,
                is_anonymous=False,
                type=Poll.QUIZ,
                correct_option_id=winner_id,
            )
            self.polls[day] = messageObj
        else:
            await messageObj.forward(chat_id)

        winner_score = max(score_left, score_right)
        loser_score = min(score_left, score_right)
        scores_text = f'{winner_score} {scoreEmoji(winner_score)} VS {loser_score} {scoreEmoji(loser_score)}'
        await context.bot.sendMessage(chat_id, f'<b>PISTEET:</b>\n<span class="tg-spoiler">{scores_text}</span>', parse_mode=ParseMode.HTML)

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

            await self.sendScran(context, chat_id, scran_left, extra_text=f'\n{SYMBOL_LEFT}')
            await self.sendScran(context, chat_id, scran_right, extra_text=f'\n{SYMBOL_RIGHT}')
            await self.sendPoll(context, chat_id, scran_left, scran_right, day)

            # Trigger vote
        else:
            await context.bot.sendMessage(chat_id=chat_id, text='Eipäs kurkita luukkuja >:(')

