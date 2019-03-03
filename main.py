import discord
import os

TOKEN = 'NTUwODU1MTUxODkyNjkyOTky.D1ovfA._13Nmqjkh01I_Q9b8I_wPX9mtBA'
client = discord.Client()
directory = "D:\servers\sapphire\isle"

def killServer():
    pass

def startServer():
    pass

def updateServer():
    pass

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!channel'):
        msg = str(message.channel)
        msg = msg + ' {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if str(message.channel) == 'sapphire-isle':
        if message.content.startswith('!start'):
            killServer()
            startServer()
        elif message.content.startswith('!stop'):
            killServer()
        elif message.content.startswith('!update'):
            killServer()
            updateServer()
    elif str(message.channel) == 'admin':
        pass

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)