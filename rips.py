import random

class Rips:
    def __init__(self, ripfile='rips.txt'):
        self.commands = { 'rip': self.ripHandler,
                        'newrip': self.newripHandler,
                        'rips': self.ripsCountHandler,
                        'delrip': self.delripHandler }
        self.rips = set()
        self.ripfile = ripfile
        self.waiting_rip = {}
        self.readRips()

    def getCommands(self):
        return self.commands

    def readRips(self):
        fs = open(self.ripfile, 'a+')
        fs.seek(0)
        for line in fs.read().splitlines():
            sline = line.split(';')
            self.rips.add((sline[0], ';'.join(sline[1:])))
        fs.close()


    def ripHandler(self, bot, update, args=''):
        riptype, rip = random.sample(self.rips, 1)[0]
        self.sendMsg(bot, update, rip, riptype)

    def newripHandler(self, bot, update, args):
        if len(args) == 0:
            self.waiting_rip[update.message.from_user.id] = 'newrip'
            self.sendMsg(bot, update, 'Usage: /newrip <ripmessage> or send mediafile for newrip')
            return
        newrip = 'text', ' '.join(args)
        self.addRip(bot, update, newrip)

    def delripHandler(self, bot, update, args):
        if len(args) == 0:
            self.waiting_rip[update.message.from_user.id] = 'delrip'
            self.sendMsg(bot, update, 'Usage: /delrip <ripname> or forward mediafile for delete')
            return
        delrip = 'text', ' '.join(args)
        self.delRip(bot, update, delrip)

    def addRip(self, bot, update, newrip):
        if newrip in self.rips:
            self.sendMsg(bot, update, 'Already in rips')
        else:
            self.rips.add(newrip)
            fs = open(self.ripfile, 'a+')
            fs.write('{};{}\n'.format(*newrip))
            fs.close()

    def delRip(self, bot, update, delrip):
        if delrip not in self.rips:
            self.sendMsg(bot, update, "Couldn't find rip")
        else:
            self.rips.remove(delrip)
            fs = open(self.ripfile, 'w')
            for line in self.rips:
                fs.write('{};{}\n'.format(*line))
            fs.close()

    def ripsCountHandler(self, bot, update, args=''):
        self.sendMsg(bot, update, str(len(self.rips)) + ' rips')

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

            if msg.from_user.id in self.waiting_rip and rip is not None:
                if self.waiting_rip[msg.from_user.id] == 'newrip':
                    self.addRip(bot, update, rip)
                elif self.waiting_rip[msg.from_user.id] == 'delrip':
                    self.delRip(bot, update, rip)

            self.waiting_rip.pop(msg.from_user.id)

            if msg.caption is not None:
                if 'newrip' in msg.caption:
                    self.addRip(bot, update, rip)
                elif 'delrip' in msg.caption:
                    self.delRip(bot, update, rip)

        if msg.text is not None:
            if 'rip' in msg.text.lower():
                riptype, rip = random.sample(self.rips, 1)[0]
                self.sendMsg(bot, update, rip, riptype)
                return

    def isNewRip(self, msg):
        if msg.from_user.id in self.waiting_rip:
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
