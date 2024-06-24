import aiosqlite

async def check_tables():
    # Database
    async with aiosqlite.connect('database.db') as db:
        # Creates the "welcomeMessages" table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS welcomeMessages (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            serverID INT,
            welcomeMessage STRING,
            welcomeChannel
        )
        """)

        # Creates the "scheduledMessages" table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS scheduledMessages (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            serverID INT,
            scheduledMessage STRING,
            scheduledChannel
        )
        """)

        # Creates the "userMessages" table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS userMessages (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INT,
            messages INT DEFAULT 0
        )
        """)
        await db.commit()