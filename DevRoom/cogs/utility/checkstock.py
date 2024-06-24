import discord
import requests
import datetime as DT

from discord import app_commands
from discord.ext import commands
from datetime import datetime

class checkstock(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="checkstock", description="Check the latest daily update to a stock!")
    @app_commands.describe(symbol="The 3 letter symbol of the stock you want to check")
    async def checkstock(self, interaction: discord.Interaction, symbol: str):
        if len(symbol) < 3 or len(symbol) > 3:
            await interaction.response.send_message(content="That is not a valid stock symbol!", ephemeral=True)
        else:
            stock = symbol.upper()
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey=ILR88NYOD5C6E1XK'
            r = requests.get(url)
            data = r.json()
            meta_data = data["Meta Data"]
            time_series = data["Time Series (Daily)"]

            metaDesc = ""
            stockDesc = ""

            for key, value in meta_data.items():
                if key == "3. Last Refreshed":
                    dateCheck = value

            for key, value in meta_data.items():
                metaDesc = metaDesc + f"\n{key}: {value}"

            for date, metrics in time_series.items():
                if date == dateCheck:
                    for metric, value in metrics.items():
                        stockDesc = stockDesc + f"\n**{metric.upper()}** {value}"

            embed = discord.Embed(title=f"📈 Stock Chart", 
                                  description=metaDesc + f"\n\nStock Values as of **{dateCheck}**\n" + stockDesc,
                                  color=discord.Color.random())
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(checkstock(bot))