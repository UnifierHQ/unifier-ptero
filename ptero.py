import discord
from discord.ext import commands
from utils import log
from pydactyl import PterodactylClient
import os
from dotenv import load_dotenv

class Ptero(commands.Cog):
    """A cog for managing a Pterodactyl server."""

    def __init__(self, bot):
        self.bot = bot
        self.ptero = None
        self.ptero_server_id = os.getenv('PTERO_SERVER_ID')
        self.logger = log.build_logger(self.bot.package, 'sysmgr', self.bot.loglevel)

        try:
            load_dotenv()
            ptero_endpoint = os.getenv('PTERO_ENDPOINT')
            ptero_api_key = os.getenv('PTERO_API_KEY')
            if not ptero_endpoint or not ptero_api_key or not self.ptero_server_id:
                raise ValueError('Missing required environment variables')
            self.ptero = PterodactylClient(ptero_endpoint, ptero_api_key)
        except Exception as e:
            self.logger.error(f'Failed to initialize Pterodactyl client: {e}')

    async def cog_before_invoke(self, ctx):
        if not self.ptero:
            await ctx.send('Pterodactyl API is not properly configured.')
            raise commands.CommandError("Pterodactyl API not configured")

    async def cog_command_error(self, ctx, error):
        self.logger.error(f'Command {ctx.command} failed with error: {error}')
        await ctx.send('An error occurred while processing the command.')

    async def _send_power_action(self, ctx, action):
        try:
            await ctx.send(f'Performing {action} action...')
            await self.ptero.servers.send_power_action(self.ptero_server_id, action)
            await ctx.send(f'{action.capitalize()} action successful.')
        except Exception as e:
            self.logger.error(f'Failed to {action} server: {e}')
            await ctx.send(f'Failed to {action} server.')

    @commands.command(hidden=True)
    async def pshutdown(self, ctx):
        """Gracefully shuts down the Pterodactyl server."""
        await self._send_power_action(ctx, 'stop')

    @commands.command(hidden=True)
    async def pkill(self, ctx):
        """Forcefully shuts down the Pterodactyl server."""
        await self._send_power_action(ctx, 'kill')

    @commands.command(hidden=True)
    async def prestart(self, ctx):
        """Restarts the Pterodactyl server."""
        await self._send_power_action(ctx, 'restart')

def setup(bot):
    bot.add_cog(Ptero(bot))
