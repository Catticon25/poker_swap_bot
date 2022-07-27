""" logs.py
Sets up logging
"""

import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)8s:%(name)20s: %(message)s'))
logger.addHandler(handler)