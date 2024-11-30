from telegram import Update
from telegram.ext import CallbackContext
import random as rigged

class Noppa:

    def __init__(self):
        self.commands = {'heitae': self.throw, 'throw': self.throw}
        self.table = '┻━┻'
        self.flipper = '(╯°□°)╯︵'

    def getCommands(self):
        return self.commands

    def throwDice(self, n: int, sides: int):
        if n < 1 or n > 1000:
            raise Exception ("Invalid number of dice.")
        if sides < 1 or sides > 100:
            raise Exception("Invalid number of sides.")

        throws = []
        for i in range(n):
            result = rigged.randint(1, sides)
            throws.append(result)

        return throws

    async def throw(self, update: Update, context: CallbackContext):
        try:
            n, sides = map(int, context.args[0].split('d'))
            throws = self.throwDice(n, sides)
            results_msg = "{}, yhteensä: {}\nSilmäluvut: {}".format(context.args[0], sum(throws), throws)
            await context.bot.sendMessage(chat_id=update.message.chat_id, text=results_msg)
        except Exception as e:
            print(e)
            await context.bot.sendMessage(chat_id=update.message.chat_id, text="%s%s" % (self.flipper, self.table))
