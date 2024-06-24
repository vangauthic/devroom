import discord
import yaml
import sys
import aiosqlite
import datetime as DT
import asyncio

from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime
from checks import check_tables
from utils import checkPlayer

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

token = data["General"]["TOKEN"]
activity = data["General"]["ACTIVITY"].lower()
doing_activity = data["General"]["DOING_ACTIVITY"]
status = data["General"]["STATUS"].lower()
admin_guild_id = data["General"]["ADMIN_GUILD_ID"]

initial_extensions = [
                      'cogs.utility.welcome',
                      'cogs.utility.schedule',
                      'cogs.utility.checkstock',
                      'cogs.game.leaderboard',
                      'cogs.game.rockpaperscissor'
                      ]
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if status == "online":
    _status = getattr(discord.Status, status)
elif status == "idle":
    _status = getattr(discord.Status, status)
elif status == "dnd":
    _status = getattr(discord.Status, status)
elif status == "invisible":
    _status = getattr(discord.Status, status)
else:
    sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Status: {bcolors.ENDC}{bcolors.OKCYAN}{status}{bcolors.ENDC}
{bcolors.OKBLUE}Valid Options: {bcolors.ENDC}{bcolors.OKGREEN}{bcolors.UNDERLINE}online{bcolors.ENDC}{bcolors.OKGREEN}, {bcolors.UNDERLINE}idle{bcolors.ENDC}{bcolors.OKGREEN}, {bcolors.UNDERLINE}dnd{bcolors.ENDC}{bcolors.OKGREEN}, or {bcolors.UNDERLINE}invisible{bcolors.ENDC}
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 7
""")

if activity == "playing":
    if doing_activity == "":
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Doing Activity: {bcolors.OKBLUE}It Must Be Set!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 5
""")
    else:
        _activity = discord.Game(name=doing_activity)
elif activity == "watching":
    if doing_activity == "":
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Doing Activity: {bcolors.OKBLUE}It Must Be Set!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 5
""")
    else:
        _activity = discord.Activity(name=doing_activity, type=discord.ActivityType.watching)
elif activity == "listening":
    if doing_activity == "":
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Doing Activity: {bcolors.OKBLUE}It Must Be Set!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 5
""")
    else:
        _activity = discord.Activity(name=doing_activity, type=discord.ActivityType.listening)
elif activity == "competing":
    if doing_activity == "":
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Doing Activity: {bcolors.OKBLUE}It Must Be Set!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 5
""")
    else:
        _activity = discord.Activity(name=doing_activity, type=discord.ActivityType.competing)
else:
    sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Activity: {bcolors.ENDC}{bcolors.OKCYAN}{activity}{bcolors.ENDC}
{bcolors.OKBLUE}Valid Options: {bcolors.ENDC}{bcolors.OKGREEN}{bcolors.UNDERLINE}playing{bcolors.ENDC}{bcolors.OKGREEN}, {bcolors.UNDERLINE}watching{bcolors.ENDC}{bcolors.OKGREEN}, {bcolors.UNDERLINE}competing{bcolors.ENDC}{bcolors.OKGREEN}, or {bcolors.UNDERLINE}listening{bcolors.ENDC}
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 4
""")

intents = discord.Intents.all()
class devRoom(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix = '.',
            intents = intents,
            token = token,
            activity = _activity,
            status = _status
        )

    async def on_ready(self):
        print(f'{client.user} is connected!')

        print("Attempting to check local tables...")
        await check_tables()
        print("Checked!")

        print('Attempting to sync slash commands...')
        await self.tree.sync()
        await self.tree.sync(guild=discord.Object(id=admin_guild_id))
        print('Synced')

    async def setup_hook(self):
        for extension in initial_extensions:
            await self.load_extension(extension)
        schedule.start()

client = devRoom()

#Scheduled message for noon CST every day
@tasks.loop(seconds = 5)
async def schedule():
    await client.wait_until_ready()

    sent = False
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute('SELECT * from scheduledMessages')
    settings = await cursor.fetchone()
    message = settings[2]
    channel = settings[3]
    channel = client.get_channel(channel)
    message = message.replace("<everyone>", '@everyone')
    message = message.replace("<here>", '@here')
    time = datetime.now()

    if time.hour == 0 and time.minute == 00 and sent == False:
        await channel.send(message)
        sent = True
        await asyncio.sleep(60)
        sent = False


#Tell cooldown
@client.tree.error
async def on_app_command_error(interaction, error):
    if isinstance(error, app_commands.CommandOnCooldown):
        time  = round(error.retry_after, 2)
        await interaction.response.send_message(f"This command is on cooldown for the next {time}s.", ephemeral=True)
        return
    raise error

#Send welcome messages
@client.event
async def on_member_join(member):
    await checkPlayer(member.id)

    async with aiosqlite.connect('database.db') as db:
        cursor = await db.execute('SELECT * FROM welcomeMessages WHERE serverID=?', (member.guild.id,))
        server = await cursor.fetchone()
        message = server[2]
        channel = server[3]
        channel = client.get_channel(channel)
        message = message.replace("<name>", member.mention)
        await channel.send(message)

#Log messages from users
@client.event
async def on_message(message):
    if message.author.bot:
        return
    else:
        await checkPlayer(message.author.id) #would running this here cause a lot of issues, ensures people can play even if they joined before the bot

        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute('SELECT * FROM userMessages WHERE userID=?', (message.author.id,))
            stats = await cursor.fetchone()
            messages = stats[2]
            await db.execute('UPDATE userMessages SET messages=messages+? WHERE userID=?', (1, message.author.id))
            await db.commit()

client.run(token)