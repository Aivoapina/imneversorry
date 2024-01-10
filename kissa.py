from string import punctuation
from telegram import Update
from telegram.ext import CallbackContext
import db
import re
import random as rigged


class Kissa:
    def __init__(self):
        self.commands = {}
        self.mjäy = 0.00005

    def getCommands(self):
        return self.commands

    def declareBeingThis(self, update: Update, context: CallbackContext):
        message_id = update.message.message_id
        if update.message.reply_to_message is not None:
            message_id = update.message.reply_to_message.message_id

        user_id = update.message.from_user.id
        chat_id = update.message.chat.id

        reserved = db.findWhoIsThis(message_id, chat_id)
        if len(reserved) > 0:
            reserved_user_id = reserved[0][1]

            if reserved_user_id != user_id:
                name = reserved[0][2]
                thing = rigged.choice(["toi", "se"])
                emoji = rigged.choice([":<", ":3", ">:", ":D", "😠", "😤", "🤔", ""])
                punctuation = rigged.choice(["!", ""])
                text = f"et sä voi olla {thing} kun @{name} on jo se{punctuation} {emoji}"
                context.bot.sendMessage(chat_id=chat_id, text=text)
                return

        db.declareBeingThis(message_id, user_id, chat_id,
                            update.message.from_user.username)

    def findWhatUserIs(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        chat_id = update.message.chat.id

        existing_rows = db.findWhatUserIs(user_id, chat_id)
        if len(existing_rows) > 0:
            message_id = existing_rows[0][0]
            emoji = rigged.choice([":>", ":3", "🤔", "😻", "🤩", "😊", ""])
            text = f"sä oot tää {emoji}"
            context.bot.sendMessage(
                chat_id=chat_id, reply_to_message_id=message_id, text=text)

    def messageHandler(self, update: Update, context: CallbackContext):
        msg = update.message
        if msg.text is not None:
            if re.match(r"oon\s(\S+\s){0,4}(tää|toi)", msg.text.lower()):
                self.declareBeingThis(update, context)
            elif 'mikä mä oon' in msg.text.lower():
                self.findWhatUserIs(update, context)
            elif rigged.random() < self.mjäy:                
                context.bot.sendMessage(
                    chat_id=update.message.chat.id, text="".join([chr([ord(x) >> 7 for x in ['㞀', '爀', '㜀', '㲀', 'က', '㒀', '㔀', '㖀', 'む', '㪀', '㦀', 'ᴀ', '⚀', 'ᦀ']][c]) for c in rigged.choice([[12,8,9,4,11,13],[12,6,1,3,3,3,3,4,11,13],[12,6,1,3,4,11,13],[12,5,9,4,11,13],[12,6,1,3,3,3,3,4,0,0,2,4,7,5,10,10,8,4,11,13]])]))
        elif msg.caption is not None:
            if re.match(r"oon\s(\S+\s){0,4}(tää|toi)", msg.caption.lower()):
                self.declareBeingThis(update, context)
