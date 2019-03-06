import discord
import os
import psutil
import json
import urllib.request

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
            msg = 'Please visit the server-box-control-guide text channel'
            msg = msg + ''.format(message)
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
        elif message.content.startswith('!edit'):
            command = message.content
            command = command.split()
            if os.path.isfile(playersDir + command[1] + ".json"):
                if changePlayer(command[1], command[2], command[3]):
                    steamID = str(command[1])
                    msg = '{0.author.mention} | '
                    msg = msg + 'Player file **'
                    msg = msg + steamID
                    msg = msg + '** edited'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
            else:
                msg = 'Player file does not exist at ' + command[1]
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
        elif message.content.startswith('!grow'):
            command = message.content
            command = command.split()
            if len(command) < 3:
                growth = '1.0'
            else:
                growth = str(command[2])

            if os.path.isfile(playersDir + command[1] + ".json"):
                if changePlayer(command[1], "Growth", growth):
                    changePlayer(command[1], "Hunger", "99999")
                    changePlayer(command[1], "Thirst", "99999")
                    changePlayer(command[1], "Stamina", "99999")
                    changePlayer(command[1], "Health", "99999")
                    changePlayer(command[1], "UnlockedCharacters", "")

                    steamID = str(command[1])
                    msg = '{0.author.mention} | '
                    msg = msg + 'Player **'
                    msg = msg + steamID
                    msg = msg + '** growth set to **' + growth + '**'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
            else:
                msg = 'Player file does not exist at ' + command[1]
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
        elif message.content.startswith('!dino'):
            command = message.content
            command = command.split()
            if os.path.isfile(playersDir + command[1] + ".json"):
                dino = str(command[2])
                if changePlayer(command[1], "CharacterClass", dino):
                    if changePlayer(command[1], "UnlockedCharacters", ""):
                        steamID = str(command[1])
                        msg = '{0.author.mention} | '
                        msg = msg + 'Player **'
                        msg = msg + steamID
                        msg = msg + '** dino set to **' + dino + '**'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
            else:
                msg = 'Player file does not exist at ' + command[1]
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
        elif message.content.startswith('!download'):
            command = message.content
            command = command.split()
            msg = '{0.author.mention} | Starting download of player file ' + str(command[1])
            msg = msg.format(message)
            await client.send_message(message.channel, msg)
            urllib.request.urlretrieve('ftp://JuicyJuiceNV:JuIcEJuiCy$4567@144.48.104.226:8821/144.48.104.226_14010/TheIsle/Saved/Databases/Survival/Players/' + str(command[1]) + '.json', playersDir + str(command[1]) + '.json')
            player = getPlayer(command[1])
            if player:
                msg = '{0.author.mention} | Download finished. Now displaying '
                msg = msg + str(command[1])
                msg = msg + '```'
                for key, value in player.items():
                    msg = msg + str(key) + ' : ' + str(value) + '\n'
                msg = msg + '```'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
        elif message.content.startswith('!upload'):
            command = message.content
            command = command.split()
            msg = '{0.author.mention} | Starting upload of player file ' + str(command[1])
            msg = msg.format(message)
            await client.send_message(message.channel, msg)
            f = open("up.ftp", "w")
            f.write('open 144.48.104.226 8821\n')
            f.write('JuicyJuiceNV\n')
            f.write('JuIcEJuiCy$4567\n')
            f.write('cd /144.48.104.226_14010/TheIsle/Saved/Databases/Survival/Players\n')
            f.write('put D:\servers\sapphire\isle\TheIsle\Saved\Databases\Survival\Players\\' + str(command[1]) + '.json\n')
            f.write('disconnect\n')
            f.write('quit')
            f.close()
            os.system('ftp -i -s:up.ftp')
            msg = '{0.author.mention} | Finished uploading player file ' + str(command[1])
            msg = msg.format(message)
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

urllib.request.urlretrieve('ftp://JuicyJuiceNV:JuIcEJuiCy$4567@144.48.104.226:8821/144.48.104.226_14010/TheIsle/Saved/Databases/Survival/Players/', 'file')
urllib.request.urlretrieve('ftp://JuicyJuiceNV:JuIcEJuiCy$4567@144.48.104.226:8821/144.48.104.226_14010/TheIsle/Saved/Databases/Survival/Players/76561197963350619.json', 'file')