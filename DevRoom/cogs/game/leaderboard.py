import discord
import aiosqlite

from discord import app_commands
from discord.ext import commands

class leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="leaderboard", description="View the leaderboard of total messages sent!")
    async def leaderboard(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        try:
            cursor = await db.execute('SELECT userID, messages from userMessages ORDER BY messages DESC LIMIT 25')
            results = await cursor.fetchall()
            leaderboard_entries = []

            for result in results:
                user_id = result[0]
                count = result[1]
                user = await self.bot.fetch_user(user_id)
                leaderboard_entries.append(f"{user.name}: {count}")

            leaderboard_text = "\n".join(leaderboard_entries)
            embed = discord.Embed(title="🏆 Top 25 Leaderboard", description=leaderboard_text, color=discord.Color.random())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message("An error occurred. Please ensure that you have set up the message database!", ephemeral=True)
        await db.close()
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(leaderboard(bot))