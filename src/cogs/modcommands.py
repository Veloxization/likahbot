"""Houses the cog that handles moderation commands"""

from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord.ui import View, Button
from config.constants import DEBUG_GUILDS
from helpers.embed_pager import EmbedPager
from helpers.temp_channel_creator import TempChannelCreator
from helpers.messager import Messager
from services.punishment_service import PunishmentService
from services.temp_ban_service import TempBanService
from time_handler.time import TimeStringConverter, EpochConverter

class ModCommands(commands.Cog):
    """This cog handles all commands that are used for moderation purposes
    Attributes:
        bot: The bot these settings apply to
        punishment_service: The service used to log punishments"""

    mod_group = discord.SlashCommandGroup(name="mod", description="Commands for moderation purposes.")

    def __init__(self, bot: discord.Bot, db_address):
        """Activate the mod commands cog
        Args:
            bot: The bot that runs the moderation commands
            db_address: The location of the database the bot saves data to"""

        self.bot = bot
        self.punishment_service = PunishmentService(db_address)
        self.temp_ban_service = TempBanService(db_address)


    @mod_group.command(name="ban",
                       description="Ban a member or a user",
                       guild_ids=DEBUG_GUILDS)
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
            messager = Messager(member)
            send_success = await messager.send_message("You have been banned from " \
                                                       f"**{ctx.guild.name}**.\n" \
                                                       f"Provided reason: `{reason}`")
        await ctx.guild.ban(member, reason=reason, delete_message_days=delete_message_days)
        await ctx.respond(f"**{member}** was banned from **{ctx.guild.name}**. {send_success}")
        await self.punishment_service.add_punishment(member.id, ctx.author.id, ctx.guild.id,
                                                     punishment_type="ban", reason=reason)

    @ban.error
    async def ban_error(self, ctx: discord.ApplicationContext, error):
        """Run when the ban command encounters an error"""

        await ctx.respond(f"{error}", ephemeral=True)


    @mod_group.command(name="tempban",
                       description="Temporarily ban a member or a user",
                       guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(ban_members=True)
    async def temp_ban(self,
        ctx: discord.ApplicationContext,
        member: discord.Option(discord.User,
                               "The user to temporarily ban from the guild. Can also be the ID of a non-member."),
        days: discord.Option(int, "How many days to ban the user for",
                             min_value=1, max_value=1095),
        reason: discord.Option(str, "An optional reason for the temporary ban", required=False),
        delete_message_days: discord.Option(int,
                                            "How many days worth of messages to delete from the member",
                                            min_value=0, max_value=7, default=0, required=False),
        notify: discord.Option(bool, "Whether the bot should attempt to notify the member about the temporary ban",
                               default=False, required=False)):
        """Temporarily ban a member from the guild"""

        time_converter = TimeStringConverter()
        epoch_converter = EpochConverter()

        try:
            ban = await ctx.guild.fetch_ban(member)
        except discord.NotFound:
            ban = None
    
        if not ban and await self.temp_ban_service.get_temp_ban(member.id, ctx.guild.id):
            await self.temp_ban_service.delete_temp_ban(member.id, ctx.guild.id)

        async def modify_button_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("You cannot interact with this response.",
                                                        ephemeral=True)
                return
            expiration_date = datetime.utcnow() + timedelta(days=days)
            expiration_date_str = time_converter.datetime_to_string(expiration_date)
            expiration_date_epoch = epoch_converter.convert_to_epoch(expiration_date)
            temp_ban = await self.temp_ban_service.get_temp_ban(member.id, ctx.guild.id)
            if not temp_ban:
                await self.temp_ban_service.create_temp_ban(member.id, ctx.guild.id, expiration_date_str)
            else:
                await self.temp_ban_service.edit_temp_ban(member.id, ctx.guild.id, expiration_date_str)
            await interaction.response.edit_message(content=f"**{member}**'s ban was edited. " \
                                                            f"The ban will expire <t:{expiration_date_epoch}:D>.",
                                                    view=None)

        async def unban_button_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("You cannot interact with this response.",
                                                        ephemeral=True)
                return
            await ctx.guild.unban(member, reason=reason)
            await self.temp_ban_service.delete_temp_ban(member.id, ctx.guild.id)
            await interaction.response.edit_message(content=f"**{member}** has been unbanned. " \
                                                            "Consider using the `unban` command next time.",
                                                    view=None)

        async def cancel_button_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("You cannot interact with this response.",
                                                        ephemeral=True)
                return

            await interaction.response.edit_message(content=f"**{member}**'s ban was not changed.",
                                                    view=None)

        if ban:
            button_modify = Button(label="Modify", style=discord.ButtonStyle.blurple, emoji="🛠️")
            button_modify.callback = modify_button_callback
            button_unban = Button(label="Unban", style=discord.ButtonStyle.red)
            button_unban.callback = unban_button_callback
            button_cancel = Button(label="Cancel", style=discord.ButtonStyle.gray)
            button_cancel.callback = cancel_button_callback
            view = View(button_modify, button_unban, button_cancel)
            temp_ban = await self.temp_ban_service.get_temp_ban(member.id, ctx.guild.id)
            if temp_ban:
                unban_datetime = time_converter.string_to_datetime(temp_ban.unban_date)
                expiration_epoch = epoch_converter.convert_to_epoch(unban_datetime)
                await ctx.respond(content="This user already has a temporary ban that will expire " \
                                          f"<t:{expiration_epoch}:D>. "
                                          "Do you want to edit the temporary ban " \
                                          "or were you trying to unban?",
                                          view=view)
            else:
                await ctx.respond(content="This user already has an active ban. " \
                                          "Do you want to convert it to a temporary ban " \
                                          "or were you trying to unban?",
                                          view=view)
            return

        if isinstance(member, discord.Member):
            if ctx.author.top_role <= member.top_role:
                await ctx.respond("You cannot ban this member. Insufficient role hierarchy.",
                                  ephemeral=True)
                return
        send_success = ""
        ban_expiration = datetime.utcnow() + timedelta(days=days)
        db_ban_expiration = time_converter.datetime_to_string(ban_expiration)
        ban_expiration_epoch = epoch_converter.convert_to_epoch(ban_expiration)
        if notify:
            messager = Messager(member)
            send_success = await messager.send_message("You have been temporarily banned from " \
                                                       f"**{ctx.guild.name}**.\n" \
                                                       f"Your ban will expire on <t:{ban_expiration_epoch}:D>\n" \
                                                       f"Provided reason: `{reason}`")
        await ctx.guild.ban(member, reason=reason, delete_message_days=delete_message_days)
        await self.temp_ban_service.create_temp_ban(member.id, ctx.guild.id, db_ban_expiration)
        await self.punishment_service.add_punishment(member.id, ctx.author.id, ctx.guild.id,
                                                     punishment_type="temporary ban", reason=reason)
        await ctx.respond(f"**{member}** was temporarily banned from **{ctx.guild.name}**. " \
                          f"Ban expires <t:{ban_expiration_epoch}:D>. {send_success}")

    @temp_ban.error
    async def temp_ban_error(self, ctx: discord.ApplicationContext, error):
        """Run when the tempban command encounters an error"""

        await ctx.respond(f"{error}", ephemeral=True)


    @mod_group.command(name="unban",
                       description="Unban a user",
                       guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(ban_members=True)
    async def unban(self,
        ctx: discord.ApplicationContext,
        member: discord.Option(discord.User,
                               "The user to unban from the guild."),
        reason: discord.Option(str,
                               "The reason for the unban. Will appear in audit log.",
                               required=False)):
        """Unban a member from the guild"""

        await ctx.guild.unban(member, reason=reason)
        await ctx.respond(f"**{member}** was unbanned from **{ctx.guild.name}**")

    @unban.error
    async def unban_error(self, ctx: discord.ApplicationContext, error):
        """Run when the unban command encounters an error"""

        await ctx.respond(f"{error}", ephemeral=True)


    @mod_group.command(name="kick",
                       description="Kick a member",
                       guild_ids=DEBUG_GUILDS)
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
            messager = Messager(member)
            send_success = await messager.send_message("You have been kicked from " \
                                                       f"**{ctx.guild.name}**.\n" \
                                                       f"Provided reason: `{reason}`")
        await member.kick(reason=reason)
        await ctx.respond(f"**{member}** was kicked from **{ctx.guild.name}**. {send_success}")
        if log_as_punishment:
            await self.punishment_service.add_punishment(member.id, ctx.author.id, ctx.guild.id,
                                                         punishment_type="kick", reason=reason)

    @kick.error
    async def kick_error(self, ctx: discord.ApplicationContext, error):
        """Run when the kick command encounters an error"""

        await ctx.respond(f"{error}", ephemeral=True)


    @mod_group.command(name="warn",
                       description="Warn a member",
                       guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(moderate_members=True)
    async def warn(self,
        ctx: discord.ApplicationContext,
        member: discord.Option(discord.Member, "The member to warn"),
        reason: discord.Option(str, "The reason for the warning")):
        """Send and log a warning to a member"""

        if ctx.author.top_role < member.top_role:
            await ctx.respond("You cannot send a warning. Insufficient role hierarchy.",
                              ephemeral=True)
            return
        punishment_id = await self.punishment_service.add_punishment(member.id, ctx.author.id,
                                                                     ctx.guild.id,
                                                                     punishment_type="warn",
                                                                     reason=reason)
        punishment = await self.punishment_service.get_punishment_by_id(punishment_id)
        try:
            await member.send(f"You have been issued a warning on **{ctx.guild.name}**\n" \
                              f"Provided reason:\n`{reason}`")
            await ctx.respond(f"**{member}** was sent a warning.")
        except discord.Forbidden:
            temp_channel_creator = TempChannelCreator(self.bot, ctx.guild)
            await temp_channel_creator.get_temp_category()
            channel = await temp_channel_creator.create_warn_channel(member,
                                                                     punishment.db_id,
                                                                     punishment.reason)
            await ctx.respond(f"A new warning channel was created for **{member}**: " \
                              f"{channel.mention}")

        await self.bot.cogs["Logging"].on_member_warn(member, punishment)

    @warn.error
    async def warn_error(self, ctx: discord.ApplicationContext, error):
        """Run when the warn command encounters an error"""

        await ctx.respond(f"{error}", ephemeral=True)


    @mod_group.command(name="timeout",
                       description="Time out a member or modify or end an existing timeout. " \
                                   "If no time is specified, defaults to 1 hour.",
                       guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(moderate_members=True)
    async def timeout(self,
        ctx: discord.ApplicationContext,
        member: discord.Option(discord.Member, "The member to time out"),
        reason: discord.Option(str, "The reason for the time out", required=False),
        minutes: discord.Option(int, "Minutes to add to the timeout duration",
                                min_value=1, max_value=59, default=0, required=False),
        hours: discord.Option(int, "Hours to add to the timeout duration",
                              min_value=1, max_value=23, default=0, required=False),
        days: discord.Option(int, "Days to add to the timeout duration",
                             min_value=1, max_value=7, default=0, required=False),
        notify: discord.Option(bool,
                               "Whether the bot should attempt to notify the member about the timeout",
                               default=False, required=False),
        log_as_punishment: discord.Option(bool,
                                          "Whether this timeout should be logged as a punishment towards the user",
                                          default=True, required=False)):
        """Time out a member, preventing them from chatting and joining voice channels"""

        duration = timedelta(days=days, hours=hours, minutes=minutes)
        if duration.days == 0 and duration.seconds == 0:
            duration = timedelta(hours=1)
        async def modify_button_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("You cannot interact with this response.",
                                                        ephemeral=True)
                return
            await member.remove_timeout(reason="Modifying existing timeout")
            await member.timeout_for(duration=duration,
                                     reason=f"Modified existing timeout with reason: {reason}")
            success = ""
            if notify:
                messager = Messager(member)
                success = await messager.send_message(f"Your existing timeout in **{ctx.guild.name}** " \
                                                      "has been modified.\n" \
                                                      f"Provided reason: `{reason}`")
            await interaction.response.edit_message(content=f"{member}'s timeout modified with new parameters. {success}",
                                                    view=None)
            if log_as_punishment:
                await self.punishment_service.add_punishment(member.id, interaction.user.id,
                                                             interaction.guild.id,
                                                             punishment_type="timeout",
                                                             reason=f"Timeout modified with reason: {reason}")

        async def end_timeout_button_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("You cannot interact with this response.",
                                                        ephemeral=True)
                return
            await member.remove_timeout()
            await interaction.response.edit_message(content=f"{member}'s timeout ended.\n" \
                                                    "Consider using the `removetimeout` command in " \
                                                    "the future for faster interaction.",
                                                    view=None)

        async def cancel_button_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("You cannot interact with this response.",
                                                        ephemeral=True)
                return
            await interaction.response.edit_message(content=f"{member}'s timeout was not changed", view=None)

        if member.timed_out:
            button_modify = Button(label="Modify", style=discord.ButtonStyle.blurple, emoji="🛠️")
            button_modify.callback = modify_button_callback
            button_end = Button(label="End timeout", style=discord.ButtonStyle.gray)
            button_end.callback = end_timeout_button_callback
            button_cancel = Button(label="Cancel action", style=discord.ButtonStyle.red)
            button_cancel.callback = cancel_button_callback
            view = View(button_modify, button_end, button_cancel)
            await ctx.respond(f"{member} is already timed out. " \
                             "Do you want to add a new timeout, " \
                             "end the current one or cancel this interaction?",
                             view=view)
        else:
            await member.timeout_for(duration=duration, reason=reason)
            success = ""
            if notify:
                messager = Messager(member)
                success = await messager.send_message(f"You have been timed out.\n" \
                                                      f"Provided reason: `{reason}`")
            await ctx.respond(f"**{member.name}** was timed out. {success}")
            if log_as_punishment:
                await self.punishment_service.add_punishment(member.id, ctx.author.id,
                                                             ctx.guild.id,
                                                             punishment_type="timeout",
                                                             reason=reason)

    @timeout.error
    async def timeout_error(self, ctx: discord.ApplicationContext, error):
        """Run when the timeout command encounters an error"""

        await ctx.respond(f"{error}", ephemeral=True)


    @mod_group.command(name="removetimeout",
                       description="Remove a timeout from a member",
                       guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(moderate_members=True)
    async def remove_timeout(self,
        ctx: discord.ApplicationContext,
        member: discord.Option(discord.Member, "The timed out member whose timeout to remove"),
        notify: discord.Option(bool,
                               "Whether the bot should attempt to notify the member about ending " \
                               "the timeout", default=False, required=False)):
        """Remove a member's timeout"""

        if ctx.author.top_role <= member.top_role:
            await ctx.respond("You cannot end this timeout. " \
                              "Insufficient role hierarchy.",
                              ephemeral=True)
            return

        if not member.timed_out:
            await ctx.respond(f"{member} is not timed out! " \
                              "Are you sure you picked the right member?",
                              ephemeral=True)
            return

        await member.remove_timeout()
        success = ""
        if notify:
            messager = Messager(member)
            success = await messager.send_message(f"Your timeout in **{ctx.guild}** " \
                                                  "has been ended.")
        await ctx.respond(f"{member}'s timeout ended. {success}")

    @remove_timeout.error
    async def remove_timeout_error(self, ctx: discord.ApplicationContext, error):
        """Run when the removetimeout command encounters an error"""

        await ctx.respond(f"{error}", ephemeral=True)


    @mod_group.command(name="listpunishments",
                       description="List punishments for a user",
                       guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(moderate_members=True)
    async def list_punishments(self,
        ctx: discord.ApplicationContext,
        user: discord.Option(discord.User, "The user whose punishment history to view")):
        """List a user's punishments"""

        punishments = await self.punishment_service.get_user_punishments(user.id, ctx.guild.id)
        punishment_fields = []
        time_converter = TimeStringConverter()
        epoch_converter = EpochConverter()
        for punishment in punishments:
            time = time_converter.string_to_datetime(punishment.time)
            epoch = epoch_converter.convert_to_epoch(time)
            issuer = await punishment.get_discord_issuer(self.bot)
            field = discord.EmbedField(f"ID: {punishment.db_id}, Type: {punishment.punishment_type}",
                                       f"**Time:** <t:{epoch}>\n" \
                                       f"**Issuer:** {issuer}\n" \
                                       f"`{punishment.reason}`")
            punishment_fields.append(field)

        embed_pager = EmbedPager(punishment_fields, page_limit=5)
        embed_pager.embed = discord.Embed(title=f"Punishments of {user}",
                                          color=discord.Color.dark_orange(),
                                          description=f"{user.name} has " \
                                                      f"{len(punishment_fields)} punishments")
        embed, view = embed_pager.get_embed_and_view()
        await ctx.respond(embeds=[embed], view=view, ephemeral=True)

    @list_punishments.error
    async def list_punishments_error(self, ctx: discord.ApplicationContext, error):
        """Run when the listpunishments command encounters an error"""

        await ctx.respond(f"{error}", ephemeral=True)


    @mod_group.command(name="listdeletedpunishments",
                       description="List deleted punishments for a user",
                       guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(moderate_members=True)
    async def list_deleted_punishments(self,
        ctx: discord.ApplicationContext,
        user: discord.Option(discord.User, "The user whose deleted punishments to view")):
        """List a user's deleted punishments"""

        punishments = await self.punishment_service.get_deleted_punishments(user.id, ctx.guild.id)
        punishment_fields = []
        time_converter = TimeStringConverter()
        epoch_converter = EpochConverter()
        for punishment in punishments:
            time = time_converter.string_to_datetime(punishment.time)
            epoch = epoch_converter.convert_to_epoch(time)
            issuer = await punishment.get_discord_issuer(self.bot)
            field = discord.EmbedField(f"ID: {punishment.db_id}, Type: {punishment.punishment_type}",
                                       f"**Time:** <t:{epoch}>\n" \
                                       f"**Issuer:** {issuer}\n" \
                                       f"`{punishment.reason}`")
            punishment_fields.append(field)

        embed_pager = EmbedPager(punishment_fields, page_limit=5)
        embed_pager.embed = discord.Embed(title=f"Deleted punishments of {user}",
                                          color=discord.Color.dark_red(),
                                          description=f"{user.name} has " \
                                                      f"{len(punishment_fields)} deleted punishments")
        embed, view = embed_pager.get_embed_and_view()
        await ctx.respond(embeds=[embed], view=view, ephemeral=True)

    @list_deleted_punishments.error
    async def list_deleted_punishments_error(self, ctx: discord.ApplicationContext, error):
        """Run when the listdeteletedpunishments command encounters an error"""

        await ctx.respond(f"{error}", ephemeral=True)


    @mod_group.command(name="listallpunishments",
                       description="List all punishments the user has, " \
                                   "including deleted ones",
                       guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(moderate_members=True)
    async def list_all_punishments(self,
        ctx: discord.ApplicationContext,
        user: discord.Option(discord.User, "The user whose punishments to view")):
        """List a user's punishments regardless of deletion status"""

        punishments = await self.punishment_service.get_all_user_punishments(user.id, ctx.guild.id)
        punishment_fields = []
        time_converter = TimeStringConverter()
        epoch_converter = EpochConverter()
        for punishment in punishments:
            time = time_converter.string_to_datetime(punishment.time)
            epoch = epoch_converter.convert_to_epoch(time)
            issuer = await punishment.get_discord_issuer(self.bot)
            if punishment.deleted:
                field = discord.EmbedField(f"~~ID: {punishment.db_id}, Type: {punishment.punishment_type}~~",
                                           f"~~**Time:** <t:{epoch}>\n" \
                                           f"**Issuer:** {issuer}\n" \
                                           f"`{punishment.reason}`~~")
            else:
                field = discord.EmbedField(f"ID: {punishment.db_id}, Type: {punishment.punishment_type}",
                                           f"**Time:** <t:{epoch}>\n" \
                                           f"**Issuer:** {issuer}\n" \
                                           f"`{punishment.reason}`")
            punishment_fields.append(field)

        embed_pager = EmbedPager(punishment_fields, page=5)
        embed_pager.embed = discord.Embed(title=f"Punishments of {user}",
                                          color=discord.Color.orange(),
                                          description=f"{user.name} has " \
                                                      f"{len(punishment_fields)} punishments")
        embed, view = embed_pager.get_embed_and_view()
        await ctx.respond(embeds=[embed], view=view, ephemeral=True)

    @list_all_punishments.error
    async def list_all_punishments_error(self, ctx: discord.ApplicationContext, error):
        """Run when listallpunishments command encounters an error"""

        await ctx.respond(f"{error}", ephemeral=True)


    @mod_group.command(name="editpunishment",
                       description="Edit an existing punishment for a user.",
                       guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(moderate_members=True)
    async def edit_punishment(self,
        ctx: discord.ApplicationContext,
        punishment_id: discord.Option(int, "The ID of the punishment to edit"),
        new_reason: discord.Option(str, "The new reason for this punishment")):
        """Edit a specific punishment"""

        punishment = await self.punishment_service.get_punishment_by_id(punishment_id)

        if not punishment:
            await ctx.respond(f"No punishment with ID {punishment_id} found.\n" \
                              "Use the `listpunishments` command to get punishment IDs.",
                              ephemeral=True)
            return
        if punishment.guild_id != ctx.guild.id:
            await ctx.respond(f"No punishment with ID {punishment_id} found for this guild.\n" \
                              "Make sure you run this command within the punishment's guild.",
                              ephemeral=True)
            return

        await self.punishment_service.edit_punishment_reason(punishment_id, new_reason)
        time_converter = TimeStringConverter()
        punishment_timestamp = time_converter.string_to_datetime(punishment.time)
        embed = discord.Embed(title=f"Punishment {punishment_id}", timestamp=punishment_timestamp,
                              description=f"Punishment ID {punishment_id} has been edited.",
                              color=discord.Color.blurple())
        if not punishment.reason:
            punishment.reason = "N/A"
        user = await punishment.get_discord_user(self.bot)
        issuer = await punishment.get_discord_issuer(self.bot)
        embed.add_field(name="User", value=user, inline=False)
        embed.add_field(name="Issuer", value=issuer, inline=False)
        embed.add_field(name="Type", value=punishment.punishment_type, inline=False)
        embed.add_field(name="Reason before", value=punishment.reason)
        embed.add_field(name="Reason after", value=new_reason)
        await ctx.respond(embed=embed)

    @edit_punishment.error
    async def edit_punishment_error(self, ctx: discord.ApplicationContext, error):
        """Run when the editpunishment command encounters and error"""

        await ctx.respond(f"{error}", ephemeral=True)


    @mod_group.command(name="deletepunishment",
                       description="Delete a punishment from a user. " \
                                   "Punishments deleted with this command can be recovered.",
                       guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(moderate_members=True)
    async def delete_punishment(self,
        ctx: discord.ApplicationContext,
        punishment_id: discord.Option(int, "The ID of the punishment to delete")):
        """Delete a specific punishment"""

        punishment = await self.punishment_service.get_punishment_by_id(punishment_id)

        if not punishment:
            await ctx.respond(f"No punishment with ID {punishment_id} found.\n" \
                              "Use the `listpunishments` command to get punishment IDs.",
                              ephemeral=True)
            return
        if punishment.guild_id != ctx.guild.id:
            await ctx.respond(f"No punishment with ID {punishment_id} found for this guild.\n" \
                              "Make sure you run this command within the punishment's guild.",
                              ephemeral=True)
            return
        if punishment.deleted:
            await ctx.respond(f"Punishment with ID {punishment_id} is already deleted.\n" \
                              "Did you mean to use the `restorepunishment` command?",
                              ephemeral=True)
            return

        await self.punishment_service.mark_deleted(punishment_id)
        time_converter = TimeStringConverter()
        punishment_timestamp = time_converter.string_to_datetime(punishment.time)
        embed = discord.Embed(title=f"Punishment {punishment_id}", timestamp=punishment_timestamp,
                              description=f"Punishment ID {punishment_id} has been deleted.",
                              color=discord.Color.purple())
        if not punishment.reason:
            punishment.reason = "N/A"
        user = await punishment.get_discord_user(self.bot)
        issuer = await punishment.get_discord_issuer(self.bot)
        embed.add_field(name="User", value=user, inline=False)
        embed.add_field(name="Issuer", value=issuer, inline=False)
        embed.add_field(name="Type", value=punishment.punishment_type, inline=False)
        embed.add_field(name="Reason", value=punishment.reason, inline=False)
        await ctx.respond(embed=embed)

    @delete_punishment.error
    async def delete_punishment_error(self, ctx: discord.ApplicationContext, error):
        """Run when the deletepunishment command encounters an error"""

        await ctx.respond(f"{error}", ephemeral=True)


    @mod_group.command(name="permadeletepunishment",
                       description="Permanently delete a punishment record. " \
                       "Punishments deleted like this cannot be recovered.",
                       guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(administrator=True)
    async def permadelete_punishment(self,
        ctx: discord.ApplicationContext,
        punishment_id: discord.Option(int, "The ID of the punishment to permanently delete")):
        """Permanently delete a punishment from a user"""

        punishment = await self.punishment_service.get_punishment_by_id(punishment_id)

        if not punishment:
            await ctx.respond(f"No punishment with ID {punishment_id} found.\n" \
                              "Use the `listallpunishments` command to get punishment IDs.",
                              ephemeral=True)
            return
        if punishment.guild_id != ctx.guild.id:
            await ctx.respond(f"No punishment with ID {punishment_id} found for this guild.\n" \
                              "Make sure you run this command within the punishment's guild.",
                              ephemeral=True)
            return

        time_converter = TimeStringConverter()
        punishment_timestamp = time_converter.string_to_datetime(punishment.time)
        embed = discord.Embed(title=f"Punishment {punishment_id}", timestamp=punishment_timestamp,
                              description=f"Punishment ID {punishment_id} will be permanently " \
                                          "deleted.",
                              color=discord.Color.red())
        if not punishment.reason:
            punishment.reason = "N/A"
        user = await punishment.get_discord_user(self.bot)
        issuer = await punishment.get_discord_issuer(self.bot)
        embed.add_field(name="User", value=user, inline=False)
        embed.add_field(name="Issuer", value=issuer, inline=False)
        embed.add_field(name="Type", value=punishment.punishment_type, inline=False)
        embed.add_field(name="Reason", value=punishment.reason, inline=False)

        async def delete_button_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("You cannot interact with this response.",
                                                        ephemeral=True)
                return
            embed.description = f"Punishment ID {punishment_id} has been permanently " \
                                "deleted."
            await self.punishment_service.delete_punishment(punishment_id)
            await interaction.response.edit_message(content=None, view=None, embed=embed)
        async def cancel_button_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("You cannot interact with this response.",
                                                        ephemeral=True)
                return
            await interaction.response.edit_message(content="Permanent deletion of punishment ID " \
                                                    f"{punishment_id} cancelled",
                                                    embed=None, view=None)

        delete_button = Button(label="Delete", style=discord.ButtonStyle.red)
        delete_button.callback = delete_button_callback
        cancel_button = Button(label="Cancel", style=discord.ButtonStyle.gray)
        cancel_button.callback = cancel_button_callback
        view = View(delete_button, cancel_button)
        await ctx.respond("**NOTE:** This command will *permanently* delete this punishment.\n" \
                          "If you want to be able to view or recover this punishment " \
                          "in the future, use the `deletepunishment` command instead.",
                          embed=embed, view=view)

    @permadelete_punishment.error
    async def permadelete_punishment_error(self, ctx: discord.ApplicationContext, error):
        """Run when the permadeletepunishment command encounters an error"""

        await ctx.respond(f"{error}", ephemeral=True)


    @mod_group.command(name="restorepunishment",
                       description="Restore a previously deleted punishment",
                       guild_ids=DEBUG_GUILDS)
    @commands.has_permissions(moderate_members=True)
    async def restore_punishment(self,
        ctx: discord.ApplicationContext,
        punishment_id: discord.Option(int, "The ID of the punishment to restore")):
        """Restore a deleted punishment"""

        punishment = await self.punishment_service.get_punishment_by_id(punishment_id)

        if not punishment:
            await ctx.respond(f"No punishment with ID {punishment_id} found.\n" \
                              "Use the `listdeletedpunishments` command to get punishment IDs of " \
                              "deleted punishments.",
                              ephemeral=True)
            return
        if punishment.guild_id != ctx.guild.id:
            await ctx.respond(f"No punishment with ID {punishment_id} found for this guild.\n" \
                              "Make sure you run this command within the punishment's guild.",
                              ephemeral=True)
            return
        if not punishment.deleted:
            await ctx.respond(f"Punishment with ID {punishment_id} is not deleted and does not " \
                              "need to be restored.",
                              ephemeral=True)
            return

        await self.punishment_service.unmark_deleted(punishment_id)
        time_converter = TimeStringConverter()
        punishment_timestamp = time_converter.string_to_datetime(punishment.time)
        embed = discord.Embed(title=f"Punishment {punishment_id}", timestamp=punishment_timestamp,
                              description=f"Punishment ID {punishment_id} has been restored.",
                              color=discord.Color.dark_green())
        if not punishment.reason:
            punishment.reason = "N/A"
        user = await punishment.get_discord_user(self.bot)
        issuer = await punishment.get_discord_issuer(self.bot)
        embed.add_field(name="User", value=user, inline=False)
        embed.add_field(name="Issuer", value=issuer, inline=False)
        embed.add_field(name="Type", value=punishment.punishment_type, inline=False)
        embed.add_field(name="Reason", value=punishment.reason, inline=False)
        await ctx.respond(embed=embed)

    @restore_punishment.error
    async def restore_punishment_error(self, ctx: discord.ApplicationContext, error):
        """Run when the restorepunishment command encounters an error"""

        await ctx.respond(f"{error}", ephemeral=True)
