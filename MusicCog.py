from discord.ext import commands
import yt_dlp as youtube_dl
import discord, asyncio, os

class MusicCog(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
        self.queuelist = []
        self.filestodelete = []

    @commands.command()
    async def musichelp(self,ctx):
        MyEmbed = discord.Embed(title = "Music Commands", description = "These are the commands that you can use for the Music Bot", colour = discord.Colour.teal())
        MyEmbed.set_thumbnail(url = "https://www.google.com/imgres?imgurl=https%3A%2F%2Ffiles.worldwildlife.org%2Fwwfcmsprod%2Fimages%2FHERO_harbor_seal_on_ice%2Fhero_small%2F41yzw17euy_Harbor_Seal_on_Ice_close_0357_6_11_07.jpg&tbnid=zU5kM0OLYAGL9M&vet=12ahUKEwjo99iO_q-CAxVLKt4AHVZuB_MQMygBegQIARB3..i&imgrefurl=https%3A%2F%2Fwww.worldwildlife.org%2Fspecies%2Fseals&docid=iYLGyoGxatOlKM&w=640&h=480&q=seal&ved=2ahUKEwjo99iO_q-CAxVLKt4AHVZuB_MQMygBegQIARB3")
        MyEmbed.add_field(name = "!musichelp", value = "This command displays the help menu for the Music Bot", inline = False)
        MyEmbed.add_field(name = "!join", value = "This command brings the bot into the voice call of the user who used this command", inline = False)
        MyEmbed.add_field(name = "!leave", value = "This command makes the bot leave the voice channel it is currently in", inline = False)
        MyEmbed.add_field(name = "!play", value = "This command either plays or queues a song depending on whether music is already playing", inline = False)
        MyEmbed.add_field(name = "!pause", value = "This command pauses the currently playing song", inline = False)
        MyEmbed.add_field(name = "!stop/!skip", value = "This command skips the currently playing song", inline = False)
        MyEmbed.add_field(name = "!resume", value = "This command resumes the currently paused song", inline = False)
        MyEmbed.add_field(name = "!viewqueue", value = "This command displays the song queue", inline = False)
        await ctx.send(embed = MyEmbed)

    @commands.command()
    async def join(self,ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @join.error
    async def errorHelper(self,ctx,error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("You have to be in a Voice Channel to use this command!")

    @commands.command()
    async def leave(self,ctx):
        await ctx.voice_client.disconnect()

    @leave.error
    async def errorHelper(self,ctx,error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("Bot is not connected to a Voice Channel!")

    @commands.command()
    async def play(self,ctx, *,searchword):
        ydl_opts = {}
        voice = ctx.voice_client

        if voice == None:
            raise commands.errors.CommandInvokeError
        
        #Get the title
        if searchword[0:4] == "http" or searchword[0:3] == "www":
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(searchword, download = False)
                title = info["title"]
                url = searchword

        if searchword[0:4] != "http" and searchword[0:3] != "www":
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{searchword}", download = False)["entries"][0]
                title = info["title"]
                url = info["webpage_url"]

        ydl_opts = {
            'format' : 'bestaudio/best',
            "outtmpl" : f"{title}",
            "postprocessors" :
            [{"key" : "FFmpegExtractAudio", "preferredcodec" : "mp3", "preferredquality" : "192"}]
        }

        def download(url):
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, download, url)
        
        def check_queue():
            try:
                if self.queuelist[0] != None:
                    voice.play(discord.FFmpegPCMAudio(f"{self.queuelist[0]}.mp3"), after = lambda e : check_queue())
                    coro = self.bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = self.queuelist[0]))
                    fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
                    fut.result()
                    self.filestodelete.append(self.queuelist[0])
                    self.queuelist.pop(0)
            except IndexError:
                for file in self.filestodelete:
                    os.remove(f"{file}.mp3")
                self.filestodelete.clear()
        
        #Playing and Queueing Audio
        if voice.is_playing() or voice.is_paused():
            self.queuelist.append(title)
            await ctx.send(f"Added to Queue: ** {title} **")
        else:
            voice.play(discord.FFmpegPCMAudio(f"{title}.mp3"), after = lambda e : check_queue())
            await ctx.send(f"Playing ** {title} ** :musical_note:")
            self.filestodelete.append(title)
            await self.bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = title))

    @play.error
    async def errorHelper(self,ctx,error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("Bot is not connected to a Voice Channel!")

    @commands.command()
    async def pause(self,ctx):
        voice = ctx.voice_client
        if voice.is_playing() == True:
            voice.pause()
        else:
            await ctx.send("Bot is not playing audio!")

    @pause.error
    async def errorHelper(self,ctx,error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("Bot is not connected to a Voice Channel!")

    @commands.command(aliases = ["skip"])
    async def stop(self,ctx):
        voice = ctx.voice_client
        if voice.is_playing() == True:
            voice.stop()
        else:
            await ctx.send("Bot is not playing audio!")

    @stop.error
    async def errorHelper(self,ctx,error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("Bot is not connected to a Voice Channel!")

    @commands.command()
    async def resume(self,ctx):
        voice = ctx.voice_client
        if voice.is_playing() == True:
            await ctx.send("Bot is playing Audio!")
        else:
            voice.resume()

    @resume.error
    async def errorHelper(self,ctx,error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("Bot is not connected to a Voice Channel!")

    @commands.command()
    async def viewqueue(self,ctx):
        if len(self.queuelist) == 0:
            await ctx.send(f"Queue is empty!")
        else:
            await ctx.send(f"Queue: ** {str(self.queuelist)} ** ")


async def setup(bot):
    await bot.add_cog(MusicCog(bot))