import discord
import os
import psutil
import json

TOKEN = 'NTUwODU1MTUxODkyNjkyOTky.D1ovfA._13Nmqjkh01I_Q9b8I_wPX9mtBA'
client = discord.Client()
directory = "D:\servers\sapphire\isle"
playersDir = 'D:\servers\sapphire\isle\TheIsle\Saved\Databases\Survival\Players\\'

def killServer():
    os.system('taskkill /F /FI "WindowTitle eq Administrator:  qHost Isle Server" /T')

def startServer():
    os.system('start cmd /c ' + directory + '\start.bat')

def updateServer():
    os.system(directory + '\\update.bat')

def getRam():
    islePID = 0
    memoryUse = 0
    process = filter(lambda p: p.name() == "TheIsleServer-Win64-Shipping.exe", psutil.process_iter())
    for i in process:
        islePID = psutil.Process(i.pid)
    if islePID != 0:
        memoryUse = islePID.memory_info()[0]/2.**30
    return memoryUse

def getCpu():
    islePID = 0
    cpuUse = 0
    process = filter(lambda p: p.name() == "TheIsleServer-Win64-Shipping.exe", psutil.process_iter())
    for i in process:
        islePID = psutil.Process(i.pid)
    if islePID != 0:
        cpuUse = islePID.cpu_percent(interval=1) / psutil.cpu_count()
        cpuUse = round(cpuUse)
    return cpuUse

def getOnline():
    islePID = 0
    process = filter(lambda p: p.name() == "TheIsleServer-Win64-Shipping.exe", psutil.process_iter())
    for i in process:
        islePID = psutil.Process(i.pid)
    if islePID == 0:
        return False
    else:
        return True

def getPlayer(steamID):
    if os.path.isfile(playersDir + steamID + ".json"):
        with open(playersDir + steamID + ".json") as f:
            data = json.load(f)
        return(data)
        f.close()
    else:
        return False

def changePlayer(steamID, key, value):
    player = getPlayer(steamID)
    if os.path.isfile(playersDir + steamID + ".json"):
        player[key] = value
        with open(playersDir + steamID + ".json", 'w') as f:
            json.dump(player, f)
        f.close()
        return True
    else:
        return False


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!channel'):
        msg = str(message.channel)
        msg = msg + ' {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if str(message.channel) == 'sapphire-isle' or str(message.channel) == 'main-server-box':
        if message.content.startswith('!help') or message.content.startswith('!commands'):
            msg = 'Commands:'
            msg = msg + '```!start | Starts the server\n'
            msg = msg + '!stop | Stops the server\n'
            msg = msg + '!update | Updates the server\n'
            msg = msg + '!restart | Restarts the server\n'
            msg = msg + '!status | Gives RAM Usage and Server Online Status'
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
        elif message.content.startswith('!status'):
            ram = round(getRam())
            cpu = getCpu()
            cpu = str(cpu)
            ram = str(ram)
            online = getOnline()
            if online:
                msg = '{0.author.mention} | RAM Usage: ' + ram + ' GB | CPU Usage: ' + cpu + '% | Server is ONLINE'
            else:
                msg = '{0.author.mention} | RAM Usage: 0 GB | 0% CPU | Server is OFFLINE'
            
            msg = msg.format(message)
            await client.send_message(message.channel, msg)
        elif message.content.startswith('!getplayer'):
            command = message.content
            command = command.split()
            player = getPlayer(command[1])
            if player:
                msg = command[1]
                msg = msg + '```'
                for key, value in player.items():
                    msg = msg + str(key) + ' : ' + str(value) + '\n'
                msg = msg + '```'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
            else:
                msg = 'Player file does not exist at ' + command[1]
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
        elif message.content.startswith('!beta'):
            command = message.content
            command = command.split()
            print(changePlayer(command[1], command[2], command[3]))

    elif str(message.channel) == 'admin':
        pass

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)