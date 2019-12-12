import requests
import json
import threading

import logging as log


class Mainari:
    def __init__(self, server, game_ops='', server_admins='', use_ip='False'):
        self.api_url = 'https://api.mcsrvstat.us/2/'
        self.commands = {'minecraft': self.getServerInfo}
        self.is_in_cooldown = False
        self.game_ops = self.parseNicks(game_ops)
        self.server = server
        self.server_admins = self.parseNicks(server_admins)
        self.use_ip = self.parseUseIP(use_ip)

    def getCommands(self):
        return self.commands

    def getServerInfo(self, bot, update, args=''):
        if self.is_in_cooldown:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Cool. Cool cool cool.")
            return

        # Set the cooldown to prevent API abuse and blocking of the bot
        threading.Timer(60.0, self.resetInfoCooldown).start()
        self.is_in_cooldown = True

        r = requests.get(self.api_url + self.server)
        data = r.json()

        message_text = self.parseServerData(data)
        bot.sendMessage(chat_id=update.message.chat_id,
                        parse_mode='Markdown', text=message_text)

    def parseNicks(self, nicks):
        nick_list = nicks.split(',')
        nick_list = [nick.strip() for nick in nick_list]
        return nick_list

    def parseServerData(self, data):
        server_is_offline = not 'online' in data

        # Due to API changes the server can also be offline if it has
        # the 'online' key with a value of False
        if 'online' in data:
            if data['online'] == False:
                server_is_offline = True

        # Data gathered if the server is offline
        if server_is_offline:
            server_status_msg = 'OFFLINE'

        # Data gathered if the server is online
        else:
            server_status_msg = 'Online'
            motd = data['motd']['clean'][0]
            players = data['players']['online']
            players_max = data['players']['max']
            version = data['version']

            if 'players' in data:
                player_list = []

                if 'list' in data['players']:
                    player_list = data['players']['list']
                    
            else:
                player_list = []

            if 'plugins' in data:
                if 'raw' in data['plugins']:
                    plugins = data['plugins']['raw']
            else:
                plugins = []

        # Show the IP or hostname based on what's available and what's wanted
        if 'hostname' in data and not self.use_ip:
            hostname = data['hostname']
        else:
            if self.use_ip:
                hostname = data['ip']
            else:
                hostname = self.server

        # The resulting message is Markdown-formatted
        message_base = '*' + hostname + '*'
        message_extension = '\n`' + server_status_msg + '`'

        if not server_is_offline:
            # MOTD, status and version
            message_extension = ': _' + motd + '_'
            message_extension += '\n`' + server_status_msg + '` - v' + version

            # Plugins
            message_extension += '\n\nPluginit: '
            if not plugins:
                message_extension += '-'
            else:
                first_plugin = True
                for plugin in plugins:
                    if first_plugin:
                        first_plugin = False
                        message_extension += '\n' + plugin
                    else:
                        message_extension += ', ' + plugin

            # Players
            message_extension += '\nPelaajia: ' + \
                str(players) + '/' + str(players_max)
            first_player = True

            for player in player_list:
                if first_player:
                    first_player = False
                    message_extension += '\n'
                else:
                    message_extension += ', '

                if player in self.game_ops:
                    message_extension += '@'

                message_extension += '_' + player + '_'

        # Berate the admins for bad maintenance
        else:
            message_extension += '\n\nMiksei kukaan admineista '
            for admin in self.server_admins:
                message_extension += '@' + admin + ' '
            message_extension += 'tee mitään?!'

        return message_base + message_extension

    def parseUseIP(self, use_ip):
        if use_ip == 'True':
            return True
        else:
            return False

    def resetInfoCooldown(self):
        self.is_in_cooldown = False
