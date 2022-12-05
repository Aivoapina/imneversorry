import random
import re
import db
from PIL import Image
from tempfile import TemporaryFile, NamedTemporaryFile
from telegram import Update
from telegram.ext import CallbackContext

class Kattelija:
    def __init__(self):
        self.commands = {'kattely': self.kattelyHandler}
        self.emojis = (':D', ':3', '❤', '☢', '™', '🍞', '🎄', '🤝', '🤗', '🤩', '🦆', '🇫🇮', '🇸🇪')
        self.rigged = random.Random()
    
    def getCommands(self):
        return self.commands

    def make_image(self, profile_pic):
        # Paste senders profile pic on the handshake image
        rect_size = (83,83)
        rect_loc = (69, 13)
        base_image = Image.open('resources/kattely/kattely.jpg')
        profile_pic_resized = profile_pic.resize(rect_size)
        base_image.paste(im=profile_pic_resized, box=rect_loc)

        # do NamedTempFile because Linux and Windows require completely different methods for this
        # the old Win method of making a non-delete file and then deleting it borks on Linux
        # this will bork on Windows but who cares -- rationale copied over from tarot.py
        fp = NamedTemporaryFile()
        fp.seek(0)
        base_image.save(fp, 'jpeg', quality=75)
        return(fp)

    def random_emoji(self):
        return self.rigged.choice(self.emojis)

    def kattelyHandler(self, update: Update, context: CallbackContext):
        if update.message.from_user:

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

            image_file = self.make_image(profile_pic)
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