"""Houses the cog that handles moderation commands"""

import discord
import aiohttp
from discord.ext import commands
from config.constants import Constants
from helpers.embed_pager import EmbedPager
from services.punishment_service import PunishmentService

class ModCommands(commands.Cog):
    """This cog handles all commands that are used for moderation purposes
    Attributes:
        bot: The bot these settings apply to
        punishment_service: The service used to log punishments"""

    def __init__(self, bot: discord.Bot, db_address):
        """Activate the mod commands cog
        Args:
            bot: The bot that runs the moderation commands
            db_address: The location of the database the bot saves data to"""

        self.bot = bot
        self.punishment_service = PunishmentService(db_address)

    @commands.slash_command(name="ban",
                            description="Ban a member or a user",
                            guild_ids=Constants.DEBUG_GUILDS.value)
    @commands.has_permissions(ban_members=True)
    async def ban(self,
        ctx: discord.ApplicationContext,
        member: discord.Option(discord.User,
                               "The user to ban from the guild. Can also be the ID of a non-member."),
        reason: discord.Option(str, "An optional reason for the ban", required=False),
        delete_message_days: discord.Option(int,
                                            "How many days worth of messages to delete from the member",
                                            min_value=0, max_value=7, default=0, required=False),
        notify: discord.Option(bool, "Whether the bot should attempt to notify the member about the ban",
                               default=False, required=False)):
        """Ban a member from the guild"""

        if isinstance(member, int):
            member = await self.bot.fetch_user(member)
        elif isinstance(member, discord.Member):
            if ctx.author.top_role <= member.top_role:
                await ctx.respond("You cannot ban this member. Insufficient role hierarchy.",
                                  ephemeral=True)
                return
        send_success = ""
        if notify and isinstance(member, discord.Member):
            try:
                await member.send(f"You have been banned from **{ctx.guild.name}**.\n" \
                                  f"Provided reason: `{reason}`")
                send_success = "User was successfully notified."
            except discord.Forbidden:
                send_success = "User couldn't be reached for notification."
            except discord.HTTPException:
                send_success = "Sending a notification failed."
            except discord.InvalidArgument:
                send_success = "Sending a notification failed due to InvalidArgument"
        await ctx.guild.ban(member, reason=reason, delete_message_days=delete_message_days)
        await ctx.respond(f"**{member.name}** was banned from **{ctx.guild.name}**. {send_success}")
        self.punishment_service.add_punishment(member.id, ctx.author.id, ctx.guild.id,
                                               punishment_type="ban", reason=reason)

    @ban.error
    async def ban_error(self, ctx: discord.ApplicationContext, error):
        """Run when the ban command encounters an error"""

        await ctx.respond(f"{error}", ephemeral=True)

    @commands.slash_command(name="kick",
                            description="Kick a member",
                            guild_ids=Constants.DEBUG_GUILDS.value)
    @commands.has_permissions(kick_members=True)
    async def kick(self,
        ctx: discord.ApplicationContext,
        member: discord.Option(discord.Member,
                               "The member to kick."),
        reason: discord.Option(str, "An optional reason for the kick", required=False),
        notify: discord.Option(bool, "Whether the bot should attempt to notify the member about the kick",
                               default=False, required=False),
        log_as_punishment: discord.Option(bool,
                                          "Whether this kick should be logged as a punishment towards the user",
                                          default=True, required=False)):
        """Kick a member from the guild"""

        if ctx.author.top_role <= member.top_role:
            await ctx.respond("You cannot kick this member. Insufficient role hierarchy.",
                              ephemeral=True)
            return
        send_success = ""
        if notify and isinstance(member, discord.Member):
            try:
                await member.send(f"You have been kicked from **{ctx.guild.name}**.\n" \
                                  f"Provided reason: `{reason}`")
                send_success = "User was successfully notified."
            except discord.Forbidden:
                send_success = "User couldn't be reached for notification."
            except discord.HTTPException:
                send_success = "Sending a notification failed."
            except discord.InvalidArgument:
                send_success = "Sending a notification failed due to InvalidArgument"
        await member.kick(reason=reason)
        await ctx.respond(f"**{member.name}** was kicked from **{ctx.guild.name}**. {send_success}")
        if log_as_punishment:
            self.punishment_service.add_punishment(member.id, ctx.author.id, ctx.guild.id,
                                                   punishment_type="kick", reason=reason)

    @kick.error
    async def kick_error(self, ctx: discord.ApplicationContext, error):
        """Run when the kick command encounters an error"""

        await ctx.respond(f"{error}", ephemeral=True)
