from discord.ext import commands,tasks
import discord

class PollCog(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
        self.numbers = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    
    @commands.command()
    async def pollhelp(self,ctx):
        MyEmbed = discord.Embed(title = "Poll Commands", description = "These are the commands that you can use for the Poll Bot", colour = discord.Colour.teal())
        MyEmbed.set_thumbnail(url = "https://www.google.com/imgres?imgurl=https%3A%2F%2Ffiles.worldwildlife.org%2Fwwfcmsprod%2Fimages%2FHERO_harbor_seal_on_ice%2Fhero_small%2F41yzw17euy_Harbor_Seal_on_Ice_close_0357_6_11_07.jpg&tbnid=zU5kM0OLYAGL9M&vet=12ahUKEwjo99iO_q-CAxVLKt4AHVZuB_MQMygBegQIARB3..i&imgrefurl=https%3A%2F%2Fwww.worldwildlife.org%2Fspecies%2Fseals&docid=iYLGyoGxatOlKM&w=640&h=480&q=seal&ved=2ahUKEwjo99iO_q-CAxVLKt4AHVZuB_MQMygBegQIARB3")
        MyEmbed.add_field(name = "!pollhelp", value = "This command displays the help menu for the Poll Bot", inline = False)
        MyEmbed.add_field(Name = "!poll", value = "This command lets you host a poll of up to ten options", inline = False)
        await ctx.send(embed = MyEmbed)

    @commands.command()
    async def poll(self,ctx,minutes : int, title, *options):
        if len(options) == 0:
            pollEmbed = discord.Embed(title = title, description = f"You have **{minutes}** minutes remaining!")
            msg = await ctx.send(embed = pollEmbed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")

        else:
            pollEmbed = discord.Embed(title = title, description = f"You have **{minutes}** minutes remaining!")
            for number,option in enumerate(options):
                pollEmbed.add_field(name = f"{self.numbers[number]}", value = f"**{option}**", inline = False)
            msg = await ctx.send(embed = pollEmbed)
            for x in range(len(pollEmbed.fields)):
                await msg.add_reaction(self.numbers[x])
        self.poll_loop.start(ctx,minutes,title,options,msg)

    @tasks.loop(minutes = 1)
    async def poll_loop(self,ctx,minutes,title,options,msg):
        count = self.poll_loop.current_loop
        remaining_time = minutes - count

        newEmbed = discord.Embed(title = title, description = f"You have **{remaining_time}** minutes remaining!")
        for number,option in enumerate(options):
            newEmbed.add_field(name = f"{self.numbers[number]}", value = f"**{option}**", inline = False)
        
        await msg.edit(embed = newEmbed)

        if remaining_time == 0:
            counts = []
            msg = discord.utils.get(self.bot.cached_messages, id = msg.id)
            reactions = msg.reactions

            for reaction in reactions:
                counts.append(reaction.count)
            max_value = max(counts)
            i = 0
            for count in counts:
                if count == max_value:
                    i = i + 1
            if i > 1:
                await ctx.send("It's a draw!")
            else:
                max_index = counts.index(max_value)

                if len(options) == 0:
                    winneremoji = reactions[max_index]
                    await ctx.send("Time's up!")
                    if winneremoji.emoji == "👍":
                        await ctx.send("Looks like people agree!")
                    if winneremoji.emoji == "👎":
                        await ctx.send("Looks like that's an unpopular opinion!")
                else:
                    winner = options[max_index]
                    winneremoji = reactions[max_index]
                    await ctx.send("Time's up!")
                    await ctx.send(f"{winneremoji.emoji} **{winner}** has won the poll!")
                
            self.poll_loop.stop()

async def setup(bot):
    await bot.add_cog(PollCog(bot))