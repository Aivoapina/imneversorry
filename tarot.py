from os import listdir
from random import shuffle, randint
from PIL import Image
from tempfile import NamedTemporaryFile
from telegram import Update
from telegram.ext import CallbackContext
import db
import re



class Tarot:
    def __init__(self):
        self.card_data = db.readSelitykset()
    
    def getCommands(self):
        return dict()

    def get_reading(self, amount):
        # cards in resources folder
        cards = listdir("resources/tarot")
        # magic shuffling
        shuffle(cards)
        reading = []
        for i in range(amount):
            # how 2 reverse a queue
            reading.append(cards.pop())

        # return the tempfile with the image
        return(self.make_image(reading))

    def make_image(self, reading):
        reading_image = Image.new('RGB', (250 * len(reading), 429))

        for i in range(len(reading)):
            # chance for flipped card
            if randint(0,10) == 0:
                card_image = Image.open("resources/tarot/" + reading[i])
                image_flipped = card_image.transpose(Image.FLIP_TOP_BOTTOM)
                reading_image.paste(im=image_flipped, box=(250 * i, 0))
            #normal card
            else:
                reading_image.paste(im=Image.open("resources/tarot/" + reading[i]), box=(250 * i, 0))

        # do NamedTempFile because Linux and Windows require completely different methods for this
        # the old Win method of making a non-delete file and then deleting it borks on Linux
        # this will bork on Windows but who cares
        fp = NamedTemporaryFile()
        fp.seek(0)
        reading_image.save(fp, 'jpeg', quality=75)
        return(fp)

    def explain_card(self, text):
        explanations_to_return = ""

        for datum in self.card_data:
            name = datum[0]
            lname = name.lower()
            if lname in text:
                if "reversed " + lname in text or "ylösalaisin " + lname in text or lname + " reversed" in text or lname + " ylösalaisin" in text:
                    rev_exp = datum[2]
                    explanations_to_return += "Reversed " + name + ": " + rev_exp + "\n\n"
                    continue
                explanation = datum[1]
                explanations_to_return += name + ": " + explanation + "\n\n"

        return explanations_to_return

    async def getTarot(self, update: Update, context: CallbackContext):
        try:
            size = int(update.message.text.lower().split(' ')[1])
        except ValueError :
            await context.bot.sendMessage(chat_id=update.message.chat_id, text=":--D")
            return

        if size < 1 or size > 78:
            await context.bot.sendMessage(chat_id=update.message.chat_id, text=":--D")
            return
        image_file = self.get_reading(size)
        image_file.seek(0)
        if size > 10:
            await context.bot.sendDocument(chat_id=update.message.chat_id, document=open(image_file.name, 'rb'))
        else:
            await context.bot.send_photo(chat_id=update.message.chat_id, photo=open(image_file.name, 'rb'))
        image_file.close()

    async def getReading(self, update: Update, context: CallbackContext):
        message = self.explain_card(update.message.text.lower())
        if message != "":
            await context.bot.sendMessage(chat_id=update.message.chat_id, text=message)

    async def messageHandler(self, update: Update, context: CallbackContext):
        msg = update.message
        if msg.text is not None:
            if re.match(r'^/tarot [0-9]+(?!\S)', msg.text.lower()):
                await self.getTarot(update, context)
            elif "selitä" in msg.text.lower() or "selitys" in msg.text.lower():
                await self.getReading(update, context)
