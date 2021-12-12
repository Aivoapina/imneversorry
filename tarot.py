from os import listdir
from random import shuffle, randint
from PIL import Image
from tempfile import NamedTemporaryFile
import db

card_data = db.readSelitykset()


def main():
    get_reading(78)

def get_reading(amount):
    # cards in resources folder
    cards = listdir("resources/tarot")
    # magic shuffling
    shuffle(cards)
    reading = []
    for i in range(amount):
        # how 2 reverse a queue
        reading.append(cards.pop())

    # return the tempfile with the image
    return(make_image(reading))

def make_image(reading):
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

def explain_card(text):
    explanations_to_return = ""

    for datum in card_data:
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


if __name__ == "__main__":
    main()
