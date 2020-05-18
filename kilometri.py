import collections
import time

import db

extract_nick = lambda update: update.message.from_user["username"]
poista_skandit = lambda s: s.replace("ä", "a").replace("Ä", "A").replace("ö", "o").replace("Ö", "O")

def dbgShowException(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print("Exception: %s" % repr(e))
    return wrapper

class Kilometri:
    Laji = collections.namedtuple("Laji", ("monikko", "partisiippi", "getter", "getTop", "add", "kerroin"))

    lajit = {
        "kavely": Laji("kävelijät", "kävellyt", db.getKavelyt, db.getTopKavelyt, db.addKavely, 1),
        "juoksu": Laji("juoksijat", "juossut", db.getJuoksut, db.getTopJuoksut, db.addJuoksu, 3),
        "pyoraily": Laji("pyöräilijät", "pyöräillyt", db.getPyorailyt, db.getTopPyorailyt, db.addPyoraily, 0.5),
    }

    def __init__(self):
        self.commands = {
            'matkaajat': self.matkaajatHandler,
            'yhdistanikit': self.yhdistaNikitHandler,
            'kmstats': self.statsHandler,
        }

        for lajinnimi, laji in self.lajit.items():
            listauskomento = poista_skandit(laji.monikko)

            self.commands[lajinnimi] = self.__genUrheilinHandler(lajinnimi)
            self.commands[listauskomento] = self.__genGetStatHandler(lajinnimi)

    def getCommands(self):
        return self.commands

    def __genUrheilinHandler(self, lajinnimi):
        def func(*args, **kwargs):
            self.__urheilinHandler(lajinnimi, *args, **kwargs)
        return func

    def __genGetStatHandler(self, lajinnimi):
        def func(*args, **kwargs):
            self.__getStatHandler(lajinnimi, *args, **kwargs)
        return func

    def __parsiAikaLkmNick(self, args):
        aikasuureet = {
            "s":   1,
            "sek": 1,
            "m":   60,
            "min": 60,
            "h":   60 * 60,
            "pv":  60 * 60 * 24,
            "d":   60 * 60 * 24,
            "kk":  60 * 60 * 24 * 30,
            "mo":  60 * 60 * 24 * 30,
            "v":   60 * 60 * 24 * 30 * 365,
            "y":   60 * 60 * 24 * 30 * 365,
        }

        aika = 3 * aikasuureet["kk"]
        aikanimi = "3kk"
        lkm = 10
        nick = None

        for arg in args:
            try:
                lkm = int(arg)
                continue
            except ValueError:
                pass

            for lyhenne, kerroin in aikasuureet.items():
                if (arg.endswith(lyhenne)):
                    try:
                        aika = float(arg.rstrip(lyhenne)) * kerroin
                        aikanimi = arg
                        break
                    except ValueError:
                        pass
            else:
                nick = arg.lstrip("@")

        return (aika, aikanimi, lkm, nick)

    def __urheilinHandler(self, lajinnimi, bot, update, args):
        def printUsage():
            usage = "Usage: /%s <km>" % lajinnimi
            bot.sendMessage(chat_id=update.message.chat_id, text=usage)

        if (len(args) != 1):
            printUsage()
            return

        laji = self.lajit[lajinnimi]
        nick = extract_nick(update)
        try:
            km = float(args[0])
        except ValueError:
            printUsage()
            return

        now = int(time.time())
        laji.add(nick, km, now)
        bot.sendMessage(chat_id=update.message.chat_id,
            text="%s: lisätään %s %.1f km" % (nick, lajinnimi, km))

    def __getStatHandler(self, lajinnimi, bot, update, args):
        def printUsage(komento):
            usage = "Usage: /%s <lkm> [ajalta]" % komento
            bot.sendMessage(chat_id=update.message.chat_id, text=usage)

        # nick-kenttä kerää ylimääräisen paskan jos sitä komennossa on
        laji = self.lajit[lajinnimi]
        aika, aikanimi, lkm, nick = self.__parsiAikaLkmNick(args)
        if (not nick is None):
            printUsage(poista_skandit(laji.monikko))
            return

        top_suoritukset = laji.getTop(time.time() - aika, lkm)
        lista = "\n".join("%s: %.1f km" % stat for stat in top_suoritukset)

        bot.sendMessage(chat_id=update.message.chat_id,
            text="Top %i %s viimeisen %s aikana:\n\n%s" % (lkm, laji.monikko, aikanimi, lista))

    def matkaajatHandler(self, bot, update, args=""):
        print("/matkaajat: %s" % repr((self, bot, update, args)))

    def yhdistaNikitHandler(self, bot, update, args=""):
        pass

    def statsHandler(self, bot, update, args=""):
        def usage():
            bot.sendMessage(chat_id=update.message.chat_id, text="Usage: /kmstats [nick] [ajalta]")

        summaa_tulos = lambda tulos: sum(map(lambda r: r[0], tulos))
        aika, aikanimi, lkm, nick = self.__parsiAikaLkmNick(args)
        alkaen = time.time() - aika

        if (nick is None):
            nick = extract_nick(update)

        stats = tuple((laji, summaa_tulos(laji.getter(nick, alkaen)))
                    for _, laji in self.lajit.items())

        score = sum(laji.kerroin * km for laji, km in stats)
        stat_str = "Viimeisen %s aikana %.1f pistettä\n\n" % (aikanimi, score)

        stat_str += ", ".join(
            "%s %.1f km" % (laji.partisiippi, km)
            for laji, km in stats)

        bot.sendMessage(chat_id=update.message.chat_id,
                        text="%s: %s" % (nick, stat_str))
