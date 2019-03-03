import discord
import os

TOKEN = 'NTUwODU1MTUxODkyNjkyOTky.D1ovfA._13Nmqjkh01I_Q9b8I_wPX9mtBA'
client = discord.Client()
directory = "D:\servers\sapphire\isle"

def killServer():
    os.system('taskkill /F /FI "WindowTitle eq Administrator:  qHost Isle Server" /T')

def startServer():
    os.system('start cmd /c ' + directory + '\start.bat')

def updateServer():
    os.system(directory + '\\update.bat')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!channel'):
        msg = str(message.channel)
        msg = msg + ' {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if str(message.channel) == 'sapphire-isle':
        if message.content.startswith('!help') or message.content.startswith('!commands'):
            msg = 'Commands:'
            msg = msg + '```!start | Starts the server\n'
            msg = msg + '!stop | Stops the server\n'
            msg = msg + '!update | Updates the server\n'
            msg = msg + '!restart | Restarts the server'
            msg = msg + '```'.format(message)
            await client.send_message(message.channel, msg)
        if message.content.startswith('!start'):
            killServer()
            startServer()
            msg = '{0.author.mention} | Server Started'.format(message)
            await client.send_message(message.channel, msg)
        elif message.content.startswith('!stop'):
            killServer()
            msg = '{0.author.mention} | Server Stopped'.format(message)
            await client.send_message(message.channel, msg)
        elif message.content.startswith('!update'):
            killServer()
            msg = '{0.author.mention} | Server Update Started'.format(message)
            await client.send_message(message.channel, msg)
            updateServer()
            msg = '{0.author.mention} | Server Update Finished'.format(message)
            await client.send_message(message.channel, msg)
        elif message.content.startswith('!restart'):
            killServer()
            startServer()
            msg = '{0.author.mention} | Server Restarted'.format(message)
            await client.send_message(message.channel, msg)
    elif str(message.channel) == 'admin':
        pass

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)