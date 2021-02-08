import discord


TOKEN = 'TOKEN'

file = open('admin_id.txt', 'r')
admin_id = int(file.read())
file.close()

client = discord.Client()
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_member_join(member):
    print('guild')
    guild = client.get_guild(808315723768135710)
    admin_role = guild.get_role(808327175841251348)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        admin_role: discord.PermissionOverwrite(read_messages=True),
        member : discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel(member.display_name, overwrites=overwrites)

    await member.send(f"Hey ! A new text channel has been created especially for you ! It's called : {member.display_name}")

@client.event
async def on_message(message):
    print(message.content)
    commands = ['!help', '!send_dm', '!say', '!print_very_secret_flag', '!debug']
    splited = message.content.split(' ')
    if splited[0] in commands :
        if splited[0] == '!help' :
            await message.author.send("""
            Help :
            !help : send help message to author
            !send_dm : send a dm to a user
                Usage : !send_dm [user_id] [message]
            !say : make the bot say wathever you want in a channel
                Usage : !say [channel_id] [message]
            !print_very_secret_flag : makes the bot print a file in someone's dm
                Usage : !print_very_secret_flag file_name""")

        if splited[0] == '!send_dm' :
            if message.channel.id == admin_id :
                user = await client.fetch_user(int(splited[1]))
                await user.send("".join((word + " ") for word in splited[2:]))
            else :
                if int(splited[1]) == message.author.id :
                    await message.author.send("".join((word + " ") for word in splited[2:]))
                else :
                    await message.author.send('Sorry, you can\'t send a DM to someone else then you')

        if splited[0] == '!say' :
            if not "admin" in [y.name.lower() for y in message.author.roles] and not "bot" in [y.name.lower() for y in message.author.roles]:
                if splited[1] ==  'admin_id' :
                    await message.author.dm_channel.send('Sorry, you don\'t have access to this channel')
                else :
                    channel = client.get_channel(int(splited[1]))
                    await channel.send("".join((word + " ") for word in splited[2:]))
            else :
                channel = client.get_channel(splited[1])
                await client.get_channel(int(splited[1])).send("".join((word + " ") for word in splited[2:]))

        if splited[0] == '!print_very_secret_flag' :
            if message.channel.id == admin_id :
                file = open('flag.txt', 'r')
                flag = file.read()
                file.close()
                user = await client.fetch_user(int(splited[1]))
                await user.send(flag)
            else :
                await message.channel.send('Sorry you don\'t have permission')

        if splited[0] == '!debug' and message.channel.id == admin_id and splited[2] != 'TOKEN':
            user = await client.fetch_user(int(splited[1]))
            await user.send(f'{splited[2]}={repr(eval(splited[2]))}')







client.run(TOKEN)
