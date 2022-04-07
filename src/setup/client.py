"""The client file only handles setting up the bot client."""

import sys
import discord

class BotClient(discord.Client):
    """Create a new bot client object"""

    async def on_ready(self):
        """What to do once the bot has successfully logged in"""

        print(f"Python {sys.version}\n{sys.version_info}")
        print(f"Logged on as {self.user}")
