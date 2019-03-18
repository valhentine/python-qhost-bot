import discord
import os
import psutil
import json
import urllib.request

TOKEN = 'NTUwODU1MTUxODkyNjkyOTky.D1ovfA._13Nmqjkh01I_Q9b8I_wPX9mtBA'
client = discord.Client()
directory = "D:\servers\sapphire\isle"
playersDir = 'D:\servers\sapphire\isle\TheIsle\Saved\Databases\Survival\Players\\'
dinosDir = 'D:\qhost-bot\dinos\\'

def killServer():
    os.system('taskkill /F /FI "WindowTitle eq Administrator:  qHost Isle Server" /T')

def startServer():
    killServer()
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

def verifyExists(steamID):
    if not os.path.isfile(playersDir + steamID + ".json"):
        with open(dinosDir + 'default.json') as f:
            default = json.load(f)
        f.close()
        with open(playersDir + steamID + ".json", 'w') as f:
            json.dump(default, f)
        f.close()

def loadDino(dino, steamID):
    verifyExists(steamID)
    if not os.path.isfile(dinosDir + dino + '.json'):
        return False
    else:
        with open(dinosDir + dino + '.json') as f:
            dinoFile = json.load(f)
        f.close()
        with open(playersDir + steamID + ".json", 'w') as f:
            json.dump(dinoFile, f)
        f.close()
        return True

def saveDino(dino, steamID):
    verifyExists(steamID)
    with open(playersDir + steamID + ".json") as f:
        dinoFile = json.load(f)
    f.close()
    with open(dinosDir + dino + '.json', 'w') as f:
        json.dump(dinoFile, f)
    f.close()
    return True


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
            verifyExists(steamID)
            return ply
    return False

def checkDiscordID(discordID, players):
    for ply in players:
        if discordID == ply['discordID']:
            verifyExists(ply['steamID'])
            return ply
    return False

def hasPoints(discordID, points):
    players = getPlayers()
    ply = checkDiscordID(discordID, players)
    points = int(points)
    plyPoints = int(ply['points'])
    if plyPoints - points < 1:
        return False
    else:
        return True

def subtractPoints(discordID, points):
    players = getPlayers()
    ply = checkDiscordID(discordID, players)
    if ply['points'] == 'admin':
        return True
    if hasPoints(discordID, points):
        players = getPlayers()
        ply = checkDiscordID(discordID, players)
        points = int(points)
        plyPoints = int(ply['points'])
        plyPoints = plyPoints - points
        plyPoints = str(plyPoints)
        ply['points'] = plyPoints
        savePlayers(players)
        return True
    else:
        return False

def checkDinoName(name):
    for dino, dinoName in dinoNameDict.items():
        if name == dino:
            return dinoName
    return False

def checkDinoPrice(name):
    for dinoName, dinoPrice in dinoPriceDict.items():
        if name == dinoName:
            return dinoPrice
    return False

def loadWarnings():
    with open('warnings.json') as f:
        return json.load(f)


def saveWarnings(warnings):
    warningsFile = open('warnings.json', 'w')
    warningsJSON = json.dumps(warnings)
    warningsJSON = json.loads(warningsJSON)
    warningsFile.write(json.dumps(warningsJSON, indent=4, sort_keys=True))
    warningsFile.close()

def getWarnings(discordID):
    warnings = loadWarnings()
    if discordID in warnings:
        return warnings[discordID]
    else:
        return False

def addWarning(discordID, warning):
    warnings = loadWarnings()
    if getWarnings(discordID):
        warns = warnings[discordID]
        warns.append(warning)
        warnings[discordID] = warns
        saveWarnings(warnings)
    else:
        warns = []
        warns.append(warning)
        warnings[discordID] = warns
        saveWarnings(warnings)

