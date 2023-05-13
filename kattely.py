import random
import re
import db
from PIL import Image
from tempfile import TemporaryFile, NamedTemporaryFile
from telegram import Update
from telegram.ext import CallbackContext

class Kattelija:
    def __init__(self):
        self.commands = {'kattely': self.kattelyHandler, 'kaarija': self.kaarijaHandler}
        self.emojis = (':D', ':3', '❤', '☢', '™', '🍞', '🎄', '🤝', '🤗', '🤩', '🦆', '🇫🇮', '🇸🇪')
        self.heads = ('🤔','🤩','😂','😌','😅','😉','😏','😎','😘','😒','😊','🤣','😍','😁','😢','😜','🙂','🙄','😫','😪','🤐','😴','😛','😜','😝','🤑','😲','🤯','🥵','🤬','😠','🤮','🤡','🤠','🥳','🤓','😇','💀','🐸','🐱')
        self.r_hands = ('👌', '✌', '🤞', '✊', '🤜', '👍')
        self.l_hands = ('👌', '✌', '🤞', '✊', '🤛', '👏')
        self.rigged = random.Random()
    
    def getCommands(self):
        return self.commands

    def make_image(self, top_image, rect_size, rect_loc, base_image, transparent=False):
        # Paste senders profile pic on the handshake image
        top_image_resized = top_image.resize(rect_size)
        if transparent:
            base_image.paste(im=top_image_resized, box=rect_loc, mask=top_image_resized)
        else:
            base_image.paste(im=top_image_resized, box=rect_loc)

        # do NamedTempFile because Linux and Windows require completely different methods for this
        # the old Win method of making a non-delete file and then deleting it borks on Linux
        # this will bork on Windows but who cares -- rationale copied over from tarot.py
        fp = NamedTemporaryFile()
        fp.seek(0)
        base_image.save(fp, 'jpeg', quality=75)
        return(fp)

    def random_emoji(self):
        return self.rigged.choice(self.emojis)
    
    def get_profile_pic(self, update: Update, context: CallbackContext):
        user = update.message.from_user
        profile_photos = user.get_profile_photos(limit=1)

        if len(profile_photos.photos) > 0:
            profile_pic_file = profile_photos.photos[0][0].get_file()
            fp = TemporaryFile()
            fp.seek(0)
            profile_pic_file.download(out=fp)
            profile_pic = Image.open(fp)
        else:
            profile_pic = Image.open('resources/kattely/anonymous.jpg')

        return profile_pic

    def random_kaarija(self):
        return self.rigged.choice(self.l_hands) + '🟢🟢' + self.rigged.choice(self.heads) + '🟢🟢' + self.rigged.choice(self.r_hands)

    def kaarijaHandler(self, update: Update, context: CallbackContext):
        if update.message.from_user:
            profile_pic = self.get_profile_pic(update, context)
            base_image = Image.open('resources/kattely/kaarija.jpg')
            overlay_image = Image.open('resources/kattely/kaarija.png')
            image_file = self.make_image(profile_pic, (128, 128), (250, 52), base_image)
            image_file.seek(0)
            image_file = self.make_image(overlay_image, (512, 289), (0, 0), Image.open(image_file), transparent=True)
            image_file.seek(0)
            context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo=open(image_file.name, 'rb'),
                caption='cha :D cha :D cha :D ' + self.random_kaarija()
            )
            image_file.close()
        else:
            return

    def kattelyHandler(self, update: Update, context: CallbackContext):
        if update.message.from_user:
            profile_pic = self.get_profile_pic(update, context)
            base_image = Image.open('resources/kattely/kattely.jpg')
            image_file = self.make_image(profile_pic, (83, 83), (69, 13), base_image)
            image_file.seek(0)
            context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo=open(image_file.name, 'rb'),
                caption='Tervetuloa! ' + self.random_emoji()
            )
            image_file.close()
        else:
            return


    def messageHandler(self, update: Update, context: CallbackContext):
        pass