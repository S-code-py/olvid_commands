"""Essentials functions and class"""

from typing import Coroutine, Dict, Union, Callable, Optional

class CommandGroup:
    """Group of commands"""
    def __init__(self, name: str, description: str = "Command group"):
        self.description = description
        self.name = name
        self.commands: Dict[str, Union[Callable, 'CommandGroup']] = {
            "help": self.help
        }

    def add_command(self, name: Optional[str] = None, afunc: Optional[Coroutine] = None):
        """Decorator to add a command to this group."""
        if afunc is None:
            def decorator(func):
                command_name = name or func.__name__
                command_name = command_name.lower()
                self.commands[command_name] = func
                return func
            return decorator
        command_name = name or afunc.__name__
        command_name = command_name.lower()
        self.commands[command_name] = afunc
        return afunc

    def create_subgroup(self, name: str, descr: str = "Command group") -> 'CommandGroup':
        """Create or retrieve a subgroup."""
        key = name.lower()
        if key not in self.commands:
            self.commands[key] = CommandGroup(name, description=descr)
        return self.commands[key]

    async def check(self, bot, message, args: str) -> bool:
        """Check and execute the command or subgroup."""
        if not args:
            return False
        parts = args.split(" ", 1)
        key_word = parts[0].lower()
        remaining_args = parts[1] if len(parts) > 1 else None
        if key_word in self.commands:
            command_or_group = self.commands[key_word]
            if isinstance(command_or_group, CommandGroup):
                if remaining_args is not None:
                    await command_or_group.check(bot, message, remaining_args)
                else:
                    await message.reply(bot, f"Usage: {bot.prefix}{key_word} [subcommand]")
            else:
                await command_or_group(bot, message, remaining_args)
            return True
        return False

    async def help(self, client, message, _parts: str):
        """Show this message"""
        body = f"**Help {self.name}:** \n\n"
        for key, func_or_group in self.commands.items():
            if isinstance(func_or_group, CommandGroup):
                body += f"`{key}`: {func_or_group.description}\n"
            else:
                body += f"`{key}`: {func_or_group.__doc__ or 'No description'}\n"
        await message.reply(client=client, body=body, quote_message=False)
