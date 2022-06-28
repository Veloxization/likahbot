"""Houses the class that includes methods for generating multipage embeds"""
import discord
from discord.ui import Button, View

class EmbedPager:
    """Use this class to generate embeds with multiple pages.
    Inlcudes buttons to switch pages.
    Attributes:
        fields: A list of Embed Fields containing the fields to include on different pages
        page_limit: How many fields are allowed on a single page. Must be between 1 and 25.
        embed: The embed that is generated
        pages: How many total pages are generated
        current_page: The number of the page to be displayed on the embed
        button_first: The button to take the user to the first page
        button_previous: The button to take the user to the previous page
        button_next: The button to take the user to the next page
        button_last: The button to take the user to the last page"""

    def __init__(self, fields: list, page_limit: int = 25, page: int = 1):
        """Create a new embed pager object
        Args:
            fields: A list of fields for the embed pages
            page_limit: The number of fields allowed on a single page. Cannot be over 25.
            page: The page the embed should start on"""

        self.fields = fields
        self.page_limit = min(page_limit, 25)
        self.page_limit = max(self.page_limit, 1)
        self.embed = discord.Embed()
        self.pages = len(fields) // self.page_limit
        if len(fields) % self.page_limit != 0:
            self.pages += 1
        self.current_page = min(page, self.pages)
        self.current_page = max(self.current_page, 1)
        self._button_first = Button(label="<<First", style=discord.ButtonStyle.blurple)
        self._button_first.callback = self.button_first_callback
        self._button_previous = Button(label="<Previous")
        self._button_previous.callback = self.button_previous_callback
        self._button_next = Button(label="Next>")
        self._button_next.callback = self.button_next_callback
        self._button_last = Button(label="Last>>", style=discord.ButtonStyle.blurple)
        self._button_last.callback = self.button_last_callback

    def get_embed_and_view(self):
        """Get the generated embed and view"""
        view = View()
        if self.pages > 1:
            if self.current_page == 1:
                view.add_item(self._button_next)
                view.add_item(self._button_last)
            elif self.current_page == self.pages:
                view.add_item(self._button_first)
                view.add_item(self._button_previous)
            else:
                view.add_item(self._button_first)
                view.add_item(self._button_previous)
                view.add_item(self._button_next)
                view.add_item(self._button_last)
        self.embed.clear_fields()
        self.embed.set_footer(text=f"Page {self.current_page}/{self.pages}")
        index_limit = min((self.current_page-1)*self.page_limit+self.page_limit, len(self.fields))
        for index in range((self.current_page-1)*self.page_limit, index_limit):
            self.embed.append_field(self.fields[index])
        return self.embed, view

    async def button_first_callback(self, interaction: discord.Interaction):
        """Create the first page of the embed"""
        self.current_page = 1
        embed, view = self.get_embed_and_view()
        await interaction.response.edit_message(embed=embed, view=view)

    async def button_last_callback(self, interaction: discord.Interaction):
        """Create the last page of the embed"""
        self.current_page = self.pages
        embed, view = self.get_embed_and_view()
        await interaction.response.edit_message(embed=embed, view=view)

    async def button_next_callback(self, interaction: discord.Interaction):
        """Create the next page of the embed"""
        if self.current_page + 1 <= self.pages:
            self.current_page += 1
        embed, view = self.get_embed_and_view()
        await interaction.response.edit_message(embed=embed, view=view)

    async def button_previous_callback(self, interaction: discord.Interaction):
        """Create the previous page of the embed"""
        if self.current_page - 1 >= 1:
            self.current_page -= 1
        embed, view = self.get_embed_and_view()
        await interaction.response.edit_message(embed=embed, view=view)
