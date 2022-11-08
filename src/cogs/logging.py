"""Houses the cog that handles logging"""

import discord
import datetime
from discord.ext import commands
from services.utility_channel_service import UtilityChannelService
from helpers.invite_use_tracker import InviteUseTracker

class Logging(commands.Cog):
    """This cog handles all listeners that are used for logging events in the logging channel
    if one is defined for the guild.
    Attributes:
        bot: The bot that handles the logging
        utility_channel_service: The service used to get the logging channel"""

    def __init__(self, bot: discord.Client, db_address, invites: dict):
        """Activate the Logging cog
        Args:
            bot: The bot that does the logging
            db_address: The location where the bot database is located
            invites: A dictionary containing {Guild: [Invite]} key-value pairs"""

        self.bot = bot
        self._utility_channel_service = UtilityChannelService(db_address)
        self.invites = invites

    async def _get_guild_log_channels(self, guild: discord.Guild):
        """Get the channels used for logs for a specific guild
        Args:
            guild: The Discord Guild whose log channel to get
        Returns: A list of discord.Channel objects if log channels were found"""

        channels = self._utility_channel_service.get_guild_utility_channel_by_purpose(guild.id,
                                                                                      "log")
        if not channels:
            return None
        log_channels = [await channel.get_discord_channel(self.bot) for channel in channels]
        return log_channels

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """Log an edited message"""

        if before.author.bot:
            return

        log_channels = await self._get_guild_log_channels(after.guild)
        embed = discord.Embed(color=discord.Color.orange(),
                              title="Message edited",
                              description=f"Message by {after.author.mention} edited in {after.channel.mention}",
                              url=after.jump_url)
        embed.set_author(name=after.author, icon_url=after.author.display_avatar.url)
        embed.set_footer(text=f"ID: {after.id}")
        before_content = before.content
        after_content = after.content
        if not before_content:
            before_content = "`Could not fetch`"
        if not after_content:
            after_content = "`Could not fetch`"
        if len(before_content) > 512:
            before_content = before_content[0:256] + "...\n..." + before_content[-256:]
        if len(after_content) > 512:
            after_content = after_content[0:256] + "...\n..." + after_content[-256:]
        embed.add_field(name="Before", value=before_content)
        embed.add_field(name="After", value=after_content)
        for channel in log_channels:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """Log a deleted message"""

        if message.author.bot:
            return

        if not message:
            return
        log_channels = await self._get_guild_log_channels(message.guild)
        embed = discord.Embed(color=discord.Color.dark_orange(),
                              title="Message deleted",
                              description=f"Message by {message.author.mention} deleted in {message.channel.mention}")
        embed.set_author(name=message.author, icon_url=message.author.display_avatar.url)
        embed.set_footer(text=f"ID: {message.id}")
        content = message.content
        if not content:
            content = "`Could not fetch`"
        if len(content) > 512:
            content = content[:512] + "..."
        embed.add_field(name="Content", value=content)
        for channel in log_channels:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Log a joining member"""

        log_channels = await self._get_guild_log_channels(member.guild)
        embed = discord.Embed(color=discord.Color.green(),
                              title="Member joined",
                              description=f"{member.mention} joined **{member.guild.name}**")
        embed.set_author(name=member, icon_url=member.display_avatar.url)
        embed.set_footer(text=f"ID: {member.id}")
        embed.set_thumbnail(url=member.display_avatar.url)
        invites = await member.guild.invites()
        invite_tracker = InviteUseTracker(self.invites[member.guild], invites)
        join_invite = invite_tracker.check_difference()
        if not join_invite:
            join_invite = "`Could not fetch`"
        else:
            join_invite = f"`{join_invite.code}` by **{join_invite.inviter}**"
        embed.add_field(name="Using invite", value=join_invite)
        create_date = member.created_at.replace(tzinfo=None)
        epoch = (create_date - datetime.datetime(1970, 1, 1)).total_seconds()
        account_created = f"<t:{int(epoch)}:R>"
        embed.add_field(name="Account created", value=account_created)
        self.invites[member.guild] = await member.guild.invites()
        for channel in log_channels:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Log a leaving member"""

        log_channels = await self._get_guild_log_channels(member.guild)
        embed = discord.Embed(color=discord.Color.yellow(),
                              title="Member left",
                              description=f"{member.mention} left **{member.guild.name}**")
        embed.set_author(name=member, icon_url=member.display_avatar.url)
        embed.set_footer(text=f"ID: {member.id}")
        roles = member.roles
        roles.pop(0) # Remove the @everyone role
        if not roles:
            roles = ["N/A"]
        else:
            roles = [role.mention for role in roles]
        embed.add_field(name="Roles", value=', '.join(roles))
        for channel in log_channels:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user):
        """Log a banned user"""

        log_channels = await self._get_guild_log_channels(guild)
        embed = discord.Embed(color=discord.Color.red(),
                              title="Member banned",
                              description=f"{user.mention} was banned from **{guild.name}**")
        embed.set_author(name=user, icon_url=user.display_avatar.url)
        embed.set_footer(text=f"ID: {user.id}")
        for channel in log_channels:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user):
        """Log an unbanned user"""

        log_channels = await self._get_guild_log_channels(guild)
        embed = discord.Embed(color=discord.Color.purple(),
                              title="Member unbanned",
                              description=f"{user.mention} was unbanned in **{guild.name}**")
        embed.set_author(name=user, icon_url=user.display_avatar.url)
        embed.set_footer(text=f"ID: {user.id}")
        for channel in log_channels:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """Log updates to members"""

        log_channels = await self._get_guild_log_channels(after.guild)
        if not before.timed_out and after.timed_out:
            embed = discord.Embed(color=discord.Color.blurple(),
                                  title="Member timed out",
                                  description=f"{after.mention} was timed out in " \
                                              f"**{after.guild.name}**")
            embed.set_author(name=after, icon_url=after.display_avatar.url)
            embed.set_footer(text=f"ID: {after.id}")
            for channel in log_channels:
                await channel.send(embed=embed)

        if before.timed_out and not after.timed_out:
            embed = discord.Embed(color=discord.Color.dark_blue(),
                                  title="Member timeout removed",
                                  description=f"{after.mention}'s timeout was removed in " \
                                              f"**{after.guild.name}**")
            embed.set_author(name=after, icon_url=after.display_avatar.url)
            embed.set_footer(text=f"ID: {after.id}")
            for channel in log_channels:
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite):
        """Log an invite creation"""

        self.invites[invite.guild].append(invite)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite: discord.Invite):
        """Log an invite deletion"""

        self.invites[invite.guild] = await invite.guild.invites()