dinoNameDict = {
    'spino': 'Spino',
    'rex': 'RexAdultS',
    'giga': 'GigaAdultS',
    'acro': 'Acro',
    'alberto': 'Albert',
    'allo': 'AlloAdultS',
    'carno': 'CarnoAdultS',
    'sucho': 'SuchoAdultS',
    'bary': 'Bary',
    'cerato': 'CeratoAdultS',
    'dilo': 'DiloAdultS',
    'utah': 'UtahAdultS',
    'austro': 'Austro',
    'herrera': 'Herrera',
    'shant': 'Shant',
    'cama': 'Camara',
    'trike': 'TrikeAdultS',
    'para': 'ParaAdultS',
    'maia': 'MaiaAdultS',
    'dryo': 'Dryo',
    'anky': 'Anky',
    'pachy': 'Pachy',
    'stego': 'Stego',
    'ava': 'Ava',
    'theri': 'Theri',
    'pue': 'Puerta',
    'diablo': 'DiabloAdultS'
}

dinoPriceDict = {
    'Spino': '250',
    'RexAdultS': '300',
    'GigaAdultS': '300',
    'Acro': '30',
    'Albert': '24',
    'AlloAdultS': '18',
    'CarnoAdultS': '16',
    'SuchoAdultS': '22',
    'Bary': '14',
    'CeratoAdultS': '20',
    'DiloAdultS': '14',
    'UtahAdultS': '26',
    'Austro': '6',
    'Herrera': '6',
    'Shant': '60',
    'Camara': '180',
    'TrikeAdultS': '36',
    'ParaAdultS': '22',
    'MaiaAdultS': '14',
    'Dryo': '4',
    'Anky': '22',
    'Pachy': '10',
    'Stego': '22',
    'Ava': '8',
    'Theri': '26',
    'Puerta': '250',
    'DiabloAdultS': '18'
}

