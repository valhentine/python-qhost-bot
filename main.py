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

def getPlayers():
    with open('points.json') as json_file:
        players = json.load(json_file)
        return players

def savePlayers(players):
    with open('points.json', 'w') as json_file:  
        json.dump(players, json_file)

def checkSteamID(steamID, players):
    for ply in players:
        if steamID == ply['steamID']:
            return ply
    return False

def checkDiscordID(discordID, players):
    for ply in players:
        if discordID == ply['discordID']:
            return ply
    return False

players = getPlayers()


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


    elif str(message.channel) == 'sapphire-isle-pointshop' or str(message.channel) == 'pointshop-admin':
        command = message.content
        command = command.split()
        players = getPlayers()
        if message.content.startswith('!points'):
            if len(command) == 1:
                plyID = message.author.id
            elif len(command) == 2:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
            found = 0
            for ply in players:
                    if ply['discordID'] == plyID:
                        msg = '<@' + plyID + '>'
                        msg = msg + ', you have **' + ply['points'] + '** fossils.'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                        found = 1
            if not found:
                msg = '<@' + plyID + '>'
                msg = msg + ', you do not have a pointshop account.'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
        elif message.content.startswith('!register'):
            if not len(command) == 2:
                msg = 'Please use !register **SteamID64**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
            else:
                plyID = message.author.id
                steamID = command[1]
                found = False
                for ply in players:
                    if steamID == ply['steamID']:
                        found = True
                        msg = 'SteamID already registered to <@' + ply['discordID'] + '>.' 
                        await client.send_message(message.channel, msg)
                if not found:
                    for ply in players:
                        if plyID == ply['discordID']:
                            found = True
                            msg = '<@' + ply['discordID'] + '>, you already have an account with the SteamID **' + ply['steamID'] + '**.' 
                            await client.send_message(message.channel, msg)
                    if not found:
                        newPlayer = {
                            'discordID': plyID,
                            'steamID': steamID,
                            'points': '0'
                        }
                        players.insert(0, newPlayer)
                        savePlayers(players)
                        msg = '<@' + plyID + '>, You have successfully registered as SteamID 64 **' + steamID + '**.'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
        elif message.content.startswith('!lookup'):
            if not len(command) == 2:
                msg = 'Please use !lookup **@discordName** OR !lookup **SteamID**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
            else:
                if command[1][0] == '<':
                    plyID = str(command[1])
                    plyID = plyID[1:]
                    plyID = plyID[1:]
                    plyID = plyID[:-1]
                    
                    found = False
                    for ply in players:
                        if plyID == ply['discordID']:
                            found = True
                            msg = plyID = str(command[1]) + ' has the SteamID **' + ply['steamID'] + '** and has **' + ply['points'] + '** fossils.'
                            msg = msg.format(message)
                            await client.send_message(message.channel, msg)
                    if not found:
                        msg = str(command[1]) + ' Does not have a pointshop account.'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                else:
                    steamID = str(command[1])
                    found = False
                    for ply in players:
                        if steamID == ply['steamID']:
                            found = True
                            msg = '<@' + ply['discordID'] + '> has the SteamID **' + ply['steamID'] + '** and has **' + ply['points'] + '** fossils.'
                            msg = msg.format(message)
                            await client.send_message(message.channel, msg)
                    if not found:
                        msg = str(command[1]) + ' Does not have a pointshop account.'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
        elif message.content.startswith('!assign'):
            if not len(command) == 3:
                msg = 'Please use !assign **@discordName SteamID64**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
            else:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
                steamID = str(command[2])

                found = checkSteamID(steamID, players)
                if found:
                    msg = 'SteamID already assigned to <@' + found['discordID'] + '>.'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    found = False
                    for ply in players:
                        if plyID == ply['discordID']:
                            found = True
                            ply['steamID'] = steamID
                            savePlayers(players)
                            msg = plyID = str(command[1]) + ' now has the SteamID **' + ply['steamID'] + '**.'
                            msg = msg.format(message)
                            await client.send_message(message.channel, msg)
                    if not found:
                        msg = plyID = str(command[1]) + ' does not have a pointshop account'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
        elif message.content.startswith('!setpoints'):
            if len(command) == 3:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
                found = checkDiscordID(plyID, players)
                if found:
                    found['points'] = command[2]
                    savePlayers(players)
                    msg = plyID = str(command[1]) + ' now has **' + found['points'] + '** fossils.'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    msg = plyID = str(command[1]) + ' does not have a pointshop account'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
            else:
                msg = 'Please use !setpoints **@discordName fossils**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
        elif message.content.startswith('!addpoints'):
            if len(command) == 3:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
                found = checkDiscordID(plyID, players)
                if found:
                    found['points'] = str(int(found['points']) + int(command[2]))
                    savePlayers(players)
                    msg = plyID = str(command[1]) + ' now has **' + found['points'] + '** fossils.'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    msg = plyID = str(command[1]) + ' does not have a pointshop account'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
            else:
                msg = 'Please use !addpoints **@discordName fossils**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
        elif message.content.startswith('!removepoints') or message.content.startswith('!yoinkpoints'):
            if len(command) == 3:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
                found = checkDiscordID(plyID, players)
                if found:
                    if int(found['points']) - int(command[2]) > 0:
                        found['points'] = str(int(found['points']) - int(command[2]))
                        savePlayers(players)
                        msg = plyID = str(command[1]) + ' now has **' + found['points'] + '** fossils.'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                    else:
                        msg = str(command[1]) + ' does not have enough fossils for that transaction.'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                else:
                    msg = plyID = str(command[1]) + ' does not have a pointshop account'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
            else:
                msg = 'Please use !removepoints **@discordName fossils**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
    elif str(message.channel) == 'sapphire-isle-pointshop-user' or str(message.channel) == 'pointshop':   
        print(message.content)
        command = message.content
        command = command.split()
        players = getPlayers()
        if message.content.startswith('!points'):
            if len(command) == 1:
                plyID = message.author.id
            elif len(command) == 2:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
            found = 0
            for ply in players:
                    if ply['discordID'] == plyID:
                        msg = '<@' + plyID + '>'
                        msg = msg + ', you have **' + ply['points'] + '** fossils.'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                        found = 1
            if not found:
                msg = '<@' + plyID + '>'
                msg = msg + ', you do not have a pointshop account.'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
        elif message.content.startswith('!register'):
            if not len(command) == 2:
                msg = 'Please use !register **SteamID64**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
            else:
                plyID = message.author.id
                steamID = command[1]
                found = False
                for ply in players:
                    if steamID == ply['steamID']:
                        found = True
                        msg = 'SteamID already registered to <@' + ply['discordID'] + '>.' 
                        await client.send_message(message.channel, msg)
                if not found:
                    for ply in players:
                        if plyID == ply['discordID']:
                            found = True
                            msg = '<@' + ply['discordID'] + '>, you already have an account with the SteamID **' + ply['steamID'] + '**.' 
                            await client.send_message(message.channel, msg)
                    if not found:
                        newPlayer = {
                            'discordID': plyID,
                            'steamID': steamID,
                            'points': '250'
                        }
                        players.insert(0, newPlayer)
                        savePlayers(players)
                        msg = '<@' + plyID + '>, You have successfully registered as SteamID 64 **' + steamID + '**.'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
        elif message.content.startswith('!transfer'):
            if not len(command) == 3:
                msg = 'Please use !transfer **@username fossils**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
            else:
                if not checkDiscordID(message.author.id, players):
                    msg = '<@' + plyID + '>'
                    msg = msg + ', you do not have a pointshop account.'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    plyID = str(command[1])
                    plyID = plyID[1:]
                    plyID = plyID[1:]
                    plyID = plyID[:-1]
                    ply = checkDiscordID(plyID, players)
                    if not ply:
                        msg = plyID = str(command[1]) + ' does not have a pointshop account'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                    else:
                        initPly = checkDiscordID(message.author.id, players)
                        if int(initPly['points']) - int(command[2]) < 0:
                            msg = '<@' + message.author.id + '>' + ', you do not have enough fossils for this transaction.'
                            msg = msg.format(message)
                            await client.send_message(message.channel, msg)
                        else:
                            initPly['points'] = str(int(initPly['points']) - int(command[2]))
                            ply['points'] = str(int(ply['points']) + int(command[2]))
                            savePlayers(players)
                            msg = '<@' + message.author.id + '>' + ', you have transfered **' + command[2] + '** fossils to <@' + ply['discordID'] + '>'
                            msg = msg.format(message)
                            await client.send_message(message.channel, msg)
    elif str(message.channel) == 'test-qbot' or str(message.channel) == 'role-registration':
        command = message.content
        command = command.split()
        players = getPlayers()
        if message.content.startswith('!register'):
            if not len(command) == 2:
                msg = 'Please use !register **SteamID64**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
            else:
                plyID = message.author.id
                steamID = command[1]
                found = False
                for ply in players:
                    if steamID == ply['steamID']:
                        found = True
                        msg = 'SteamID already registered to <@' + ply['discordID'] + '>.' 
                        await client.send_message(message.channel, msg)
                if not found:
                    for ply in players:
                        if plyID == ply['discordID']:
                            found = True
                            msg = '<@' + ply['discordID'] + '>, you already have an account with the SteamID **' + ply['steamID'] + '**.' 
                            await client.send_message(message.channel, msg)
                    if not found:
                        newPlayer = {
                            'discordID': plyID,
                            'steamID': steamID,
                            'points': '250'
                        }
                        players.insert(0, newPlayer)
                        savePlayers(players)
                        role = discord.utils.get(message.server.roles, name='Members')
                        await client.add_roles(message.author, role)
                        msg = '<@' + plyID + '>, You have successfully registered as SteamID 64 **' + steamID + '**.'
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