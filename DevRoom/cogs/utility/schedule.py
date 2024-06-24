import discord
import aiosqlite

from discord import app_commands
from discord.ext import commands

class schedule(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="setscheduledmessage", description="Set a new scheduled message for your server!")
    @commands.has_permissions(administrator=True)
    @app_commands.describe(message="The scheduled message (Use <everyone> and <here> to mention @everyone and @here)")
    @app_commands.describe(channel="The channel to send the scheduled message in")
    async def setscheduledmessage(self, interaction: discord.Interaction, message: str, channel: discord.TextChannel):
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute('SELECT * FROM scheduledMessages WHERE serverID=?', (interaction.guild.id,))
            if await cursor.fetchone() is None:
                await db.execute('INSERT INTO scheduledMessages (serverID, scheduledMessage, scheduledChannel) VALUES (?,?,?)', (interaction.guild.id, message, channel.id))
                await db.commit()
            else:
                await db.execute('UPDATE scheduledMessages (scheduledMessage, scheduledChannel) VALUES (?,?) WHERE serverID=?', (message, channel.id, interaction.guild.id))
                await db.commit()
            embed = discord.Embed(title=f"Scheduled Message Updated", 
                                  description=f"\n\nYou have succesfully changed the server's scheduled message to:\n\n{message}",
                                  color=discord.Color.random())
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(schedule(bot))