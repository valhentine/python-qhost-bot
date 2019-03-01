import discord

TOKEN = 'NTUwODU1MTUxODkyNjkyOTky.D1ovfA._13Nmqjkh01I_Q9b8I_wPX9mtBA'
client = discord.Client()

class Server():
    def __init__(self, name, port, directory):
        self.commands = []
        self.roles = []
        self.port = port
        self.name = name
        self.dir = directory
        self.roles.insert(0, "Developer")
        self.roles.insert(0, "Admin")
    
    def addCommand(self, command, output):
        self.commands.insert(0, [command, output])

    def addRole(self, role):
        self.roles.insert(0, role)

    def doCommand(self, command):
        pass

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)