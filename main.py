#!/usr/bin/env python3
# A simple script to print some messages.
import time
import re
import json
import random
import os
from asyncio import sleep
from pprint import pprint
import logging

from telethon import TelegramClient, events, utils
from dotenv import load_dotenv

load_dotenv() # get .env variable

session = os.environ.get('TG_SESSION', 'printer')
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
debug_mode = os.getenv("DEBUG_MODE").upper() == "TRUE"
phone_number = os.getenv("PHONE_NUMBER")

proxy = None  # https://github.com/Anorov/PySocks

# Create and start the client so we can make requests (we don't here)
client = TelegramClient(session, api_id, api_hash, proxy=proxy).start()

# create a sender list to check if user already send private message or mention
senderList = [] 

# config for logs
logging.basicConfig(level=logging.INFO, filename="logs.log", filemode='a', format=' %(asctime)s - %(levelname)s - %(message)s')

@client.on(events.NewMessage)
async def handle_new_message(event):
    
    me = await client.get_me()
    sender = await event.get_sender()  # this lookup will be cached by telethon
    to_ = await event.client.get_entity(event.message.to_id)

    message = f"""
        **AUTO REPLY**
        \nHi @{sender.username},
        \nCurrently I decided to take a break from social media, so I'm not available to reply to your message.
        \nPlease be patient, I will reply to your message as soon as possible.
        \nOr you can call me directly at {phone_number}

        \n** Автоответчик **
        \nПривет @{sender.username},
        \nВ настоящее время я решил взять перерыв от социальных сетей, поэтому я не могу ответить на ваше сообщение.
        \nПожалуйста, будьте терпеливы, я отвечу на ваше сообщение как можно скорее.
        \nИли вы можете позвонить мне напрямую по номеру {phone_number}
    """


    needToProceed = sender.is_self if debug_mode else not sender.is_self and (event.is_private or re.search("@"+me.username,event.raw_text))
    if needToProceed:  # only auto-reply to private chats:  # only auto-reply to private chats   
        if not sender.bot and event:  # don't auto-reply to bots
            print(time.asctime(), '-', event.message, sender)  # optionally log time and message
            logging.info(f"Message: {event.message} from: {sender}")
            await sleep(1)  # pause for 1 second to rate-limit automatic replies   
            senderList.append(to_.id)

            await event.reply(message)

client.start()
client.run_until_disconnected()
