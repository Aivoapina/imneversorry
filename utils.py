from configparser import ConfigParser
import telegram

cfg = ConfigParser()
cfg.read('env.cfg')

BANNED_CHANNELS = cfg['TELEGRAM']['banned_channels']

def oppisWithSameText(definitions, text):
    sameDefs = []
    for defin in definitions:
        if defin[0].lower() == text.lower():
            sameDefs.append(defin[1].lower())
    result = (text, sameDefs)
    return result

def banCheck(func):
    def checkForBan(*args, **kwargs):
        if len(args) > 2 and isinstance(args[2], telegram.update.Update):
            chat_id = str(args[2].message.chat.id)
            if (chat_id in BANNED_CHANNELS):
                return
        return func(*args, **kwargs)
    return checkForBan
