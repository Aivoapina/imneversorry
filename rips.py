# Our random.sample usage is unsafe and pylint is unhappy with that.
# Disable pylint for this file (please use pylint, it spots errors/unsafe code pretty well)
# pylint: disable=unsubscriptable-object

from telegram import Update
from telegram.ext import CallbackContext
import random
import db

class Rips:
    def __init__(self):
        self.commands = { 'rip': self.ripHandler,
                        'newrip': self.newripHandler,
                        'rips': self.ripsCountHandler,
                        'delrip': self.delripHandler }
        self.rips = db.readRips()
        self.waiting_rip = {}

    def getCommands(self):
        return self.commands

    async def ripHandler(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        if chat_id not in self.rips:
            self.rips[chat_id] = set()
            return # Cannot select 1 random sample from 0 samples
        # pylint: disable=unpacking-non-sequence
        riptype, rip = random.sample(self.rips[chat_id], 1)[0]
        await self.sendMsg(update, context, rip, riptype)

    async def newripHandler(self, update: Update, context: CallbackContext):
        if len(context.args) == 0:
            key = str(update.message.from_user.id) + str(update.message.chat.id)
            self.waiting_rip[key] = 'newrip'
            await self.sendMsg(update, context, 'Usage: /newrip <ripmessage> or send mediafile for newrip')
            return
        newrip = 'text', ' '.join(context.args)
        await self.addRip(update, context, newrip)

    async def delripHandler(self, update: Update, context: CallbackContext):
        if len(context.args) == 0:
            key = str(update.message.from_user.id) + str(update.message.chat.id)
            self.waiting_rip[key] = 'delrip'
            await self.sendMsg(update, context, 'Usage: /delrip <ripname> or forward mediafile for delete')
            return
        delrip = 'text', ' '.join(context.args)
        self.delRip(update, context, delrip)

    async def addRip(self, update: Update, context: CallbackContext, newrip):
        chat_id = update.message.chat.id
        if chat_id not in self.rips:
            self.rips[chat_id] = set()
        elif newrip in self.rips[chat_id]:
            await self.sendMsg(update, context, 'Already in rips')
        else:
            self.rips[chat_id].add(newrip)
            type, rip = newrip
            db.addRip(type, rip, chat_id, update.message.from_user.username)

    async def delRip(self, update: Update, context: CallbackContext, delrip):
        chat_id = update.message.chat.id
        if chat_id not in self.rips:
            self.rips[chat_id] = set()
            await self.sendMsg(update, context, "Couldn't find rip")
        elif delrip not in self.rips[chat_id]:
            await self.sendMsg(update, context, "Couldn't find rip")
        else:
            self.rips[chat_id].remove(delrip)
            db.delRip(delrip)

    async def ripsCountHandler(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        if chat_id not in self.rips:
            self.rips[chat_id] = set()
        await self.sendMsg(update, context, str(len(self.rips[chat_id])) + ' rips')

    async def messageHandler(self, update: Update, context: CallbackContext):
        msg = update.message
        if self.isNewRip(msg):
            if len(msg.photo) > 0:
                rip = 'photo', msg.photo[1].file_id
            elif msg.document is not None:
                rip = 'document', msg.document.file_id
            elif msg.voice is not None:
                rip = 'voice', msg.voice.file_id
            elif msg.location is not None:
                rip = 'location', (str(msg.location.longitude) + ',' + str(msg.location.latitude))
            elif msg.video is not None:
                rip = 'video', msg.video.file_id
            elif msg.audio is not None:
                rip = 'audio', msg.audio.file_id
            else:
                rip = None

            key = str(msg.from_user.id) + str(msg.chat.id)
            if key in self.waiting_rip:
                if rip is not None:
                    if self.waiting_rip[key] == 'newrip':
                        await self.addRip(update, context, rip)
                    elif self.waiting_rip[key] == 'delrip':
                        await self.delRip(update, context, rip)
                self.waiting_rip.pop(key)

            if msg.caption is not None:
                if 'newrip' in msg.caption:
                    await self.addRip(update, context, rip)
                elif 'delrip' in msg.caption:
                    await self.delRip(update, context, rip)

        if msg.text is not None:
            if 'rip' in msg.text.lower():
                await self.ripHandler(update, context)

    def isNewRip(self, msg):
        key = str(msg.from_user.id) + str(msg.chat.id)
        if key in self.waiting_rip:
            return True
        else:
            if msg.caption is not None:
                if 'newrip' in msg.caption or 'delrip' in msg.caption:
                    return True
            return False

    async def sendMsg(self, update: Update, context: CallbackContext, msg, msg_type=''):
        if msg_type == 'photo':
            await context.bot.sendPhoto(chat_id=update.message.chat_id, photo=msg, caption='rip in')
        elif msg_type == 'document':
            await context.bot.sendDocument(chat_id=update.message.chat_id, document=msg, caption='rip in')
        elif msg_type == 'location':
            loc = msg.split(',')
            await context.bot.sendLocation(chat_id=update.message.chat_id, longitude=float(loc[0]), latitude=float(loc[1]), caption='rip in')
        elif msg_type == 'voice':
            await context.bot.sendVoice(chat_id=update.message.chat_id, voice=msg, caption='rip in')
        elif msg_type == 'video':
            await context.bot.sendVideo(chat_id=update.message.chat_id, video=msg, caption='rip in')
        elif msg_type == 'text':
            await context.bot.sendMessage(chat_id=update.message.chat_id, text=('rip in ' + msg))
        elif msg_type == 'audio':
            await context.bot.sendAudio(chat_id=update.message.chat_id, audio=msg, caption='rip in')
        else:
            await context.bot.sendMessage(chat_id=update.message.chat_id, text=msg)
