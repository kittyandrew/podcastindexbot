import importlib
import logging
import os


def init(bot, *args):
    bot.loop.run_until_complete(start_plugins(bot, *args, plugins=[
        # Dynamically import
        importlib.import_module(f'.', f'{__name__}.{file[:-3]}')

        # All the files in the current directory
        for file in os.listdir(os.path.dirname(__file__))

        # If they start with a letter and are Python files
        if file[0].isalpha() and file.endswith('.py')
    ]))


async def start_plugins(bot, *args, plugins):
    for plugin in plugins:
        logging.info("Loading plugin: '%s'..", plugin)
        p_init = getattr(plugin, 'init', None)
        if callable(p_init):
            try:
                await p_init(bot, *args)
            except Exception as e:
                logging.warn("Failed to load %s: %s (%s)", plugin.__name__, type(e), e)
