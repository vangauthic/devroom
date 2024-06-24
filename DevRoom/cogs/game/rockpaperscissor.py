import discord
import random

from discord import app_commands
from discord.ext import commands
from typing import Literal

class minigame(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="rps", description="Play a game of Rock, Paper, Scissors!")
    @app_commands.describe(choice="Your RPS choice")
    async def rockpaperscissors(self, interaction: discord.Interaction, choice: Literal["Rock", "Paper", "Scissors"]):
        choices = [
            "Rock",
            "Paper",
            "Scissors"
        ]
        botChoice = random.choice(choices)

        if choice == botChoice:
            message = f"You chose {choice} and the bot chose {botChoice}! It was a **TIE**!"
        elif choice == "Rock":
            if botChoice == "Paper":
                message = f"You chose {choice} and the bot chose {botChoice}! You **LOST**!"
            elif botChoice == "Scissors":
                message = f"You chose {choice} and the bot chose {botChoice}! You **WON**!"
        elif choice == "Paper":
            if botChoice == "Rock":
                message = f"You chose {choice} and the bot chose {botChoice}! You **WON**!"
            elif botChoice == "Scissors":
                message = f"You chose {choice} and the bot chose {botChoice}! You **LOST**!"
        elif choice == "Scissors":
            if botChoice == "Rock":
                message = f"You chose {choice} and the bot chose {botChoice}! You **LOST**!"
            elif botChoice == "Paper":
                message = f"You chose {choice} and the bot chose {botChoice}! You **WON**!"

        await interaction.response.send_message(message, ephemeral=True)
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(minigame(bot))