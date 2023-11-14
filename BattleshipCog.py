from discord.ext import commands
import discord

class BattleShipCog(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
        self.playing = False
        self.player1doneplacing = False
        self.player2doneplacing = False
        self.board1 = ""
        self.board2 = ""
        self.boardtoshow1 = ""
        self.boardtoshow2 = ""
        self.turn = ""
    
    @commands.command()
    async def battleshiphelp(self,ctx):
        MyEmbed = discord.Embed(title = "Battleship Commands", description = "These are the commands that you can use for the battleship game", colour = discord.Colour.teal())
        MyEmbed.set_thumbnail(url = "https://www.google.com/imgres?imgurl=https%3A%2F%2Ffiles.worldwildlife.org%2Fwwfcmsprod%2Fimages%2FHERO_harbor_seal_on_ice%2Fhero_small%2F41yzw17euy_Harbor_Seal_on_Ice_close_0357_6_11_07.jpg&tbnid=zU5kM0OLYAGL9M&vet=12ahUKEwjo99iO_q-CAxVLKt4AHVZuB_MQMygBegQIARB3..i&imgrefurl=https%3A%2F%2Fwww.worldwildlife.org%2Fspecies%2Fseals&docid=iYLGyoGxatOlKM&w=640&h=480&q=seal&ved=2ahUKEwjo99iO_q-CAxVLKt4AHVZuB_MQMygBegQIARB3")
        MyEmbed.add_field(name = "!battleshiphelp", value = "This command displays the help menu for the Battleship Bot", inline = False)
        MyEmbed.add_field(name = "!battleship", value = "This command lets you to play a game of battleship with another member", inline = False)
        MyEmbed.add_field(name = "!place", value = "This command lets you place a ship on your board", inline = False)
        MyEmbed.add_field(name = "!shoot", value = "This command lets you shoot a coordinate on the board", inline = False)
        MyEmbed.add_field(name = "!surrender", value = "This command lets you end the game early", inline = False)
        await ctx.send(embed = MyEmbed)

    async def render(self,ctx,board):
        numbers = [":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:",":nine:",":keycap_ten:"]
        alphabets = [":regional_indicator_a:",":regional_indicator_b:",":regional_indicator_c:",":regional_indicator_d:",":regional_indicator_e:",":regional_indicator_f:",":regional_indicator_g:",":regional_indicator_h:",":regional_indicator_i:",":regional_indicator_j:"]

        stringboard = ""

        stringboard = stringboard + ":black_medium_small_square:"
        for x in range(len(board[0])):
            stringboard = stringboard + alphabets[x]
        stringboard = stringboard + "\n"

        i = 0
        for row in board:
            stringboard = stringboard + numbers[i]
            i = i + 1
            for square in row:
                stringboard = stringboard + square
            stringboard = stringboard + "\n"
        await ctx.send(stringboard)

    @commands.command()
    async def battleship(self,ctx,player2: discord.Member, ver : int = 5, hor : int = 5):
        if self.playing == False:
            if ver >= 5 and ver <= 10 and hor >= 5 and hor <= 10:
                self.playing = True
                self.player1doneplacing = False
                self.player2doneplacing = False
                self.player1 = ctx.author
                self.player2 = player2
                self.turn = self.player1
                self.board1 = [[":blue_square:"]*hor for x in range(ver)]
                self.board2 = [[":blue_square:"]*hor for x in range(ver)]
                self.boardtoshow1 = [[":blue_square:"]*hor for x in range(ver)]
                self.boardtoshow2 = [[":blue_square:"]*hor for x in range(ver)]
                await self.render(self.player1,self.board1)
                await self.render(self.player2,self.board2)
                await self.player1.send("Welcome to Battleship! Type !place to place your ships")
                await self.player2.send("Welcome to Battleship! Type !place to place your ships")
            else:
                await ctx.send("You can only make a board between 5 and 10!")
        else:
            await ctx.send("A game is currently in progress!")

    @battleship.error
    async def errorHelper(self,ctx,error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Please mention a second player.")

    def shipcount(self,board):
        count = 0
        for row in board:
            for square in row:
                if square == ":ship:":
                    count = count + 1
        return count

    @commands.command()
    async def place(self,ctx,*coordinates):
        if self.playing == True:
            if ctx.author == self.player1 and self.player1doneplacing == False:
                board = self.board1
            elif ctx.author == self.player2 and self.player2doneplacing == False:
                board = self.board2
            else:
                await ctx.send("You cannot place more ships after the placing phase has ended!")
            if len(coordinates) == 0:
                await ctx.send("Please type in the coordinates!")
            else:
                for coordinate in coordinates:
                    if self.shipcount(board) == 6:
                        await ctx.send("You are only allowed to have six ships!")
                    else:
                        if len(coordinate) == 2:
                            alphabet = coordinate[0]
                            number = coordinate[1]
                        else:
                            alphabet = coordinate[0]
                            number = coordinate[1] + coordinate[2]
                        loweralphabet = alphabet.lower()
                        x = ord(loweralphabet) - 97
                        y = int(number) - 1
                        board[y][x] = ":ship:"
                if self.shipcount(board) == 6:
                    if ctx.author == self.player1:
                        self.player1doneplacing = True
                    if ctx.author == self.player2:
                        self.player2doneplacing = True
                if self.player1doneplacing == True and self.player2doneplacing == True:
                    await self.player1.send("Placement phase is done! It's your turn!")
                    await self.player2.send(f"Placement phase is done! {self.player1} is shooting!")
                await self.render(ctx.author,board)
        else:
            await ctx.send("Please start a game by typing !battleship")

    @place.error
    async def errorHelper(self,ctx,error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("Please define the coordinate (ex: a1)")
        
    @commands.command()
    async def shoot(self,ctx,coordinate):
        if self.turn == ctx.author:
            if self.playing == True:
                if ctx.author == self.player1:
                    boardtoshoot = self.board2
                    boardtoshow = self.boardtoshow2
                    nextshooter = self.player2

                if ctx.author == self.player2:
                    boardtoshoot = self.board1
                    boardtoshow = self.boardtoshow1
                    nextshooter = self.player1

                if len(coordinate) == 2:
                    loweralphabet = coordinate[0].lower()
                    number = coordinate[1]
                else:
                    loweralphabet = coordinate[0].lower()
                    number = coordinate[1] + coordinate[2]
                
                x = ord(loweralphabet) - 97
                y = int(number) - 1
                square = boardtoshoot[y][x]

                if square == ":ship:":
                    await ctx.send("Hit! Shoot again!")
                    boardtoshoot[y][x] = ":boom:"
                    boardtoshow[y][x] = ":boom:"

                if square == ":blue_square:":
                    await ctx.send("Miss!")
                    boardtoshoot[y][x] = ":white_medium_square:"
                    boardtoshow[y][x] = ":white_medium_square:"
                    self.turn = nextshooter
                    await nextshooter.send("It's your turn!")

                if square == ":white_medium_square:" or square == ":boom:":
                    await ctx.send("You have already shot this square, try again")

                #Show their board and the board they are shooting
                await self.render(self.player1,self.board1)
                await self.render(self.player1,self.boardtoshow2)
                await self.render(self.player2,self.board2)
                await self.render(self.player2,self.boardtoshow1)

                if self.shipcount(boardtoshoot) == 0:
                    self.playing = False

                    await self.player1.send(f"{ctx.author} has won the game!")
                    await self.player2.send(f"{ctx.author} has won the game!")

                    if ctx.author == self.player1:
                        await self.render(self.player2,self.board1)

                    if ctx.author == self.player2:
                        await self.render(self.player1,self.board2)
            else:
                await ctx.send("Please start a game by typing !battleship")
        else:
            await ctx.send("It's not your turn!")

    @shoot.error
    async def errorHelper(self,ctx,error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Please define the coordinate (ex: a1)")
    
    @commands.command()
    async def surrender(self,ctx):
        self.playing = False
        await self.player1.send(f"{ctx.author} surrendered!")
        await self.player2.send(f"{ctx.author} surrendered!")

async def setup(bot):
    await bot.add_cog(BattleShipCog(bot))