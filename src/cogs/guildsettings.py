"""Houses the cog that handles guild settings commands"""

import discord
from discord.ext import commands
from discord.ui import View, Button
from config.constants import DEBUG_GUILDS
from helpers.embed_pager import EmbedPager
from services.utility_channel_service import UtilityChannelService

class GuildSettings(commands.Cog):
    """This cog handles all commands that are used for editing the bot specific settings for the
    guilds the bot is on.
    Attributes:
        bot: The bot these settings apply to
        utility_channel_service: The service used to apply settings in utility channels"""

    settings_group = discord.SlashCommandGroup(name="settings", description="Commands for setting up the bot for the guild.")

    def __init__(self, bot: discord.Bot, db_address):
        """Activate the guild settings cog
        Args:
            bot: The bot the settings apply to
            db_address: The location of the database the bot saves data to"""

        self.bot = bot
        self.utility_channel_service = UtilityChannelService(db_address)


    @settings_group.command(name="addchannelutility",
                            description="Add a new utility for a channel in the guild",
                            guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(administrator=True)
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


    @settings_group.command(name="removechannelutility",
                            description="Remove an established utility from a channel",
                            guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(administrator=True)
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
                               "Use the command `listutilitychannels` to get a list of a channel's utilities.",
                              ephemeral=True)
            return

        self.utility_channel_service.delete_utility_from_channel(channel.id, ctx.guild.id, utility)
        await ctx.respond(f"{channel.mention} no longer has the utility `{utility}`.")


    @settings_group.command(name="removeallchannelutilities",
                            description="Remove all utilities from a single channel",
                            guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(administrator=True)
    async def remove_all_channel_utilities(self,
        ctx: discord.ApplicationContext,
        channel: discord.Option(discord.TextChannel,
                                "The channel to remove utilities from")):
        """Remove all utilities from a single channel"""

        channels = self.utility_channel_service.get_guild_utility_channel_by_id(ctx.guild.id,
                                                                                channel.id)
        if not channels:
            await ctx.respond(f"{channel.mention} does not have any utilities applied. " \
                              "You can find the guild's utility channels with the " \
                              "`listchannelutilities` command.",
                              ephemeral=True)
            return
        self.utility_channel_service.delete_utility_channel(channel.id, ctx.guild.id)
        await ctx.respond(f"{channel.mention} is no longer used as a utility channel.")


    @settings_group.command(name="removeguildutilitychannels",
                            description="Clear all channel utilities from the guild",
                            guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(administrator=True)
    async def remove_guild_utility_channels(self,
        ctx: discord.ApplicationContext):
        """Remove all utility channels from a given guild"""

        channels = self.utility_channel_service.get_all_guild_utility_channels(ctx.guild.id)
        async def confirm_button_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("You cannot interact with this response.",
                                                        ephemeral=True)
                return
            self.utility_channel_service.delete_guild_utility_channels(ctx.guild.id)
            await interaction.response.edit_message(content=f"Removed **{len(channels)}** " \
                                                            f"channel utilities from {ctx.guild.name}.",
                                                    view=None)

        async def cancel_button_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("You cannot interact with this response.",
                                                        ephemeral=True)
                return
            await interaction.response.edit_message(content="Utility channel removal cancelled", view=None)

        confirm_button = Button(label="Confirm", style=discord.ButtonStyle.green)
        cancel_button = Button(label="Cancel", style=discord.ButtonStyle.red)
        confirm_button.callback = confirm_button_callback
        cancel_button.callback = cancel_button_callback
        view = View(confirm_button, cancel_button)
        await ctx.respond(f"Are you sure? This will delete **{len(channels)}** utilities from the guild.",
                          view=view)


    @settings_group.command(name="listchannelutilities",
                            description="List the channels used as utility channels",
                            guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(administrator=True)
    async def list_channel_utilities(self,
        ctx: discord.ApplicationContext,
        channel: discord.Option(discord.TextChannel,
                                "To list the utilities of a single channel, use this argument",
                                required=False)):
        """List the utility channels the guild uses"""

        embed = discord.Embed(title=f"{ctx.guild.name} utility channels")
        if channel:
            channels = self.utility_channel_service.get_guild_utility_channel_by_id(ctx.guild.id,
                                                                                    channel.id)
            embed.title = f"#{channel.name} utilities"
        else:
            channels = self.utility_channel_service.get_all_guild_utility_channels(ctx.guild.id)
        if not channels:
            if channel:
                embed.add_field(name="No utilities",
                                value="This channel has no utilities. " \
                                      "Consider adding some with the `addchannelutility` command")
            else:
                embed.add_field(name="No channels found",
                                value="This guild has no utility channels. " \
                                      "Consider adding some with the `addchannelutility` command")
            await ctx.respond(embed=embed, ephemeral=True)
            return
        fields = []
        for chan in channels:
            channel_obj = await chan.get_discord_channel(self.bot)
            fields.append(discord.EmbedField(f"#{channel_obj.name}",
                                             chan.channel_purpose))
        embed_pager = EmbedPager(fields)
        embed_pager.embed = embed
        res_embed, res_view = embed_pager.get_embed_and_view()
        await ctx.respond(embed=res_embed, view=res_view, ephemeral=True)
