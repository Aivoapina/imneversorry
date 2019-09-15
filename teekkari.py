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
        }
        self.vituttaaUrl = 'https://fi.wikipedia.org/wiki/Toiminnot:Satunnainen_sivu'
        self.urbaaniUrl = 'https://urbaanisanakirja.com/random/'
        self.urbaaniWordUrl = 'https://urbaanisanakirja.com/word/'
        self.slangopediaUrl = 'http://www.slangopedia.se/slumpa/'
        self.uutineUrl = 'https://www.is.fi/tuoreimmat/'
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
        self.ennustukset = db.readEnnustukset()
        self.lastVitun = {}
        self.nextUutine = 0
        self.lastUutineUpdate = 0
        self.uutineet = [ [], [] ]

    def getCommands(self):
        return self.commands

    def getVittuilu(self, bot, update, args=''):
        if random.randint(0, 4) == 0:
            bot.sendMessage(chat_id=update.message.chat_id, text='TÖRKEÄÄ SOLVAAMISTA')
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text='vittuilu'+random.sample(self.sanat, 1)[0][0])

    def handleHakemus(self, bot, update, args=''):
        if random.randint(0, 9) == 0:
            bot.sendSticker(chat_id=update.message.chat_id, sticker='CAADBAADJgADiR7LDbglwFauETpzFgQ')
        else:
            bot.sendSticker(chat_id=update.message.chat_id, sticker='CAADBAADPwADiR7LDV1aPNns0V1YFgQ')

    def getViisaus(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text=random.sample(self.viisaudet, 1)[0][0])

    def getVitutus(self, bot, update, args=''):
        r = requests.get(self.vituttaaUrl)
        url = urllib.parse.unquote_plus(r.url).split('/')
        vitutus = url[len(url)-1].replace('_', ' ') + " vituttaa"
        bot.sendMessage(chat_id=update.message.chat_id, text=vitutus)

    def getDiagnoosi(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text=random.sample(self.diagnoosit, 1)[0][0])

    def getMaitonimi(self, bot, update, args=''):
        maitoNimi = random.sample(self.maidot, 1)[0][0] + "-" + random.sample(self.nimet, 1)[0][0]
        bot.sendMessage(chat_id=update.message.chat_id, text=maitoNimi)

    def getLintunimi(self, bot, update, args=''):
        lintu = random.sample(self.linnut, 1)[0][0]
        lintu = re.sub(r'nen$', 's', lintu)
        lintuNimi = lintu + "-" + random.sample(self.nimet, 1)[0][0]
        bot.sendMessage(chat_id=update.message.chat_id, text=lintuNimi)

    def getKalanimi(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text=random.sample(self.kalat, 1)[0][0])

    def getMoponimi(self, bot, update, args=''):
        kurkku = random.sample(self.vihanneet, 1)[0][0]
        mopo = random.sample(self.kulkuneuvot, 1)[0][0]
        kuu = random.sample(self.planetoidit, 1)[0][0]
        mopoNimi = kurkku + ("", "-")[kurkku[-1:] == mopo[0] and mopo[0] in ('a', 'e', 'i', 'o', 'u', 'y', 'ä', 'ö')] + mopo + " eli " + kuu + ("", "-")[kuu[-1:] == 'e'] + 'eläin ' + kurkku + 'maasta'
        bot.sendMessage(chat_id=update.message.chat_id, text=mopoNimi)

    def getSotanimi(self, bot, update, args=''):
        arvo = random.sample(self.sotilasarvot, 1)[0][0]
        nimi = random.sample(self.sotilasnimet, 1)[0][0]
        if random.randint(0, 7) == 0:
            if update.message.from_user:
                if update.message.from_user.last_name:
                    nimi = update.message.from_user.last_name
                elif update.message.from_user.first_name:
                    nimi = update.message.from_user.first_name
        sotaNimi = arvo + ' ' + nimi
        bot.sendMessage(chat_id=update.message.chat_id, text=sotaNimi)

    def getHalo(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text=random.choice(['Halo', 'Halo?', 'Halo?!']))

    def getPizza(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text='Ananas kuuluu pizzaan!')

    def getNoppa(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text='Heitit ' + str(random.randint(1, 6)) + ' ja ' + str(random.randint(1, 6)) + '.')

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

    def getVitun(self, bot, update, args=''):
        now = datetime.datetime.now().date()
        userId = update.message.from_user.id
        if userId not in self.lastVitun:
            self.lastVitun[userId] = now
            bot.sendMessage(chat_id=update.message.chat_id, text=self.getUrbaani().capitalize() + " vitun " + self.getUrbaani())
        elif self.lastVitun[userId] != now:
            self.lastVitun[userId] = now
            bot.sendMessage(chat_id=update.message.chat_id, text=self.getUrbaani().capitalize() + " vitun " + self.getUrbaani())

    def getVitunSelitys(self, bot, update, args=''):
        word = update.message.text[11:].lower().replace(' ', '-').replace('ä', 'a').replace('ö', 'o').replace('å', 'a')
        word = re.sub(r"[^a-z0-9\-]", '', word)
        bot.sendMessage(chat_id=update.message.chat_id, text=self.getUrbaaniSelitys(word))

    def getVaalikone(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id, text='Äänestä: ' + str(random.randint(1,424) + 1))

    def getHelveten(self, bot, update, args=''):
        bot.sendMessage(chat_id=update.message.chat_id,
            text=self.getSlango().capitalize() + ' jävla ' + self.getSlango().lower() )

    def getTEK(self, bot, update, args=''):
        if random.randint(0, 12) == 0:
            for word in update.message.text.lower().split(' '):
                if re.match(r'.*tek.*', word) and word != 'tek':
                    bot.sendMessage(chat_id=update.message.chat_id, text='ai ' + word.replace('tek', 'TEK') + ' xD')
                    return
                
    def getTUNI(self, bot, update, args=''):
        if random.randint(0, 5) == 0:
            for word in update.message.text.lower().split(' '):
                if re.match(r'.*tuni.*', word) and word != 'tuni':
                    bot.sendMessage(chat_id=update.message.chat_id, text='ai ' + word.replace('tuni', 'TUNI') + ' xD')
                    return

    def getEnnustus(self, bot, update, args=''):
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
        for x in range(n):
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
        bot.sendMessage(chat_id=update.message.chat_id, text=ennustus)

    def getUutine(self, bot, update, args=''):
        now = time.time()
        if self.lastUutineUpdate + 3600 < now:
            self.lastUutineUpdate = now
            webpage = urllib.request.urlopen(self.uutineUrl).read().decode("utf-8")
            uutine = str(webpage)
            self.uutineet = [ [], [] ]
            for otsikko in uutine.split('<li class="list-item">'):
                otsikko = otsikko.replace('\n', '').replace('\r', '')
                if '<div class="content">' in otsikko:
                    otsikko = otsikko.split('<div class="content">')[1].split('</div>')[0]
                    if ' – ' in otsikko:
                        otsikko = otsikko.split(' – ')
                        self.uutineet[0].append(otsikko[0])
                        self.uutineet[1].append(otsikko[1])
        if self.nextUutine < now:
            self.nextUutine = now + random.randint(10, 120)
            uutine = random.choice(self.uutineet[0]) + ' – ' + random.choice(self.uutineet[1])
            bot.sendMessage(chat_id=update.message.chat_id, text=uutine)

    def banHammer(self, bot, update, args=''):
        duration = datetime.datetime.now() + datetime.timedelta(minutes=1)
        print(duration)
        bot.kickChatMember(update.message.chat.id, update.message.from_user.id, until_date=duration)

    def messageHandler(self, bot, update):
        msg = update.message
        #print(msg)
        if msg.text is not None:
            if 'vituttaa' in msg.text.lower():
                self.getVitutus(bot, update)
            elif 'viisaus' in msg.text.lower():
                self.getViisaus(bot, update)
            elif 'pekkauotila' in msg.text.lower():
                self.getVittuilu(bot, update)
            elif 'hakemus' in msg.text.lower():
                self.handleHakemus(bot, update)
            elif 'diagno' in msg.text.lower():
                self.getDiagnoosi(bot, update)
            elif 'horoskoop' in msg.text.lower():
                self.getEnnustus(bot, update)
            elif 'uutine' in msg.text.lower():
                self.getUutine(bot, update)
            elif re.match(r'^halo', msg.text.lower()):
                self.getHalo(bot, update)
            elif re.match(r'^noppa', msg.text.lower()):
                self.getNoppa(bot, update)
            elif re.match(r'^vitun', msg.text.lower()):
                self.getVitun(bot, update)
            elif re.match(r'^mikä vitun ', msg.text.lower()):
                self.getVitunSelitys(bot, update)
            elif re.match(r'^helveten', msg.text.lower()):
                self.getHelveten(bot, update)
            elif re.match(r'^/maitonimi', msg.text.lower()):
                self.getMaitonimi(bot, update)
            elif re.match(r'^/lintuslanginimi', msg.text.lower()):
                self.getLintunimi(bot, update)
            elif re.match(r'^/kurkkumoponimi', msg.text.lower()):
                self.getMoponimi(bot, update)
            elif re.match(r'^/sotanimi', msg.text.lower()):
                self.getSotanimi(bot, update)
            elif re.match(r'.*[tT]ek.*', msg.text):
                self.getTEK(bot, update)
            elif re.match(r'.*[tT]uni.*', msg.text):
                self.getTUNI(bot, update)
