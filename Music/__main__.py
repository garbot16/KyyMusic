import asyncio
import time
import uvloop
import importlib
from pyrogram import Client
from Music.config import API_ID, API_HASH, BOT_TOKEN, MONGO_DB_URI, SUDO_USERS, LOG_GROUP_ID, AUTO_LEAVE
from Music import BOT_NAME, ASSNAME, app, client
from Music.MusicUtilities.database.functions import clean_restart_stage
from Music.MusicUtilities.database.queue import (get_active_chats, remove_active_chat)
from Music.MusicUtilities.tgcallsrun import run
from Music.MusicUtilities.helpers.decorators import nothingmuch as startapp
from pytgcalls import idle
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import time
import pytz
from pytz import utc
from Music.MusicUtilities.helpers.autoleave import leave_from_inactive_call
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()

Client(
    ':Music:',
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins={'root': 'Music.Plugins'},
).start()


print(f"[INFO]: BOT STARTED AS {BOT_NAME}!")
print(f"[INFO]: ASSISTANT STARTED AS {ASSNAME}!")

print("[INFO]: STARTED BOT AND SENDING THE INFO TO SERVER")
    if AUTO_LEAVE:
        print("[ INFO ] STARTING SCHEDULER")
        scheduler.configure(timezone=pytz.utc)
        scheduler.add_job(
            leave_from_inactive_call, "interval", seconds=AUTO_LEAVE
        )
        scheduler.start()

async def load_start():
    restart_data = await clean_restart_stage()
    if restart_data:
        print("[INFO]: SENDING RESTART STATUS")
        try:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**Restarted the Bot Successfully.**",
            )
        except Exception:
            pass
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        print("Error came while clearing db")
    for served_chat in served_chats:
        try:
            await remove_active_chat(served_chat)                                         
        except Exception as e:
            print("Error came while clearing db")
            pass     
    await startapp()
    await app.send_message(LOG_GROUP_ID, "Bot Started")
    await client.send_message(LOG_GROUP_ID, "Assistant Started")
    print("[INFO]: STARTED")
    
   
loop = asyncio.get_event_loop()
loop.run_until_complete(load_start())

run()
idle()
loop.close()

print("[LOG] CLOSING BOT")
