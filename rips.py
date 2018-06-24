import random
import sqlite3 as sq
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

    def ripHandler(self, bot, update, args=''):
        chat_id = update.message.chat.id
        if chat_id not in self.rips:
            self.rips[chat_id] = set()
        riptype, rip = random.sample(self.rips[update.message.chat.id], 1)[0]
        self.sendMsg(bot, update, rip, riptype)

    def newripHandler(self, bot, update, args):
        if len(args) == 0:
            key = str(update.message.from_user.id) + str(update.message.chat.id)
            self.waiting_rip[key] = 'newrip'
            self.sendMsg(bot, update, 'Usage: /newrip <ripmessage> or send mediafile for newrip')
            return
        newrip = 'text', ' '.join(args)
        self.addRip(bot, update, newrip)

    def delripHandler(self, bot, update, args):
        if len(args) == 0:
            key = str(update.message.from_user.id) + str(update.message.chat.id)
            self.waiting_rip[key] = 'delrip'
            self.sendMsg(bot, update, 'Usage: /delrip <ripname> or forward mediafile for delete')
            return
        delrip = 'text', ' '.join(args)
        self.delRip(bot, update, delrip)

    def addRip(self, bot, update, newrip):
        chat_id = update.message.chat.id
        if chat_id not in self.rips:
            self.rips[chat_id] = set()
        elif newrip in self.rips[chat_id]:
            self.sendMsg(bot, update, 'Already in rips')
        else:
            self.rips[chat_id].add(newrip)
            type, rip = newrip
            db.addRip(type, rip, chat_id, update.message.from_user.username)

    def delRip(self, bot, update, delrip):
        chat_id = update.message.chat.id
        if chat_id not in self.rips:
            self.rips[chat_id] = set()
            self.sendMsg(bot, update, "Couldn't find rip")
        elif delrip not in self.rips[chat_id]:
            self.sendMsg(bot, update, "Couldn't find rip")
        else:
            self.rips[chat_id].remove(delrip)
            db.delRip(delrip)

    def ripsCountHandler(self, bot, update, args=''):
        chat_id = update.message.chat.id
        if chat_id not in self.rips:
            self.rips[chat_id] = set()
        self.sendMsg(bot, update, str(len(self.rips[chat_id])) + ' rips')

    def messageHandler(self, bot, update):
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
            if key in self.waiting_rip and rip is not None:
                if self.waiting_rip[key] == 'newrip':
                    self.addRip(bot, update, rip)
                elif self.waiting_rip[key] == 'delrip':
                    self.delRip(bot, update, rip)

            self.waiting_rip.pop(key)

            if msg.caption is not None:
                if 'newrip' in msg.caption:
                    self.addRip(bot, update, rip)
                elif 'delrip' in msg.caption:
                    self.delRip(bot, update, rip)

        if msg.text is not None:
            if 'rip' in msg.text.lower():
                self.ripHandler(bot, update)

    def isNewRip(self, msg):
        key = str(msg.from_user.id) + str(msg.chat.id)
        if key in self.waiting_rip:
            return True
        else:
            if msg.caption is not None:
                if 'newrip' in msg.caption or 'delrip' in msg.caption:
                    return True
            return False

    def sendMsg(self, bot, update, msg, msg_type=''):
        if msg_type == 'photo':
            bot.sendPhoto(chat_id=update.message.chat_id, photo=msg, caption='rip in')
        elif msg_type == 'document':
            bot.sendDocument(chat_id=update.message.chat_id, document=msg, caption='rip in')
        elif msg_type == 'location':
            loc = msg.split(',')
            bot.sendLocation(chat_id=update.message.chat_id, longitude=float(loc[0]), latitude=float(loc[1]), caption='rip in')
        elif msg_type == 'voice':
            bot.sendVoice(chat_id=update.message.chat_id, voice=msg, caption='rip in')
        elif msg_type == 'video':
            bot.sendVideo(chat_id=update.message.chat_id, video=msg, caption='rip in')
        elif msg_type == 'text':
            bot.sendMessage(chat_id=update.message.chat_id, text=('rip in ' + msg))
        elif msg_type == 'audio':
            bot.sendAudio(chat_id=update.message.chat_id, audio=msg, caption='rip in')
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text=msg)
