import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

import random
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intent = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intent, help_command=None)

@bot.event
async def on_ready():
    print("Loading cogs...")
    print("Loading MusicCog...")
    await bot.load_extension("MusicCog")
    print("Loading BattleshipCog...")
    await bot.load_extension("BattleshipCog")
    print("Loading PollCog...")
    await bot.load_extension("PollCog")
    print("Cogs loaded!")

@bot.command()
async def ping(ctx):
    await ctx.channel.send("Pong!")

@bot.command()
async def coinflip(ctx):
    num = random.randint(1,2)
    if (num == 1):
        await ctx.channel.send("Heads!")
    else:
        await ctx.channel.send("Tails!")

@bot.command()
async def rps(ctx, hand):
    hands = ["✌️","✋","✊"]
    botHand = random.choice(hands)

    if hand == botHand:
        await ctx.send(f"It's a Draw! {botHand}")
    elif hand == "✌️":
        if botHand == "✊":
            await ctx.send("I won! ✊")
        elif botHand == "✋":
            await ctx.send("You won! ✋")
    elif hand == "✋":
        if botHand == "✌️":
            await ctx.send("I won! ✌️")
        elif botHand == "✊":
            await ctx.send("You won! ✊")
    elif hand == "✊":
        if botHand == "✋":
            await ctx.send("I won! ✋")
        elif botHand == "✌️":
            await ctx.send("You won! ✌️")

@bot.command(aliases = ["about"])
async def help(ctx):
    MyEmbed = discord.Embed(title = "Commands", description = "These are the commands that you can use for this bot", colour = discord.Colour.teal())
    MyEmbed.set_thumbnail(url = "https://www.google.com/imgres?imgurl=https%3A%2F%2Ffiles.worldwildlife.org%2Fwwfcmsprod%2Fimages%2FHERO_harbor_seal_on_ice%2Fhero_small%2F41yzw17euy_Harbor_Seal_on_Ice_close_0357_6_11_07.jpg&tbnid=zU5kM0OLYAGL9M&vet=12ahUKEwjo99iO_q-CAxVLKt4AHVZuB_MQMygBegQIARB3..i&imgrefurl=https%3A%2F%2Fwww.worldwildlife.org%2Fspecies%2Fseals&docid=iYLGyoGxatOlKM&w=640&h=480&q=seal&ved=2ahUKEwjo99iO_q-CAxVLKt4AHVZuB_MQMygBegQIARB3")
    MyEmbed.add_field(name = "!ping", value = "This command replies with Pong! when you write !ping", inline = False)
    MyEmbed.add_field(name = "!coinflip", value = "This command lets you flip a coin", inline = False)
    MyEmbed.add_field(name = "!rps", value = "This command lets you play a game of Rock Paper Scissors with the bot", inline = False)
    MyEmbed.add_field(name = "!edit", value = "This command is the prefix for editing the server. You can edit servername, region, createtextchannel, createvoicechannel, and createrole", inline = False)
    MyEmbed.add_field(name = "!kick", value = "This command lets you kick a member", inline = False)
    MyEmbed.add_field(name = "!ban", value = "This command lets you ban a member", inline = False)
    MyEmbed.add_field(name = "!unban", value = "This command lets you unban a member", inline = False)
    MyEmbed.add_field(name = "!purge", value = "This command lets you purge the last x messages from a channel's history, or all messages since a specific date (day, month, year) in numeric form. (i.e. 6 11 2011 for November 6, 2011)", inline = False)
    MyEmbed.add_field(name = "!mute", value = "This command lets you mute a member", inline = False)
    MyEmbed.add_field(name = "!unmute", value = "This command lets you unmute a member", inline = False)
    MyEmbed.add_field(name = "!deafen", value = "This command lets you deafen a member", inline = False)
    MyEmbed.add_field(name = "!undeafen", value = "This command lets you undeafen a member", inline = False)
    MyEmbed.add_field(name = "!voicekick", value = "This command lets you kick a member from a voice channel", inline = False)
    MyEmbed.add_field(name = "!musichelp", value = "This command displays the help menu for the Music Bot", inline = False)
    MyEmbed.add_field(name = "!battleshiphelp", value = "This command displays the help menu for the Battleship Bot", inline = False)
    MyEmbed.add_field(name = "!pollhelp", value = "This command displays the help menu for the Poll Bot", inline = False)
    await ctx.send(embed = MyEmbed)

