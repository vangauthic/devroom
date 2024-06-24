import discord
import aiosqlite

from discord import app_commands
from discord.ext import commands

class welcome(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="setwelcomemessage", description="Set a new welcome message for your server!")
    @commands.has_permissions(administrator=True)
    @app_commands.describe(message="The welcome message (Use <name> to mention new users)")
    @app_commands.describe(channel="The channel to send the welcome messages in")
    async def setwelcomemessage(self, interaction: discord.Interaction, message: str, channel: discord.TextChannel):
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute('SELECT * FROM welcomeMessages WHERE serverID=?', (interaction.guild.id,))
            if await cursor.fetchone() is None:
                await db.execute('INSERT INTO welcomeMessages (serverID, welcomeMessage, welcomeChannel) VALUES (?,?,?)', (interaction.guild.id, message, channel.id))
                await db.commit()
            else:
                await db.execute('UPDATE welcomeMessages (welcomeMessage, welcomeChannel) VALUES (?,?) WHERE serverID=?', (message, channel.id, interaction.guild.id))
                await db.commit()
            embed = discord.Embed(title=f"Welcome Message Updated", 
                                  description=f"\n\nYou have succesfully changed the server's welcome message to:\n\n{message}",
                                  color=discord.Color.random())
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(welcome(bot))