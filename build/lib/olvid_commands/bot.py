"""Bot class"""

import asyncio
from olvid import OlvidClient, datatypes
from .base import CommandGroup

class Bot(OlvidClient):
    """Instance of the Bot"""
    def __init__(self, *args, prefix: str = "!", **kwargs):
        super().__init__(*args, **kwargs)
        self.command_group = CommandGroup("Main")
        self.prefix = prefix

    async def set_settings(self, settings: datatypes.IdentitySettings):
        """Set bot settings"""
        await self.settings_identity_set(settings)

    async def on_message_received(self, message: datatypes.Message):
        if message.discussion_id not in (1, 2):
            await message.reply(self, "Sorry, you can't use this bot")
            return
        body = message.body.strip()
        if body.lower().startswith(self.prefix):
            full_command = body[len(self.prefix):].strip()
            await self.command_group.check(self, message, full_command)

    async def run(self) -> asyncio.Task:
        """Run the bot"""
        task = asyncio.create_task(self.run_forever())
        return task
