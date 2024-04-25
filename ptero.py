from discord.ext import commands
from utils import log
from pydactyl import PterodactylClient
import os
from dotenv import load_dotenv

class Ptero(commands.Cog):
    """A template cog written for unifier-plugin temmplate repo"""

    def __init__(self,bot):
        self.bot = bot
        self.ptero = None
        self.ptero_server = None
        self.logger = log.buildlogger(self.bot.package, 'sysmgr', self.bot.loglevel)

        try:
            load_dotenv()
            self.ptero = PterodactylClient(self.bot.config['ptero_endpoint'],os.environ.get('PTERO_API_KEY'))
            if not 'ptero_server_id' in list(self.bot.config.keys()):
                raise ValueError('Missing server ID')
        except:
            self.logger.exception('Failed to initialize Pterodactyl client!')

    async def cog_before_invoke(self, ctx):
        if not self.ptero or not self.ptero_server:
            return await ctx.send('Pterodactyl API is not configured properly!\nMake sure there\'s a `ptero_endpoint` and `ptero_server_id` present in config.json')

    @commands.command(hidden=True)
    async def pshutdown(self, ctx):
        """Shuts the Pterodactyl server down."""
        if not ctx.author.id == self.bot.config['owner']:
            return
        self.logger.info("Attempting graceful shutdown...")
        try:
            self.logger.info("Backing up message cache...")
            await self.bot.bridge.backup(limit=10000)
            self.logger.info("Backup complete")
            await ctx.send('Shutting down...')
            self.logger.info("Sending API request for shutdown")
            self.ptero.servers.send_power_action(self.bot.config['ptero_server_id'],'stop')
        except:
            self.logger.exception("Graceful shutdown failed")
            await ctx.send('Shutdown failed')
            return

    @commands.command(hidden=True)
    async def pkill(self, ctx, *, args=''):
        """Shuts the Pterodactyl server down forcefully."""
        if not ctx.author.id == self.bot.config['owner']:
            return
        force = False
        if 'force' in args:
            force = True
        self.logger.info("Attempting forced shutdown...")
        try:
            if not force:
                self.logger.info("Backing up message cache...")
                await self.bot.bridge.backup(limit=10000)
                self.logger.info("Backup complete")
            await ctx.send('Force shutting down...')
            self.logger.info("Sending API request for shutdown")
            self.ptero.servers.send_power_action(self.bot.config['ptero_server_id'], 'kill')
        except:
            self.logger.exception("Force shutdown failed")
            await ctx.send('Shutdown failed')
            return

    @commands.command(hidden=True)
    async def prestart(self, ctx):
        """Restarts the Pterodactyl server."""
        if not ctx.author.id == self.bot.config['owner']:
            return
        self.logger.info("Attempting graceful shutdown...")
        try:
            self.logger.info("Backing up message cache...")
            await self.bot.bridge.backup(limit=10000)
            self.logger.info("Backup complete")
            await ctx.send('Restarting...')
            self.logger.info("Sending API request for restart")
            self.ptero.servers.send_power_action(self.bot.config['ptero_server_id'], 'restart')
        except:
            self.logger.exception("Graceful restart failed")
            await ctx.send('Restart failed')
            return

def setup(bot):
    bot.add_cog(Ptero(bot))
