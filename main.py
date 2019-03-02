import discord

TOKEN = 'NTUwODU1MTUxODkyNjkyOTky.D1ovfA._13Nmqjkh01I_Q9b8I_wPX9mtBA'
client = discord.Client()

class Server():
    def __init__(self, name, port, directory):
        self.commands = []
        self.roles = []
        self.channels = []
        self.port = port
        self.name = name
        self.dir = directory
        self.roles.insert(0, "Developer")
        self.roles.insert(0, "Admin")
    
    def addCommand(self, command, output, channel):
        self.commands.insert(0, [command, output, channel])

    def addRole(self, role):
        self.roles.insert(0, role)

    def addChannel(self, channel):
        self.channels.insert(0, channel)

    def doCommand(self, command):
        pass

sapphireIsle = Server("Sapphire Isle", 27015, "D:\servers\sapphire\isle")
sapphireIsle.addRole("Server Development")
sapphireIsle.addChannel("sapphire-isle")
sapphireIsle.addCommand(["", ""], "Send server start request", "sapphire-isle")

servers = []

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
        print("Hello World")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)