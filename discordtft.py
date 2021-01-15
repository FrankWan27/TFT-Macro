import discord
import re
import util
from TFTMacro import TFTMacro

class MyClient(discord.Client):
    async def on_ready(self):
        print('!tft Ready! ', self.user, flush=True)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if re.match(r'^\.', message.clean_content):
            content = util.removeNonAscii(message.clean_content[1:])
            content = util.removeLeadSpaces(content)
            async with message.channel.typing():
                output = tft.doCommand(content)

            await message.channel.send(output)
tft = TFTMacro()
client = MyClient()
client.run(util.token)