import discord
import yaml
import json
import aiosqlite
from discord.ext import commands
from datetime import datetime

async def checkPlayer(user_id: int):
    async with aiosqlite.connect('database.db') as db:
        player_cursor = await db.execute('SELECT * FROM userMessages WHERE UserId=?', (user_id,))
        player = await player_cursor.fetchone()
        if player is None:
            await db.execute('INSERT INTO userMessages (UserId) VALUES (?)', (user_id,))
            await db.commit()