import discord
from discord.ext.commands import Bot
from discord.ext import commands
import sqlite3 as sqlite
import asyncio
import sys
import os
import json
import random as r 
from datetime import datetime


LICENSE = "{temp}"


async def sendEmbed(msgList, channel, COLOR, TITLE, DESC):
    channel = channel
    
    embed = discord.Embed(
        title = TITLE,
        description = DESC,
        color = COLOR
    )
    
    def messageSplit(message):
        list = message.split("|")
        return list
    
    
    for string in msgList:
        tempList = messageSplit(string)
        
        embed.add_field(name = str(tempList[0]), value = str(tempList[1]))
        
    returnME = await channel.send(embed=embed)
    
    return returnME
    
async def waitForReaction(client, neededReaction, neededUser, neededChannel):
    outcome = False
    
    while outcome != True:
        reaction, user = await client.wait_for('reaction_add')
        
        if str(neededReaction) == str(reaction):
            if str(neededUser).upper() == "NONE":
                if str(neededChannel) == str(reaction.message.channel):
                    outcome = True
            elif str(neededChannel).upper() == "NONE":
                if str(neededUser) == str(user):
                    outcome = True
            elif str(neededChannel) == str(reaction.message.channel):
                if str(neededUser) == str(user):
                    outcome = True
                
    return True
                