@bot.group()
@commands.has_role("Admin")
async def edit(ctx):
    pass

@edit.command()
async def servername(ctx, *,input):
    await ctx.guild.edit(name = input)
    await ctx.channel.send(f"Server name changed to '{input}'")

@edit.command()
async def createtextchannel(ctx, *,input):
    await ctx.guild.create_text_channel(name = input)
    await ctx.channel.send(f"Text channel '{input}' has been created!")

@edit.command()
async def createvoicechannel(ctx, *,input):
    await ctx.guild.create_voice_channel(name = input)
    await ctx.channel.send(f"Voice channel '{input}' has been created!")

@edit.command()
async def createrole(ctx, *,input):
    await ctx.guild.create_role(name = input)
    await ctx.channel.send(f"Role '{input}' has been created!")

@bot.command()
@commands.has_role("Admin")
async def kick(ctx, member : discord.Member, *,reason = None):
    await ctx.guild.kick(member, reason = reason)
    await ctx.channel.send(f"{member.user.name} has been kicked!")

@kick.error
async def errorHelper(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.channel.send("You don't have the necessary role to perform this action!")

@bot.command()
@commands.has_role("Admin")
async def ban(ctx, member : discord.Member, *,reason = None):
    await ctx.guild.ban(member, reason = reason)
    await ctx.channel.send(f"{member.user.name} has been banned!")

@ban.error
async def errorHelper(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.channel.send("You don't have the necessary role to perform this action!")

@bot.command()
@commands.has_role("Admin")
async def unban(ctx, *,input):
    async for entry in ctx.guild.bans(limit=150):
        username = entry.user.name
        if input == username:
            await ctx.guild.unban(entry.user)
    await ctx.channel.send(f"{username} has been unbanned!")

@unban.error
async def errorHelper(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.channel.send("You don't have the necessary role to perform this action!")

@bot.command()
@commands.has_role("Admin")
async def purge(ctx, amount, day : int = None, month : int = None, year = datetime.now().year):
    if amount == "-":
        if day == None or month == None:
            return
        else:
            await ctx.channel.purge(after = datetime(year, month, day))
    else:
        await ctx.channel.purge(limit = int(amount) +1)
    await ctx.channel.send("Purge complete!")

@purge.error
async def errorHandler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("Command is missing required arguments. (!purge [amount] OR !purge - [day] [month] [year])")
    if isinstance(error, commands.CommandInvokeError):
        await ctx.channel.send("Arguments must be an integer")

@bot.command()
@commands.has_role("Admin")
async def mute(ctx, user : discord.Member):
    await user.edit(mute = True)

@mute.error
async def errorHelper(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.channel.send("You don't have the necessary role to perform this action!")

@bot.command()
@commands.has_role("Admin")
async def unmute(ctx, user : discord.Member):
    await user.edit(mute = False)

@unmute.error
async def errorHelper(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.channel.send("You don't have the necessary role to perform this action!")

@bot.command()
@commands.has_role("Admin")
async def deafen(ctx, user : discord.Member):
    await user.edit(deafen = True)

@deafen.error
async def errorHelper(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.channel.send("You don't have the necessary role to perform this action!")

@bot.command()
@commands.has_role("Admin")
async def undeafen(ctx, user : discord.Member):
    await user.edit(deafen = False)

@undeafen.error
async def errorHelper(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.channel.send("You don't have the necessary role to perform this action!")

@bot.command()
@commands.has_role("Admin")
async def voicekick(ctx, user : discord.Member):
    await user.edit(voice_channel = None)

@voicekick.error
async def errorHelper(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.channel.send("You don't have the necessary role to perform this action!")

@bot.command()
async def load(ctx, *,name):
    await bot.load_extension(name)

@bot.command()
async def unload(ctx, *,name):
    await bot.unload_extension(name)

@bot.command()
async def reload(ctx, *,name):
    await bot.reload_extension(name)

bot.run(TOKEN)