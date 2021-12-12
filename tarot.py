from os import listdir
from random import shuffle, randint
from PIL import Image
from tempfile import TemporaryFile
import itertools

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

    # do tempfile fuckenings to give pic to telegram somewhat safely
    # doesn't work (on Windows) without making it delete=False and then killing it later.
    # don't really like the fragmentation but can't figure out a better way.
    fp = TemporaryFile(delete=False)
    reading_image.save(fp, 'jpeg', quality=75)
    return(fp)

def explain_card(text, card_data):
    names = [item[0] for item in card_data]
    explanations = [item[1] for item in card_data]
    rev_exps = [item[2] for item in card_data]
    explanations_to_return = ""

    for (name, explanation, rev_exp) in zip(names, explanations, rev_exps):
        lname = name.lower()
        if lname in text:
            if "reversed " + lname in text or "ylösalaisin " + lname in text or lname + " reversed" in text or lname + " ylösalaisin" in text:
                explanations_to_return += "Reversed " + name + ": " + rev_exp + "\n\n"
                continue
            explanations_to_return += name + ": " + explanation + "\n\n"

    return explanations_to_return


if __name__ == "__main__":
    main()
