import discord

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value == None

    @discord.ui.button(label = "Send Message", style = discord.ButtonStyle.grey)
    async def menu1(self, Button: discord.ui.Button, interaction: discord.interaction):
        await interaction.response.send_message("Hey yeah")

