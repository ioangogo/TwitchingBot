import configparser, os
from twitchio.ext import commands

class Bot(commands.Bot):


    def __init__(self, token, clientID, nick, prefix, channels):
        super().__init__(irc_token=token, client_id=clientID, nick=nick, prefix=prefix,
                         initial_channels=channels)
        self.TitleFile = open("titles.txt", "a+")

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        await self.handle_commands(message)

    # Commands use a decorator...
    @commands.command(name='cleartitles')
    async def cleartitles(self, ctx):
        if ctx.author.is_mod:
            self.TitleFile.close()
            open("titles.txt", "w").close()
            self.TitleFile = open("titles.txt", "a+")
            await ctx.send("Cleared Title list")

    @commands.command(name='suggest')
    async def suggestTitle(self, ctx):
        await ctx.send(f"added @{ctx.author.name}")
        self.TitleFile.write(f"{ctx.author.name}: {ctx.message.content.replace('!suggest ', '')}\r\n")
        self.TitleFile.flush()

config = configparser.ConfigParser()
chans=[]

if os.path.exists("config.ini"):
    config.read("config.ini")
    if 'API' in config:
        apiconfig = config["API"]
        token = apiconfig["irc_token"]
        clientID = apiconfig["client_id"]
        if 'CHAT' in config:
            chatconf = config["CHAT"]
            nick = chatconf["nick"]
            prefix = chatconf["prefix"]
            if "CHANNELS" in config:
                channelsCon = config["CHANNELS"]
                for chan in channelsCon:
                    chans.append(chan)
                bot = Bot(token, clientID, nick, prefix, chans)
                bot.run()

else:
    print("Make a config.ini please, there should be a config.ini.example you can copy and rename")