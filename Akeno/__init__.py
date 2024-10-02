import asyncio
import logging
import os
import random
import re
import string
import time
from datetime import datetime as dt
from inspect import getfullargspec
from os import path
from platform import python_version
from random import choice

import aiohttp
import pyrogram
from pyrogram import Client
from pyrogram import __version__ as pyrogram_version
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.raw.all import layer
from pyrogram.types import *

from Akeno.utils.logger import LOGS
from config import API_HASH, API_ID, SESSION, SESSION2, SESSION3, SESSION4, SESSION5, SESSION6,SESSION7, SESSION8, SESSION9, SESSION10

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

StartTime = time.time()
START_TIME = dt.now()
CMD_HELP = {}
clients = []
ids = []
act = []
db = {}


SUDOERS = filters.user()

__version__ = {
    "pyrogram": pyrogram_version,
    "python": python_version(),
}

APP_VERSION = "latest"
DEVICE_MODEL = "Akeno"
SYSTEM_VERSION = "Linux"
PLUGINS_ROOT = "Akeno.plugins"
PLUGINS_ROOT2 = ["Akeno.plugins","Akeno.plugins2"]

riddle_client = Client(
    "ten",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION10,
    plugins=dict(root=PLUGINS_ROOT2),
)

clients.append(riddle_client)

def create_and_append_client(name, session_string):
    if session_string:
        client = Client(
            name,
            app_version=APP_VERSION,
            device_model=DEVICE_MODEL,
            system_version=SYSTEM_VERSION,
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
            plugins=dict(root=PLUGINS_ROOT),
        )
        
        clients.append(client) 


sessions = [
    ("two", SESSION2),
    ("one", SESSION),
    ("three", SESSION3),
    ("four", SESSION4),
    ("five", SESSION5),
    ("six", SESSION6),
    ("sev", SESSION7),
    ("eig", SESSION8),
    ("nin", SESSION9)
    

    
]

for name, session in sessions:
    create_and_append_client(name, session)
