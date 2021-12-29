# Our random.sample usage is unsafe and pylint is unhappy with that.
# Disable pylint for this file (please use pylint, it spots errors/unsafe code pretty well)
# pylint: disable=unsubscriptable-object

from telegram import Update
from telegram.ext import CallbackContext
import requests
import urllib
import random
import re
import db
import time
import datetime
import json
import hashlib
import emoji
from emoji import unicode_codes
from kasvinimi import findKasvinimi

class Teekkari:
    def __init__(self):
        self.commands = {
            'vituttaa': self.getVitutus,
            'viisaus': self.getViisaus,
            'hakemus': self.handleHakemus,
            'pekkauotila': self.getVittuilu,
            'diagnoosi': self.getDiagnoosi,
            'maitonimi': self.getMaitonimi,
            'helveten' : self.getHelveten,
            'pizza': self.getPizza,
            'kalanimi': self.getKalanimi,
            'addsikulla': self.banHammer,
            'sotanimi': self.getSotanimi,
            'kasvinimi': self.getKasvinimi,
            'sukunimi': self.getSukunimi,
            'pottiin': self.getPottiin,
            'kanye': self.getKanye
        }
        self.vituttaaUrl = 'https://fi.wikipedia.org/wiki/Toiminnot:Satunnainen_sivu'
        self.urbaaniUrl = 'https://urbaanisanakirja.com/random/'
        self.urbaaniWordUrl = 'https://urbaanisanakirja.com/word/'
        self.slangopediaUrl = 'http://www.slangopedia.se/slumpa/'
        self.uutineUrl = 'https://www.is.fi/api/laneitems/392841/multilist'
        self.sukunimiUrl = 'https://fi.wiktionary.org/wiki/Toiminnot:Satunnainen_kohde_luokasta/Luokka:Suomen_kielen_sukunimet'
        self.viisaudet = db.readViisaudet()
        self.sanat = db.readSanat()
        self.diagnoosit = db.readDiagnoosit()
        self.maidot = db.readMaidot()
        self.nimet = db.readNimet()
        self.kalat = db.readKalat()
        self.vihanneet = db.readVihanneet()
        self.planetoidit = db.readPlanetoidit()
        self.kulkuneuvot = db.readKulkuneuvot()
        self.linnut = db.readLinnut()
        self.sotilasarvot = db.readSotilasarvot()
        self.sotilasnimet = db.readSotilasnimet()
        self.kasvinimet = db.readKasvinimet()
        self.ennustukset = db.readEnnustukset()
        self.nakutukset = db.readNakutukset()
        self.lastVitun = {}
        self.nextUutine = 0
        self.lastUutineUpdate = 0
        self.uutineet = [ [], [] ]
        self.nextVaihdan = 0
        self.lastPottiin = {}
        self.kanyeRest = 'https://api.kanye.rest/'

    def getCommands(self):
        return self.commands

    def getVittuilu(self, update: Update, context: CallbackContext):
        if random.randint(0, 4) == 0:
            context.bot.sendMessage(chat_id=update.message.chat_id, text='TÖRKEÄÄ SOLVAAMISTA')
        else:
            context.bot.sendMessage(chat_id=update.message.chat_id, text='vittuilu'+random.sample(self.sanat, 1)[0][0])

    def handleHakemus(self, update: Update, context: CallbackContext):
        bot = context.bot

        # https://t.me/c/1363070040/153134
        if 'hacemus' in update.message.text.lower():
            txtHyyva = 'hy-wae'
            txtTapanSut = 'i cill u'
            txtTapanKaikki = 'HEADSHOT'
        elif 'hakemsu' in update.message.text.lower():
            txtHyyva = 'hvy-ää'
            txtTapanSut = 'tapna stu'
            txtTapanKaikki = 'TAPNA KIKKI'
        elif 'h4k3mu5' in update.message.text.lower():
            txtHyyva = 'hy-\/44'
            txtTapanSut = '74p4n 5u7'
            txtTapanKaikki = '74P4|\| K41KK1'
        else:
            txtHyyva = 'hyy-vä'
            txtTapanSut = 'tapan sut'
            txtTapanKaikki = 'TAPAN KAIKKI'

        if random.randint(0, 9) == 0:
            if random.randint(0, 200) == 0:
                bot.sendSticker(chat_id=update.message.chat_id, sticker='CAADBAADJgADiR7LDbglwFauETpzFgQ')
            else:
                bot.sendMessage(chat_id=update.message.chat_id, text=txtHyyva)
        else:
            if random.randint(0, 1000) == 0:
                bot.sendSticker(chat_id=update.message.chat_id, sticker='CAADBAADPwADiR7LDV1aPNns0V1YFgQ')
            elif random.randint(0, 600) == 0:
                bot.sendMessage(chat_id=update.message.chat_id, text=txtTapanKaikki)
            else:
                bot.sendMessage(chat_id=update.message.chat_id, text=txtTapanSut)

    def getViisaus(self, update: Update, context: CallbackContext):
        context.bot.sendMessage(chat_id=update.message.chat_id, text=random.sample(self.viisaudet, 1)[0][0])

    def getVitutus(self, update: Update, context: CallbackContext):
        r = requests.get(self.vituttaaUrl)
        url = urllib.parse.unquote_plus(r.url).split('/')
        vitutus = url[len(url)-1].replace('_', ' ') + " vituttaa"
        context.bot.sendMessage(chat_id=update.message.chat_id, text=vitutus)

    def getSukunimi(self, update: Update, context: CallbackContext):
        r = requests.get(self.sukunimiUrl)
        url = urllib.parse.unquote_plus(r.url).split('/')
        vitutus = url[len(url)-1].replace('_', ' ')
        context.bot.sendMessage(chat_id=update.message.chat_id, text=vitutus)

    def getDiagnoosi(self, update: Update, context: CallbackContext):
        context.bot.sendMessage(chat_id=update.message.chat_id, text=random.sample(self.diagnoosit, 1)[0][0])

    def getMaitonimi(self, update: Update, context: CallbackContext):
        maitoNimi = random.sample(self.maidot, 1)[0][0] + "-" + random.sample(self.nimet, 1)[0][0]
        context.bot.sendMessage(chat_id=update.message.chat_id, text=maitoNimi)

    def getLintunimi(self, update: Update, context: CallbackContext):
        lintu = random.sample(self.linnut, 1)[0][0]
        lintu = re.sub(r'nen$', 's', lintu)
        lintuNimi = lintu + "-" + random.sample(self.nimet, 1)[0][0]
        context.bot.sendMessage(chat_id=update.message.chat_id, text=lintuNimi)

    def getKalanimi(self, update: Update, context: CallbackContext):
        context.bot.sendMessage(chat_id=update.message.chat_id, text=random.sample(self.kalat, 1)[0][0])

    def getMoponimi(self, update: Update, context: CallbackContext):
        kurkku = random.sample(self.vihanneet, 1)[0][0]
        mopo = random.sample(self.kulkuneuvot, 1)[0][0]
        kuu = random.sample(self.planetoidit, 1)[0][0]
        mopoNimi = kurkku + ("", "-")[kurkku[-1:] == mopo[0] and mopo[0] in ('a', 'e', 'i', 'o', 'u', 'y', 'ä', 'ö')] + mopo + " eli " + kuu + ("", "-")[kuu[-1:] == 'e'] + 'eläin ' + kurkku + 'maasta'
        context.bot.sendMessage(chat_id=update.message.chat_id, text=mopoNimi)

    def getSotanimi(self, update: Update, context: CallbackContext):
        arvo = random.sample(self.sotilasarvot, 1)[0][0]
        nimi = random.sample(self.sotilasnimet, 1)[0][0]
        if random.randint(0, 7) == 0:
            if update.message.from_user:
                if update.message.from_user.last_name:
                    nimi = update.message.from_user.last_name
                elif update.message.from_user.first_name:
                    nimi = update.message.from_user.first_name
        sotaNimi = arvo + ' ' + nimi
        context.bot.sendMessage(chat_id=update.message.chat_id, text=sotaNimi)

    def getKasvinimi(self, update: Update, context: CallbackContext):
        if len(context.args) > 0:
            name = " ".join(context.args)
            if len(name) > 32:
                context.bot.sendMessage(chat_id=update.message.chat_id, text=":D")
                return
            kasviNimi = findKasvinimi(self.kasvinimet,
                                      first_name=name, last_name=None)
        elif update.message.from_user:
            if update.message.from_user.first_name:
                first_name = update.message.from_user.first_name
            else:
                first_name = update.message.from_user.username
            if update.message.from_user.last_name:
                last_name = update.message.from_user.last_name
            else:
                last_name = None
            kasviNimi = findKasvinimi(self.kasvinimet,
                                      first_name=first_name,
                                      last_name=last_name)
        else:
            return
        context.bot.sendMessage(chat_id=update.message.chat_id, text=kasviNimi)

    def getNakuttaa(self, update: Update, context: CallbackContext):
        if random.randint(0, 100) == 0:
            context.bot.sendMessage(chat_id=update.message.chat_id, text="Mikä vitun Nakuttaja?")
        else:
            context.bot.sendMessage(chat_id=update.message.chat_id, text=random.sample(self.nakutukset, 1)[0][0] + " vaa")

    def getHalo(self, update: Update, context: CallbackContext):
        context.bot.sendMessage(chat_id=update.message.chat_id, text=random.choice(['Halo', 'Halo?', 'Halo?!']))

    def getPizza(self, update: Update, context: CallbackContext):
        context.bot.sendMessage(chat_id=update.message.chat_id, text='Ananas kuuluu pizzaan!')

    def getNoppa(self, update: Update, context: CallbackContext):
        context.bot.sendDice(chat_id=update.message.chat_id)
        context.bot.sendDice(chat_id=update.message.chat_id)

    def getVaihdan(self, update: Update, context: CallbackContext):
        now = time.time()
        if self.nextVaihdan < now:
            self.nextVaihdan = now + random.randint(60, 180)
            context.bot.sendDice(chat_id=update.message.chat_id)

    def getUrbaani(self):
        webpage = urllib.request.urlopen(self.urbaaniUrl).read().decode("utf-8")
        title = str(webpage).split('<title>')[1].split('</title>')[0]
        sana = title.split(" |")[0]
        return sana

    def getUrbaaniSelitys(self, word):
        webpage = urllib.request.urlopen(self.urbaaniWordUrl + word + '/').read().decode("utf-8")
        meaning = str(webpage).split('<meta name="description" content="')[1].split('">')[0]
        meaning = meaning[meaning.find('.')+2:]
        return meaning

    def getSlango(self):
        r = requests.get(self.slangopediaUrl)
        url = urllib.parse.unquote_plus(r.url, encoding='ISO-8859-1').split('/')
        return str(url[-1].split('=')[-1].lower())

    def getVitun(self, update: Update, context: CallbackContext):
        now = datetime.datetime.now().date()
        userId = update.message.from_user.id
        if userId not in self.lastVitun:
            self.lastVitun[userId] = now
            context.bot.sendMessage(chat_id=update.message.chat_id, text=self.getUrbaani().capitalize() + " vitun " + self.getUrbaani())
        elif self.lastVitun[userId] != now:
            self.lastVitun[userId] = now
            context.bot.sendMessage(chat_id=update.message.chat_id, text=self.getUrbaani().capitalize() + " vitun " + self.getUrbaani())

    def getVitunSelitys(self, update: Update, context: CallbackContext):
        word = update.message.text[11:].lower().replace(' ', '-').replace('ä', 'a').replace('ö', 'o').replace('å', 'a')
        word = re.sub(r"[^a-z0-9\-]", '', word)
        context.bot.sendMessage(chat_id=update.message.chat_id, text=self.getUrbaaniSelitys(word))

    def getVaalikone(self, update: Update, context: CallbackContext):
        context.bot.sendMessage(chat_id=update.message.chat_id, text='Äänestä: ' + str(random.randint(1,424) + 1))

    def getHelveten(self, update: Update, context: CallbackContext):
        context.bot.sendMessage(chat_id=update.message.chat_id,
            text=self.getSlango().capitalize() + ' jävla ' + self.getSlango().lower() )

    def getTEK(self, update: Update, context: CallbackContext):
        if random.randint(0, 50) == 0:
            for word in update.message.text.lower().split(' '):
                if re.match(r'.*tek.*', word) and word != 'tek':
                    context.bot.sendMessage(chat_id=update.message.chat_id, text='ai ' + word.replace('tek', 'TEK') + ' xD')
                    return

    def getTUNI(self, update: Update, context: CallbackContext):
        if random.randint(0, 50) == 0:
            for word in update.message.text.lower().split(' '):
                if re.match(r'.*tuni.*', word) and word != 'tuni':
                    context.bot.sendMessage(chat_id=update.message.chat_id, text='ai ' + word.replace('tuni', 'TUNI') + ' xD')
                    return

    def getEnnustus(self, update: Update, context: CallbackContext):
        now = datetime.datetime.now()
        data = [
            update.message.from_user.id,
            now.day,
            now.month,
            now.year
        ]
        seed = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
        rigged = random.Random(seed)
        ennustus = ""
        n = rigged.randint(0, 2)
        for _x in range(n):
            r = rigged.choice(tuple(unicode_codes.EMOJI_UNICODE))
            ennustus += emoji.emojize(r)
        n = rigged.randint(1, 4)
        for x in range(n):
            ennustus += rigged.sample(self.ennustukset, 1)[0][0]+". "
            m = rigged.randint(0, 2)
            for x in range(m):
                r = rigged.choice(tuple(unicode_codes.EMOJI_UNICODE))
                ennustus += emoji.emojize(r)
        ennustus = ennustus.replace('?.', '.')
        n = rigged.randint(1, 3)
        for x in range(n):
            r = rigged.choice(tuple(unicode_codes.EMOJI_UNICODE))
            ennustus += emoji.emojize(r)
        context.bot.sendMessage(chat_id=update.message.chat_id, text=ennustus)

    def getUutine(self, update: Update, context: CallbackContext):
        now = time.time()
        if self.lastUutineUpdate + 3600 < now:
            self.lastUutineUpdate = now
            req = requests.get(self.uutineUrl)
            uutineet = req.json()[0]
            self.uutineet = [ [], [] ]
            for uutine in uutineet:
                if 'title' in uutine:
                    otsikko = uutine['title']
                    if ' – ' in otsikko:
                        otsikko = otsikko.split(' – ')
                        self.uutineet[0].append(otsikko[0])
                        self.uutineet[1].append(otsikko[1])
        if self.nextUutine < now:
            self.nextUutine = now + random.randint(10, 120)
            uutine = random.choice(self.uutineet[0]) + ' – ' + random.choice(self.uutineet[1])
            context.bot.sendMessage(chat_id=update.message.chat_id, text=uutine)

    def getPottiin(self, update: Update, context: CallbackContext):
        now = datetime.datetime.now().date()
        userId = update.message.from_user.id
        msg = "Pottiin!" if (random.randint(0, 1) == 0) else "kottiin..."
        if userId not in self.lastPottiin:
            self.lastPottiin[userId] = now
            context.bot.sendMessage(chat_id=update.message.chat_id, text=msg)
        elif self.lastPottiin[userId] != now:
            self.lastPottiin[userId] = now
            context.bot.sendMessage(chat_id=update.message.chat_id, text=msg)

    def getKanye(self, update: Update, context: CallbackContext):
        r = requests.get(self.kanyeRest)
        kanye = r.json()["quote"]
        context.bot.sendMessage(chat_id=update.message.chat_id, text=kanye)

    def banHammer(self, update: Update, context: CallbackContext):
        duration = datetime.datetime.now() + datetime.timedelta(minutes=1)
        print(duration)
        context.bot.kickChatMember(update.message.chat.id, update.message.from_user.id, until_date=duration)

    def messageHandler(self, update: Update, context: CallbackContext):
        msg = update.message

        if msg.text is not None:
            if 'vituttaa' in msg.text.lower():
                self.getVitutus(update, context)
            elif 'viisaus' in msg.text.lower():
                self.getViisaus(update, context)
            elif 'pekkauotila' in msg.text.lower():
                self.getVittuilu(update, context)
            elif 'hakemus' in msg.text.lower() or 'hacemus' in msg.text.lower() or 'hakemsu' in msg.text.lower() or 'h4k3mu5' in msg.text.lower():
                self.handleHakemus(update, context)
            elif 'diagno' in msg.text.lower():
                self.getDiagnoosi(update, context)
            elif 'horoskoop' in msg.text.lower():
                self.getEnnustus(update, context)
            elif 'uutine' in msg.text.lower():
                self.getUutine(update, context)
            elif re.match(r'^halo', msg.text.lower()):
                self.getHalo(update, context)
            elif re.match(r'^noppa', msg.text.lower()):
                self.getNoppa(update, context)
            elif re.match(r'^vaihdan', msg.text.lower()):
                self.getVaihdan(update, context)
            elif re.match(r'^vitun', msg.text.lower()):
                self.getVitun(update, context)
            elif re.match(r'^mikä vitun ', msg.text.lower()):
                self.getVitunSelitys(update, context)
            elif re.match(r'^helveten', msg.text.lower()):
                self.getHelveten(update, context)
            elif re.match(r'^/maitonimi', msg.text.lower()):
                self.getMaitonimi(update, context)
            elif re.match(r'^/lintuslanginimi', msg.text.lower()):
                self.getLintunimi(update, context)
            elif re.match(r'^/kurkkumoponimi', msg.text.lower()):
                self.getMoponimi(update, context)
            elif re.match(r'^/sotanimi', msg.text.lower()):
                self.getSotanimi(update, context)
            elif re.match(r'^/kasvinimi', msg.text.lower()):
                self.getKasvinimi(update, context)
            elif re.match(r'^/sukunimi', msg.text.lower()):
                self.getSukunimi(update, context)
            elif re.match(r'.*[tT]ek.*', msg.text):
                self.getTEK(update, context)
            elif re.match(r'.*[tT]uni.*', msg.text):
                self.getTUNI(update, context)
            elif 'nakuttaa' in msg.text.lower():
                self.getNakuttaa(update, context)
            elif re.match(r'^/pottiin', msg.text.lower()):
                self.getPottiin(update, context)
            elif re.match(r'^/kanye', msg.text.lower()):
                self.getKanye(update, context)
