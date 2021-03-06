"""
MIT License
Copyright (c) 2020 GamingGeek

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from discord.ext import commands, tasks
from core.config import Config
import datetime
import discord
import traceback
import json


class SocketRespone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(self.bot, 'socketstats'):
            self.bot.socketstats = json.load(open('socketstats.json'))
        self.save_socket_stats.start()

    @commands.Cog.listener()
    async def on_socket_response(self, payload):
        t = payload['t']
        if t == 'GUILD_CREATE':
            guild = int(payload['d']['id'])
            if guild not in self.bot.configs:
                self.bot.configs[guild] = Config(guild, bot=self.bot, db=self.bot.db)
            await self.bot.configs[guild].load()
        if not t:
            if payload['op'] == 11:
                t = 'HEARTBEAT'
            elif payload['op'] == 10:
                t = 'HELLO'  # hi
            else:
                self.bot.logger.warning(f'$REDUnknown event, $BLUE{t}\n$REDPayload: $BLUE{payload}')
                return
        if t not in self.bot.socketstats:
            self.bot.logger.info(f'$GREENFound new event, $BLUE{t}')
            self.bot.socketstats[t] = 1
        else:
            self.bot.socketstats[t] += 1

    @tasks.loop(minutes=2)
    async def save_socket_stats(self):
        with open('socketstats.json', 'w') as f:
            f.write(json.dumps(self.bot.socketstats))


def setup(bot):
    try:
        bot.add_cog(SocketRespone(bot))
        bot.logger.info(f'$GREENLoaded event $BLUESocketRespone!')
    except Exception as e:
        # errortb = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        bot.logger.error(f'$REDError while loading event $BLUE"SocketRespone"', exc_info=e)
