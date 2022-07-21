"""Houses the Messager helper class"""

import discord
from discord.ui import View

class Messager:
    """Tries to send a message to a user
    Attributes:
        user: The user to send messages to"""

    def __init__(self, user: discord.User):
        self.user = user

    async def send_message(self, message: str, embed: discord.Embed = None, view: View = None):
        """Attempt to send a message to a user
        Args:
            message: The message to send to the user
            embed: The optional embed to send to the user
            view: The optional view to send to the user
        Returns: A status string depending on whether sending the message was a success"""

        send_success = "User was successfully notified."

        try:
            await self.user.send(content=message, embed=embed, view=view)
        except discord.Forbidden:
            send_success = "User couldn't be reached."
        except discord.HTTPException:
            send_success = "Sending a message to user failed."
        except discord.InvalidArgument:
            send_success = "Sending a message to user failed due to InvalidArgument."

        return send_success