players = getPlayers()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!channel'):
        msg = str(message.channel)
        msg = msg + ' {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if str(message.channel) == 'sapphire-isle' or str(message.channel) == 'server-control': #main-server-box
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
        elif message.content.startswith('!stats'):
            pDir = 'D:\servers\sapphire\isle\TheIsle\Saved\Databases\Survival\Players'
            onlyfiles = next(os.walk(pDir))[2]
            joinedCount = str(len(onlyfiles))
            players = getPlayers()
            plyCount = 0
            for ply in players:
                plyCount = plyCount + 1
            registerRate = str(round(plyCount / int(joinedCount) * 100))
            msg = 'Registered Discord Users: **' + str(plyCount) + '**\nUnique Players To Join Server: **' + joinedCount + '**\n'
            msg = msg + 'That is a register rate of **' + registerRate + '**%'
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
        elif message.content.startswith('!wipe'):
            msg = '{0.author.mention} | Initating Wipe...'
            msg = msg.format(message)
            await client.send_message(message.channel, msg)
            os.system('ftp -i -s:new.ftp')
            msg = '{0.author.mention} | Wiped all player files from Queens Isle '
            msg = msg.format(message)
            await client.send_message(message.channel, msg)


    elif str(message.channel) == 'admin-commands' or str(message.channel) == 'server-administration': #server-administration
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
                if plyID[0] == '!':
                    plyID = plyID[1:]
            found = 0
            players = getPlayers()
            found = checkDiscordID(plyID, players)
            if found:
                msg = '<@' + plyID + '>'
                msg = msg + ', you have **' + found['points'] + '** <:fossil:556472990460805138>'
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
        elif message.content.startswith('!gender') or message.content.startswith('!transition'):
            if not len(command) == 3:
                msg = 'Please use !gender **@discordName male/female**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
            else:
                gender = False
                if command[2].lower() == 'male' or command[2].lower() == 'm':
                    gender = 'False'
                elif command[2].lower() == 'female' or command[2].lower() == 'f':
                    gender = 'True'
                else:
                    msg = 'Please use !gender **@discordName male/female**'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                if gender:
                    plyID = str(command[1])
                    plyID = plyID[1:]
                    plyID = plyID[1:]
                    plyID = plyID[:-1]
                    if plyID[0] == '!':
                        plyID = plyID[1:]
                    ply = checkDiscordID(plyID, players)
                    steamID = ply['steamID']
                    if changePlayer(steamID, "bGender", gender):
                        msg = str(command[1]) + ' Gender set to ' + gender
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)


        elif message.content.startswith('!grow'):
            growth = False
            if len(command) == 2:
                growth = '1.0'
            elif len(command) == 3:
                growth = str(command[2])
            else:
                msg = 'Please use !grow **@discordName** **growthLevel**(optional)'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
            if growth:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
                if plyID[0] == '!':
                        plyID = plyID[1:]

                ply = checkDiscordID(plyID, players)
                if not ply:
                    msg = str(command[1]) + ' Does not have a pointshop account.'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    steamID = ply['steamID']
                    if changePlayer(steamID, "Growth", growth):
                        changePlayer(steamID, "Hunger", "99999")
                        changePlayer(steamID, "Thirst", "99999")
                        changePlayer(steamID, "Stamina", "99999")
                        changePlayer(steamID, "Health", "99999")
                        changePlayer(steamID, "UnlockedCharacters", "")
                        msg = str(command[1]) + ' Growth set to ' + growth
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
        elif message.content.startswith('!skin'):
            if not len(command) == 9:
                msg = 'Please use !skin **@discordName** **1 2 3 4 5 6 7**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
            else:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
                if plyID[0] == '!':
                        plyID = plyID[1:]

                ply = checkDiscordID(plyID, players)
                if not ply:
                    msg = str(command[1]) + ' Does not have a pointshop account.'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    steamID = ply['steamID']
                    if changePlayer(steamID, "SkinPaletteSection1", command[2]):
                        if changePlayer(steamID, "SkinPaletteSection2", command[3]):
                            if changePlayer(steamID, "SkinPaletteSection3", command[4]):
                                if changePlayer(steamID, "SkinPaletteSection4", command[5]):
                                    if changePlayer(steamID, "SkinPaletteSection6", command[7]):
                                        if changePlayer(steamID, "SkinPaletteVariation", command[8]):
                                            msg = str(command[1]) + ' Skin edited.'
                                            msg = msg.format(message)
                                            await client.send_message(message.channel, msg)
        elif message.content.startswith('!warn'):
            if len(command) < 3:
                msg = 'Please use !warn **@discordName** **warning**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
                return
            plyID = str(command[1])
            plyID = plyID[1:]
            plyID = plyID[1:]
            plyID = plyID[:-1]
            if plyID[0] == '!':
                        plyID = plyID[1:]

            players = getPlayers()

            if not checkDiscordID(plyID, players):
                msg = 'Could not find player ' + command[1]
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
                return
            
            warning = ''

            for i in range(2, len(command)):
                warning = warning + command[i] + ' '
            
            addWarning(plyID, warning)
            msg = 'Warned ' + command[1] + ' for ' + warning
            msg = msg.format(message)
            await client.send_message(message.channel, msg)

        elif message.content.startswith('!dino'):
            if not len(command) == 3:
                msg = 'Please use !dino **@discordName** **DinoName**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
            else:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
                if plyID[0] == '!':
                        plyID = plyID[1:]

                ply = checkDiscordID(plyID, players)
                if not ply:
                    msg = str(command[1]) + ' Does not have a pointshop account.'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    steamID = ply['steamID']
                    dino = str(command[2])
                    if changePlayer(steamID, "CharacterClass", dino):
                        if changePlayer(steamID, "UnlockedCharacters", ""):
                            msg = str(command[1]) + ' Dino set to ' + dino
                            msg = msg.format(message)
                            await client.send_message(message.channel, msg)
        elif message.content.startswith('!lookup') or message.content.startswith('!getplayer'):
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
                    if plyID[0] == '!':
                        plyID = plyID[1:]

                    warnings = getWarnings(plyID)
                    warnString = 'None'
                    if warnings:
                        warnString = '```'
                        for warning in warnings:
                            warnString = warnString + warning + '\n'
                        warnString = warnString + '```'

                    found = False
                    for ply in players:
                        if plyID == ply['discordID']:
                            verifyExists(ply['steamID'])
                            found = True
                            player = getPlayer(ply['steamID'])
                            msg = plyID = str(command[1]) + ' has the SteamID **' + ply['steamID'] + '** and has **' + ply['points'] + '** <:fossil:556472990460805138>\n profile: 	http://steamcommunity.com/profiles/' + ply['steamID'] + '\n' 
                            msg = msg + 'Warnings: ' + warnString
                            msg = msg + '```'
                            for key, value in player.items():
                                msg = msg + str(key) + ' : ' + str(value) + '\n'
                            msg = msg + '```'
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
                            player = getPlayer(ply['steamID'])

                            warnings = getWarnings(ply['discordID'])
                            warnString = 'None'
                            if warnings:
                                warnString = '```'
                                for warning in warnings:
                                    warnString = warnString + warning + '\n'
                                warnString = warnString + '```'

                            msg = '<@' + ply['discordID'] + '> has the SteamID **' + ply['steamID'] + '** and has **' + ply['points'] + '** <:fossil:556472990460805138>\n profile: http://steamcommunity.com/profiles/' + ply['steamID'] + '\n' 
                            msg = msg + 'Warnings: ' + warnString
                            msg = msg + '```'
                            for key, value in player.items():
                                msg = msg + str(key) + ' : ' + str(value) + '\n'
                            msg = msg + '```'
                            msg = msg.format(message)
                            await client.send_message(message.channel, msg)
                    if not found:
                        msg = str(command[1]) + ' Does not have a pointshop account.'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
        elif message.content.startswith('!save'):
            if not len(command) == 3:
                msg = 'Please use !save **@discordName** **Name_Of_Save**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
            else:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
                if plyID[0] == '!':
                        plyID = plyID[1:]

                ply = checkDiscordID(plyID, players)
                if not ply:
                    msg = str(command[1]) + ' Does not have a pointshop account.'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    steamID = ply['steamID']
                    saveDino(command[2], steamID)
                    msg = str(command[1]) + ' Saved to ' + str(command[2])
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
        elif message.content.startswith('!load'):
            if not len(command) == 3:
                msg = 'Please use !load **@discordName** **Name_Of_Save**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
            else:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
                if plyID[0] == '!':
                        plyID = plyID[1:]

                ply = checkDiscordID(plyID, players)
                if not ply:
                    msg = str(command[1]) + ' Does not have a pointshop account.'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    steamID = ply['steamID']
                    if loadDino(command[2], steamID):
                        msg = str(command[1]) + ' Loaded dino file ' + str(command[2])
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                    else:
                        msg = str(command[2]) + ' File does not exist.'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                    

        elif message.content.startswith('!edit'):
            if not len(command) == 4:
                msg = 'Please use !edit **@discordName** **Trait** **NewValue**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
            else:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
                if plyID[0] == '!':
                        plyID = plyID[1:]

                ply = checkDiscordID(plyID, players)
                if not ply:
                    msg = str(command[1]) + ' Does not have a pointshop account.'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    steamID = ply['steamID']
                    if changePlayer(steamID, command[2], command[3]):
                        msg = 'Player file <@' + ply['discordID'] + '> ' + command[2] + ' is now ' + command[3] + '.'
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
                if plyID[0] == '!':
                        plyID = plyID[1:]
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
                if plyID[0] == '!':
                        plyID = plyID[1:]
                found = checkDiscordID(plyID, players)
                if found:
                    found['points'] = command[2]
                    savePlayers(players)
                    msg = plyID = str(command[1]) + ' now has **' + found['points'] + '** <:fossil:556472990460805138>'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    msg = plyID = str(command[1]) + ' does not have a pointshop account'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
            else:
                msg = 'Please use !setpoints **@discordName amount**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
        elif message.content.startswith('!addpoints'):
            if len(command) == 3:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
                if plyID[0] == '!':
                        plyID = plyID[1:]
                found = checkDiscordID(plyID, players)
                if found:
                    found['points'] = str(int(found['points']) + int(command[2]))
                    savePlayers(players)
                    msg = plyID = str(command[1]) + ' now has **' + found['points'] + '** <:fossil:556472990460805138>'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    msg = plyID = str(command[1]) + ' does not have a pointshop account'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
            else:
                msg = 'Please use !addpoints **@discordName amount**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
        elif message.content.startswith('!removepoints') or message.content.startswith('!yoinkpoints'):
            if len(command) == 3:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
                if plyID[0] == '!':
                        plyID = plyID[1:]
                found = checkDiscordID(plyID, players)
                if found:
                    if int(found['points']) - int(command[2]) > 0:
                        found['points'] = str(int(found['points']) - int(command[2]))
                        savePlayers(players)
                        msg = plyID = str(command[1]) + ' now has **' + found['points'] + '** <:fossil:556472990460805138>'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                    else:
                        msg = str(command[1]) + ' does not have enough <:fossil:556472990460805138> for that transaction.'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                else:
                    msg = plyID = str(command[1]) + ' does not have a pointshop account'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
            else:
                msg = 'Please use !removepoints **@discordName amount**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
    elif str(message.channel) == 'sapphire-isle-pointshop-user' or str(message.channel) == 'shop-points':   #shop-points
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
                if plyID[0] == '!':
                        plyID = plyID[1:]
            found = 0
            for ply in players:
                    if ply['discordID'] == plyID:
                        msg = '<@' + plyID + '>'
                        msg = msg + ', you have **' + ply['points'] + '** <:fossil:556472990460805138>'
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
                msg = 'Please use !transfer **@username amount**'
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
                    if plyID[0] == '!':
                        plyID = plyID[1:]
                    ply = checkDiscordID(plyID, players)
                    if not ply:
                        msg = plyID = str(command[1]) + ' does not have a pointshop account'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                    else:
                        initPly = checkDiscordID(message.author.id, players)
                        if int(initPly['points']) - int(command[2]) < 0:
                            msg = '<@' + message.author.id + '>' + ', you do not have enough <:fossil:556472990460805138> for this transaction.'
                            msg = msg.format(message)
                            await client.send_message(message.channel, msg)
                        else:
                            initPly['points'] = str(int(initPly['points']) - int(command[2]))
                            ply['points'] = str(int(ply['points']) + int(command[2]))
                            savePlayers(players)
                            msg = '<@' + message.author.id + '>' + ', you have transfered **' + command[2] + '** <:fossil:556472990460805138> to <@' + ply['discordID'] + '>'
                            msg = msg.format(message)
                            await client.send_message(message.channel, msg)
    elif str(message.channel) == 'test-qbot' or str(message.channel) == 'member-registration':  #member-registration
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
                            role = discord.utils.get(message.server.roles, name='Member')
                            await client.add_roles(message.author, role)
                    if not found:
                        newPlayer = {
                            'discordID': plyID,
                            'steamID': steamID,
                            'points': '250'
                        }
                        players.insert(0, newPlayer)
                        savePlayers(players)
                        role = discord.utils.get(message.server.roles, name='Member')
                        await client.add_roles(message.author, role)
                        msg = '<@' + plyID + '>, You have successfully registered as SteamID 64 **' + steamID + '**.'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
    elif str(message.channel) == 'purchasing-chat':  #purchasing chat
        command = message.content
        command = command.split()
        players = getPlayers()
        if not checkDiscordID(message.author.id, players):
            msg = '<@' + message.author.id + '>'
            msg = msg + ', you do not have a pointshop account.'
            msg = msg.format(message)
            await client.send_message(message.channel, msg)
            return
        if message.content.startswith('!points'):
            if len(command) == 1:
                plyID = message.author.id
            elif len(command) == 2:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
                if plyID[0] == '!':
                        plyID = plyID[1:]
            found = 0
            for ply in players:
                    if ply['discordID'] == plyID:
                        msg = '<@' + plyID + '>'
                        msg = msg + ', you have **' + ply['points'] + '** <:fossil:556472990460805138>'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                        found = 1
            if not found:
                msg = '<@' + plyID + '>'
                msg = msg + ', you do not have a pointshop account.'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
        elif message.content.startswith('!purchase'):
            if len(command) == 1:
                command.append('')
            if command[1] == 'gender' or command[1] == 'genderswap':
                plyID = message.author.id
                ply = checkDiscordID(plyID, players)
                if not len(command) == 2:
                    msg = 'Please use !purchase gender'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                    return
                if subtractPoints(plyID, 10):
                    verifyExists(ply['steamID'])
                    plyFile = getPlayer(ply['steamID'])
                    gender = str(plyFile['bGender'])
                    if gender == 'False':
                        gender = 'True'
                        pGender = 'Female'
                    elif gender == 'True':
                        gender = 'False'
                        pGender = 'Male'
                    else:
                        msg = '<@' + message.author.id + '>' + ', ERROR READING PLAYER FILE @GRIFF#6889'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                    if changePlayer(ply['steamID'], 'bGender', gender):
                        players = getPlayers()
                        ply = checkDiscordID(plyID, players)
                        msg = '<@' + message.author.id + '>' + ', You have purchased a gender swap to **' + pGender + '**. You now have **' + ply['points'] + '** <:fossil:556472990460805138>'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                else:
                    msg = '<@' + message.author.id + '>' + ', you do not have enough <:fossil:556472990460805138> for this transaction'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
            else:
                plyID = message.author.id
                ply = checkDiscordID(plyID, players)
                verifyExists(ply['steamID'])
                plyFile = getPlayer(ply['steamID'])
                if not len(command) == 2:
                    msg = 'Please use !purchase dinoname'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                    return
                dino = checkDinoName(command[1].lower())
                if dino:
                    if subtractPoints(plyID, checkDinoPrice(dino)):
                        plyFile = getPlayer(ply['steamID'])
                        if changePlayer(ply['steamID'], 'CharacterClass', dino):
                            changePlayer(ply['steamID'], 'UnlockedCharacters', '')
                            changePlayer(ply['steamID'], 'Growth', '1.0')
                            changePlayer(ply['steamID'], "Hunger", "99999")
                            changePlayer(ply['steamID'], "Thirst", "99999")
                            changePlayer(ply['steamID'], "Stamina", "99999")
                            changePlayer(ply['steamID'], "Health", "99999")
                            players = getPlayers()
                            ply = checkDiscordID(plyID, players)
                            msg = '<@' + message.author.id + '>' + ', you have purchased **' + dino + '** You now have **' + ply['points'] + '** <:fossil:556472990460805138>'
                            msg = msg.format(message)
                            await client.send_message(message.channel, msg)
                            return
                    else:
                        msg = '<@' + message.author.id + '>' + ', you do not have enough <:fossil:556472990460805138> for this transaction'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                        return
                else:
                    msg = 'Invalid dino: **' + command[1] + '** please do !prices for a list of things you can purchase.'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                    return
        elif message.content.startswith('!list') or message.content.startswith('!prices'):
            msg = 'Currently available purchases:\n'
            dinos = []
            prices = []
            for key, value in dinoNameDict.items():
                dinos.append(key)
            for key, value in dinoPriceDict.items():
                prices.append(value)
            msg = msg + '\n 10   <:fossil:556472990460805138> | !purchase gender'
            for i in range(0, len(dinos)):
                extra = ''
                if int(prices[i]) < 100:
                    extra = ' '
                    if int(prices[i]) < 10:
                        extra = '  '
                msg = msg + '\n ' + prices[i] + extra + ' <:fossil:556472990460805138> | !purchase ' + dinos[i]
            msg = msg.format(message)
            await client.send_message(message.channel, msg)    
    elif str(message.channel) == 'event-points':
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
                if plyID[0] == '!':
                        plyID = plyID[1:]
            found = 0
            for ply in players:
                    if ply['discordID'] == plyID:
                        msg = '<@' + plyID + '>'
                        msg = msg + ', you have **' + ply['points'] + '** <:fossil:556472990460805138>'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                        found = 1
            if not found:
                msg = '<@' + plyID + '>'
                msg = msg + ', you do not have a pointshop account.'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
        elif message.content.startswith('!removepoints') or message.content.startswith('!yoinkpoints'):
            if len(command) == 3:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
                if plyID[0] == '!':
                        plyID = plyID[1:]
                found = checkDiscordID(plyID, players)
                if found:
                    if int(found['points']) - int(command[2]) > 0:
                        found['points'] = str(int(found['points']) - int(command[2]))
                        savePlayers(players)
                        msg = plyID = str(command[1]) + ' now has **' + found['points'] + '** <:fossil:556472990460805138>'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                    else:
                        msg = str(command[1]) + ' does not have enough <:fossil:556472990460805138> for that transaction.'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)
                else:
                    msg = plyID = str(command[1]) + ' does not have a pointshop account'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
            else:
                msg = 'Please use !removepoints **@discordName amount**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
        elif message.content.startswith('!addpoints'):
            if len(command) == 3:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
                if plyID[0] == '!':
                        plyID = plyID[1:]
                found = checkDiscordID(plyID, players)
                if found:
                    found['points'] = str(int(found['points']) + int(command[2]))
                    savePlayers(players)
                    msg = plyID = str(command[1]) + ' now has **' + found['points'] + '** <:fossil:556472990460805138>'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    msg = plyID = str(command[1]) + ' does not have a pointshop account'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
            else:
                msg = 'Please use !addpoints **@discordName amount**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
        elif message.content.startswith('!setpoints'):
            if len(command) == 3:
                plyID = str(command[1])
                plyID = plyID[1:]
                plyID = plyID[1:]
                plyID = plyID[:-1]
                if plyID[0] == '!':
                        plyID = plyID[1:]
                found = checkDiscordID(plyID, players)
                if found:
                    found['points'] = command[2]
                    savePlayers(players)
                    msg = plyID = str(command[1]) + ' now has **' + found['points'] + '** <:fossil:556472990460805138>'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    msg = plyID = str(command[1]) + ' does not have a pointshop account'
                    msg = msg.format(message)
                    await client.send_message(message.channel, msg)
            else:
                msg = 'Please use !setpoints **@discordName amount**'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
        elif message.content.startswith('!lookup') or message.content.startswith('!getplayer'):
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
                    if plyID[0] == '!':
                        plyID = plyID[1:]

                    found = False
                    for ply in players:
                        if plyID == ply['discordID']:
                            verifyExists(ply['steamID'])
                            found = True
                            player = getPlayer(ply['steamID'])
                            msg = plyID = str(command[1]) + ' has the SteamID **' + ply['steamID'] + '** and has **' + ply['points'] + '** <:fossil:556472990460805138>\n profile: 	http://steamcommunity.com/profiles/' + ply['steamID'] + '\n' 
                            msg = msg + '```'
                            for key, value in player.items():
                                msg = msg + str(key) + ' : ' + str(value) + '\n'
                            msg = msg + '```'
                            msg = msg.format(message)
                            await client.send_message(message.channel, msg)
                    if not found:
                        msg = str(command[1]) + ' Does not have a pointshop account.'
                        msg = msg.format(message)
                        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)