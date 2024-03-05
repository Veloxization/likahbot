"""Houses the cog that handles guild settings commands"""

import discord
from discord.ext import commands
from discord.ui import View, Button
from config.constants import DEBUG_GUILDS
from helpers.embed_pager import EmbedPager
from services.utility_channel_service import UtilityChannelService
from services.guild_setting_service import GuildSettingService

class GuildSettings(commands.Cog):
    """This cog handles all commands that are used for editing the bot specific settings for the
    guilds the bot is on.
    Attributes:
        bot: The bot these settings apply to
        utility_channel_service: The service used to apply settings in utility channels"""

    settings_group = discord.SlashCommandGroup(name="settings", description="Commands for setting up the bot for the guild.")
    utility_channel_group = settings_group.create_subgroup(name="utilitychannel",
                                                           description="Settings related to guild utility channels")
    log_setting_group = settings_group.create_subgroup(name="logs",
                                                       description="Change what is logged.")
    log_settings = ["log edited messages", "log deleted messages", "log membership changes",
                    "log bans", "log timeouts", "log warnings", "log name changes",
                    "log member role changes", "log avatar changes","log channel changes",
                    "log guild role changes", "log invites", "log message reactions",
                    "log webhook changes"]

    def __init__(self, bot: discord.Bot, db_address):
        """Activate the guild settings cog
        Args:
            bot: The bot the settings apply to
            db_address: The location of the database the bot saves data to"""

        self.bot = bot
        self.utility_channel_service = UtilityChannelService(db_address)
        self.guild_setting_service = GuildSettingService(db_address)


    @utility_channel_group.command(name="add",
                                   description="Add a new utility for a channel in the guild",
                                   guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(administrator=True)
    async def add_channel_utility(self,
        ctx: discord.ApplicationContext,
        utility: discord.Option(str,
                                "The utility to add for a channel",
                                choices=["log", "message log", "moderation log", "member log",
                                         "server log", "rules", "verification"]),
        channel: discord.Option(discord.TextChannel, "The channel to apply the utility to")):
        """Assign a channel for a specified utility"""

        await self.utility_channel_service.create_guild_utility_channel(channel.id, ctx.guild.id, utility)
        if utility == "log":
            await ctx.respond(f"{channel.mention} is now a log channel. All future logs will be posted there.")
        if utility == "message log":
            await ctx.respond(f"{channel.mention} is now a message log channel. Message edits, deletions and reactions will be posted there.")
        if utility == "moderation log":
            await ctx.respond(f"{channel.mention} is now a moderation log channel. Bans, unbans, timeouts and warnings will be posted there.")
        if utility == "member log":
            await ctx.respond(f"{channel.mention} is now a member log channel. Changes to membership and members' names and avatars will be posted there.")
        if utility == "guild log":
            await ctx.respond(f"{channel.mention} is now a guild log channel. Changes to the guild's channels, roles etc. will be posted there.")
        if utility == "rules":
            await ctx.respond(f"{channel.mention} is now a rules channel. If you've specified any rules, they will be posted and maintained there.")
        if utility == "verification":
            await ctx.respond(f"{channel.mention} is now a verification channel. New members can verify through this channel from now on.")


    @utility_channel_group.command(name="remove",
                                   description="Remove an established utility from a channel",
                                   guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(administrator=True)
    async def remove_channel_utility(self,
        ctx: discord.ApplicationContext,
        utility: discord.Option(str,
                                "The utility to remove from the channel",
                                choices=["log", "message log", "moderation log", "member log",
                                         "server log", "rules", "verification"]),
        channel: discord.Option(discord.TextChannel, "The channel to remove the the utility from")):
        """Remove a utility from a certain channel"""

        channels = await self.utility_channel_service.get_guild_utility_channel_by_id(ctx.guild.id, channel.id)
        utilities = [chan.channel_purpose for chan in channels]
        if utility not in utilities:
            await ctx.respond(f"{channel.mention} does not have the utility `{utility}` applied to it.\n" \
                               "Use the command `listutilitychannels` to get a list of a channel's utilities.",
                              ephemeral=True)
            return

        await self.utility_channel_service.delete_utility_from_channel(channel.id, ctx.guild.id, utility)
        await ctx.respond(f"{channel.mention} no longer has the utility `{utility}`.")


    @utility_channel_group.command(name="removeallfromchannel",
                                   description="Remove all utilities from a single channel",
                                   guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(administrator=True)
    async def remove_all_channel_utilities(self,
        ctx: discord.ApplicationContext,
        channel: discord.Option(discord.TextChannel,
                                "The channel to remove utilities from")):
        """Remove all utilities from a single channel"""

        channels = await self.utility_channel_service.get_guild_utility_channel_by_id(ctx.guild.id,
                                                                                channel.id)
        if not channels:
            await ctx.respond(f"{channel.mention} does not have any utilities applied. " \
                              "You can find the guild's utility channels with the " \
                              "`listchannelutilities` command.",
                              ephemeral=True)
            return
        await self.utility_channel_service.delete_utility_channel(channel.id, ctx.guild.id)
        await ctx.respond(f"{channel.mention} is no longer used as a utility channel.")


    @utility_channel_group.command(name="removeallfromguild",
                                   description="Clear all channel utilities from the guild",
                                   guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(administrator=True)
    async def remove_guild_utility_channels(self,
        ctx: discord.ApplicationContext):
        """Remove all utility channels from a given guild"""

        channels = await self.utility_channel_service.get_all_guild_utility_channels(ctx.guild.id)
        async def confirm_button_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("You cannot interact with this response.",
                                                        ephemeral=True)
                return
            await self.utility_channel_service.delete_guild_utility_channels(ctx.guild.id)
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


    @utility_channel_group.command(name="list",
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
            channels = await self.utility_channel_service.get_guild_utility_channel_by_id(ctx.guild.id,
                                                                                          channel.id)
            embed.title = f"#{channel.name} utilities"
        else:
            channels = await self.utility_channel_service.get_all_guild_utility_channels(ctx.guild.id)
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


    @log_setting_group.command(name="get",
                               description="Get the current value of a logging setting",
                               guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(administrator=True)
    async def get_log_setting(self,
        ctx: discord.ApplicationContext,
        log_setting: discord.Option(str,
                                    "The logging setting to view",
                                    choices=log_settings)):
        """Get the currently set value of a guild logging setting"""

        embed = discord.Embed(title=log_setting)
        guild_setting = await self.guild_setting_service.get_guild_setting_value_by_name(ctx.guild.id,
                                                                                         log_setting.replace(" ", "_"))
        value = "**ON**" if guild_setting.value == "1" else "OFF"
        embed.add_field(name="Value", value=value)
        await ctx.respond(embed=embed, ephemeral=True)


    @log_setting_group.command(name="getall",
                               description="Get the current values of all logging settings",
                               guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(administrator=True)
    async def get_all_log_settings(self, ctx: discord.ApplicationContext):
        """List the current values of all guild logging settings"""

        embed = discord.Embed(title=f"{ctx.guild.name} logging settings")
        guild_settings = await self.guild_setting_service.get_all_guild_settings(ctx.guild.id)
        fields = []
        for guild_setting in guild_settings:
            value = "**ON**" if guild_setting.value == "1" else "OFF"
            fields.append(discord.EmbedField(name=guild_setting.setting.name.replace("_", " "),
                                             value=value))
        embed_pager = EmbedPager(fields)
        embed_pager.embed = embed
        res_embed, res_view = embed_pager.get_embed_and_view()
        await ctx.respond(embed=res_embed, view=res_view, ephemeral=True)


    @log_setting_group.command(name="set",
                               description="Set the value of a logging setting",
                               guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(administrator=True)
    async def set_log_setting(self,
        ctx: discord.ApplicationContext,
        log_setting: discord.Option(str,
                                    "The logging setting to change",
                                    choices=log_settings),
        value: discord.Option(bool,
                              "Whether this option is turned on")):
        """Change the value of a guild logging setting"""

        setting_value = "1" if value else "0"
        await self.guild_setting_service.edit_guild_setting_by_setting_name(ctx.guild.id,
                                                                            log_setting.replace(" ", "_"),
                                                                            setting_value)
        embed = discord.Embed(title="Logging Setting Changed")
        embed.add_field(name=log_setting, value="**ON**" if value else "OFF")
        await ctx.respond(embed=embed)


    @log_setting_group.command(name="setall",
                               description="Set all logging settings to a single value",
                               guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(administrator=True)
    async def set_all_log_settings(self,
        ctx: discord.ApplicationContext,
        value: discord.Option(bool,
                              "Whether to set all logging settings on or off")):
        """Change the value of all guild settings to a single value"""

        setting_value = "1" if value else "0"
        await self.guild_setting_service.edit_guild_settings_by_setting_name_pattern(ctx.guild.id,
                                                                                     "log_",
                                                                                     setting_value)
        embed = discord.Embed(title="Logging Settings Changed")
        embed.add_field(name="All logging settings changed to", value="**ON**" if value else "OFF")
        await ctx.respond(embed=embed)


    @log_setting_group.command(name="default",
                               description="Set a logging setting to its default value",
                               guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(administrator=True)
    async def set_log_setting_to_default(self,
        ctx: discord.ApplicationContext,
        log_setting: discord.Option(str,
                                    "The logging setting to set to default",
                                    choices=log_settings)):
        """Change the value of a guild logging setting back to default"""

        await self.guild_setting_service.reset_guild_setting_to_default_value_by_name(ctx.guild.id,
                                                                                      log_setting.replace(" ", "_"))
        embed = discord.Embed(title="Logging Setting Reset")
        embed.add_field(name=log_setting, value="Setting reset to default")
        await ctx.respond(embed=embed)


    @log_setting_group.command(name="reset",
                               description="Reset logging settings to default",
                               guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(administrator=True)
    async def reset_log_settings(self, ctx: discord.ApplicationContext):
        """Reset all guild logging settings to default values"""

        await self.guild_setting_service.reset_all_guild_settings_to_default_value(ctx.guild.id)
        embed = discord.Embed(title="Logging Settings Reset",
                              description="All logging settings were reset to default values")
        await ctx.respond(embed=embed)
