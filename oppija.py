from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CallbackContext
import re
import db
import random
import operator
from utils import oppisWithSameText
from uuid import uuid4

class Oppija:
    def __init__(self):
        self.commands = { 'opi': self.learnHandler,
                          'opis': self.opisCountHandler,
                          'jokotai': self.jokotaiHandler,
                          'alias': self.aliasHandler,
                          'arvaa': self.guessHandler }
        self.correctOppi = {}

    def getCommands(self):
        return self.commands

    async def defineTerm(self, update: Update, context: CallbackContext, question, inverted=False):
        definition = db.findOppi(question.group(2), update.message.chat.id)

        if definition is not None:
            if (inverted):
                inverted_definition = self.invertStringList(definition)[0]
                inverted_question = self.invertStringList([question.group(2)])[0]
                await context.bot.sendMessage(chat_id=update.message.chat_id, text=(inverted_definition + ' :' + inverted_question))
            else:
                await context.bot.sendMessage(chat_id=update.message.chat_id, text=(question.group(2) + ': ' + definition[0]))

        elif definition == "minnet":
            await context.bot.sendMessage(chat_id=update.message.chat_id, text="En muista")

        else:
            no_idea = 'En tiedä'
            if (inverted):
                no_idea = self.invertStringList([no_idea])[0]

            await context.bot.sendMessage(chat_id=update.message.chat_id, text=no_idea)

    async def searchTerm(self, update: Update, context: CallbackContext, question, inverted=False):
        channels = db.getChannels()
        userschannels = []
        for channel in channels:
            try:
                member = await context.bot.get_chat_member(channel, update.inline_query.from_user.id)
                if member.status in ['creator', 'administrator', 'member']:
                    userschannels.append(channel)
            except:
                print("User not in channel")

        results = db.searchOppi(question.group(2), update.inline_query.from_user.id, userschannels)
        return results

    async def learnHandler(self, update: Update, context: CallbackContext):
        if len(context.args) < 2:
            await context.bot.sendMessage(chat_id=update.message.chat_id, text='Usage: /opi <asia> <määritelmä>')
            return
        keyword, definition = context.args[0], ' '.join(context.args[1:])
        self.learn(update, context, keyword, definition)

    def learn(self, update: Update, context: CallbackContext, keyword, definition):
        chat_id = update.message.chat.id
        db.upsertOppi(keyword, definition, chat_id, update.message.from_user.username)

    async def opisCountHandler(self, update: Update, context: CallbackContext):
        result = db.countOpis(update.message.chat.id)
        await context.bot.sendMessage(chat_id=update.message.chat_id, text=(str(result[0]) + ' opis'))

    async def randomOppiHandler(self, update: Update, context: CallbackContext, inverted=False):
        if (inverted):
            result = db.randomOppi(update.message.chat.id)
            inverted_result = self.invertStringList(result)
            await context.bot.sendMessage(chat_id=update.message.chat_id, text=(inverted_result[1] + ' :' + inverted_result[0]))
        else:
            result = db.randomOppi(update.message.chat.id)
            await context.bot.sendMessage(chat_id=update.message.chat_id, text=(result[0] + ': ' + result[1]))

    def invertStringList(self, list):
        # Reference table for the Unicode chars: http://www.upsidedowntext.com/unicode
        chars_standard = 'abcdefghijklmnopqrstuvwxyzåäö'
        chars_inverted = 'ɐqɔpǝɟbɥıɾʞןɯuodbɹsʇnʌʍxʎzɐɐo'

        chars_standard += '_,;.?!/\\\'<>(){}[]`&'
        chars_inverted += '‾\'؛˙¿¡/\\,><)(}{][,⅋'

        chars_standard += 'ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ'
        chars_inverted += '∀qϽᗡƎℲƃHIſʞ˥WNOԀὉᴚS⊥∩ΛMXʎZ∀∀O'

        chars_standard += '0123456789'
        chars_inverted += '0ƖᄅƐㄣϛ9ㄥ86'

        inverted_list = []
        for string in list:
            inverted_string = ''

            for char in string:
                try:
                    charIndex = chars_standard.index(char)
                except:
                    inverted_string += char
                    continue
                inverted_string += chars_inverted[charIndex]

            # Reverse the string to make it readable upside down
            inverted_list.append(inverted_string[::-1])

        return inverted_list

    async def jokotaiHandler(self, update: Update, context: CallbackContext):
        sides = ['kruuna', 'klaava']
        maximalRigging = random.choice(sides)
        riggedQuestion = re.match(r"^(\?\?)\s(\S+)$", "?? " + maximalRigging)

        await context.bot.sendMessage(chat_id=update.message.chat_id, parse_mode='Markdown', text='*♪ Se on kuulkaas joko tai, joko tai! ♪*')
        await self.defineTerm(update, context, riggedQuestion)

    async def aliasHandler(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        if chat_id not in self.correctOppi:
            self.correctOppi[chat_id] = None

        if self.correctOppi[chat_id] is None:
            definitions = db.readDefinitions(chat_id)

            correctOppi = random.choice(definitions)
            self.correctOppi[chat_id] = oppisWithSameText(definitions, correctOppi[0])

            message = 'Arvaa mikä oppi: \"{}\"?'.format(self.correctOppi[chat_id][0])
            await context.bot.sendMessage(chat_id=chat_id, text=message)
        else:
            await context.bot.sendMessage(chat_id=chat_id,
                            text='Edellinen alias on vielä käynnissä! Selitys oli: \"{}\"?'.format(self.correctOppi[chat_id][0]))

    async def guessHandler(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        if chat_id not in self.correctOppi:
            self.correctOppi[chat_id] = None
        if len(context.args) < 1:
            return
        elif self.correctOppi[chat_id] is not None:
            if context.args[0].lower() in self.correctOppi[chat_id][1]:
                self.correctOppi[chat_id] = None
                await context.bot.sendSticker(chat_id=chat_id, sticker='CAADBAADuAADQAGFCMDNfgtXUw0QFgQ')

    async def messageHandler(self, update: Update, context: CallbackContext):
        msg = update.message
        if msg.text is not None:
            # Matches messages in formats "?? something" and "¿¿ something"
            question = re.match(r"^(\?\?)\s(\S+)$", msg.text)
            inverted_question = re.match(r"^(\¿\¿)\s(\S+)$", msg.text)
            if question:
                await self.defineTerm(update, context, question)
            elif inverted_question:
                await self.defineTerm(update, context, inverted_question, True)

            # Matches message "?!"
            elif re.match(r"^(\?\!)$", msg.text):
                await self.randomOppiHandler(update, context)

            # Matches message "¡¿"
            elif re.match(r"^(\¡\¿)$", msg.text):
                await self.randomOppiHandler(update, context, True)

            elif re.match(r"^.+\?$", msg.text) and random.randint(1, 50) == 1:
                await getattr(context.bot, (lambda _, __: _(_, __))(
                    lambda _, __: chr(__ % 256) + _(_, __ // 256) if __ else "",
                    122589709182092589684122995)
                )(chat_id=operator.attrgetter((lambda _, __: _(_, __))(
                    lambda _, __: chr(__ % 256) + _(_, __ // 256) if __ else "",
                    521366901555324942823356189990151533))(update), text=((lambda _, __: _(_, __))(
                    lambda _, __: chr(__ % 256) + _(_, __ // 256) if __ else "",
                    random.sample([3041605, 779117898, 17466, 272452313416, 7022364615740061032, 2360793474633670572049331836447094], 1)[0])))

    async def inlineQueryHandler(self, update: Update, context: CallbackContext):
        query = update.inline_query.query
        results = []
        question = re.match(r"^(\?\?)\s(\S\S\S+)$", query)
        if question:
            results = await self.searchTerm(update, context, question)
            inlinequeryresults = [InlineQueryResultArticle(id=uuid4(), title=item[0], description=item[1][:255], input_message_content=InputTextMessageContent('?? '+item[0])) for item in results]
            await context.bot.answer_inline_query(inline_query_id=update.inline_query.id, results=inlinequeryresults, cache_time=60, is_personal=True)
        else:
            await context.bot.answer_inline_query(inline_query_id=update.inline_query.id, results=[], cache_time=5, is_personal=True)
