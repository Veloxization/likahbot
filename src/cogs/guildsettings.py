"""Houses the cog that handles guild settings commands"""

import discord
from discord.ext import commands
from discord.ui import Button, View
from services.utility_channel_service import UtilityChannelService

class GuildSettings(commands.Cog):
    """This cog handles all commands that are used for editing the bot specific settings for the
    guilds the bot is on.
    Attributes:
        bot: The bot these settings apply to
        utility_channel_service: The service used to apply settings in utility channels"""

    def __init__(self, bot: discord.Bot, db_address):
        """Activate the guild settings cog
        Args:
            bot: The bot the settings apply to
            db_address: The location of the database the bot saves data to"""

        self.bot = bot
        self.utility_channel_service = UtilityChannelService(db_address)

    @commands.slash_command(name="addchannelutility",
                            description="Add a new utility for a channel in the guild",
                            guild_ids=[383107941173166083])
    async def add_channel_utility(self,
        ctx: discord.ApplicationContext,
        utility: discord.Option(str,
                                "The utility to add for a channel",
                                choices=["log", "rules", "verification"]),
        channel: discord.Option(discord.TextChannel, "The channel to apply the utility to")):
        """Assign a channel for a specified utility"""

        self.utility_channel_service.create_guild_utility_channel(channel.id, ctx.guild.id, utility)
        if utility == "log":
            await ctx.respond(f"{channel.mention} is now a log channel. Future logs will be posted there.")
        if utility == "rules":
            await ctx.respond(f"{channel.mention} is now a rules channel. If you've specified any rules, they will be posted and maintained there.")
        if utility == "verification":
            await ctx.respond(f"{channel.mention} is now a verification channel. New members can verify through this channel from now on.")

    @commands.slash_command(name="removechannelutility",
                            description="Remove an established utility from a channel",
                            guild_ids=[383107941173166083])
    async def remove_channel_utility(self,
        ctx: discord.ApplicationContext,
        utility: discord.Option(str,
                                "The utility to remove from the channel",
                                choices=["log", "rules", "verification"]),
        channel: discord.Option(discord.TextChannel, "The channel to remove the the utility from")):
        """Remove a utility from a certain channel"""

        channels = self.utility_channel_service.get_guild_utility_channel_by_id(ctx.guild.id, channel.id)
        utilities = [chan.channel_purpose for chan in channels]
        if utility not in utilities:
            await ctx.respond(f"{channel.mention} does not have the utility `{utility}` applied to it.\n" \
                               "Use the command `listutilitychannels` to get a list of a channel's utilities.")
            return

        self.utility_channel_service.delete_utility_from_channel(channel.id, ctx.guild.id, utility)
        await ctx.respond(f"{channel.mention} no longer has the utility `{utility}`.")

    @commands.slash_command(name="listutilitychannels",
                            description="List the channels used as utility channels",
                            guild_ids=[383107941173166083])
    async def list_utility_channels(self,
        ctx: discord.ApplicationContext,
        channel: discord.Option(discord.TextChannel,
                                "To list the utilities of a single channel, use this argument",
                                required=False)):
        """List the utility channels the guild uses"""

        if channel:
            channels = self.utility_channel_service.get_guild_utility_channel_by_id(ctx.guild.id,
                                                                                    channel.id)
        else:
            channels = self.utility_channel_service.get_all_guild_utility_channels(ctx.guild.id)
        embed = discord.Embed(title=f"{ctx.guild.name} utility channels")
        if channel:
            embed.title = f"#{channel.name} utilities"
        if not channels:
            embed.add_field(name="No channels found",
                            value="This guild has no utility channels. " \
                                  "Consider adding some with the `addchannelutility` command")
            await ctx.respond(embed=embed)
            return
        if len(channels) <= 25:
            for chan in channels:
                embed.add_field(name=f"#{ctx.guild.get_channel(chan.channel_id).name}",
                                value=chan.channel_purpose,
                                inline=True)
            await ctx.respond(embed=embed)
            return
