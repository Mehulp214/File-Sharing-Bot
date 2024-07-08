# from pyrogram import Client, filters
# from pyrogram.types import Message


# from database.users_db import USERS
# from helper.force_join import *
# from vars import OWNER_ID

# owner_filt = filters.user(OWNER_ID)


# @Client.on_message(filters.command("addfsub") & owner_filt)
# async def add_new_force_sub(c: Client, m: Message):
#     if len(m.command) != 2:
#         await m.reply_text("Usage\n /addfsub [channel id]")
#         return
#     try:
#         channel = int(m.command[1])
#     except ValueError:
#         await m.reply_text("Channel id should be integer")
#         return
#     await add_one_fsub(channel)
#     await m.reply_text("Added channel to force sub")
#     return


# @Client.on_message(filters.command("rmfsub") & owner_filt)
# async def rm_force_subs(_, m: Message):
#     if len(m.command) != 2:
#         await m.reply_text("Usage\n /rmfsub [channel id | all]: Pass all to remove all channels from fsubs")
#         return

#     if m.command[1].lower() == "all":
#         await remove_all_force_sub()
#         await m.reply_text("Removed all channels from force sub")
#         return
#     try:
#         channel = int(m.command[1])
#     except ValueError:
#         await m.reply_text("Channel id should be integer")
#         return

#     await remove_one(channel)
#     await m.reply_text("Removed channel from force sub")
#     return


# @Client.on_message(filters.command("getfsub") & owner_filt)
# async def get_curr_fsubs(_, m: Message):
#     all_channels = await get_all_force_sub()

#     if not all_channels:
#         await m.reply_text("No channel found in force sub")
#         return

#     txt = "Here are channels in foce sub\n\n"
#     for i, j in enumerate(all_channels):
#         i += 1
#         txt += f"{i}. {j}"

#     await m.reply_text(txt)
#     return


import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user, add_fsub_channel, remove_fsub_channel, get_fsub_channels, enable_fsub, disable_fsub, is_fsub_enabled
@Bot.on_message(filters.private & filters.command('addfsub') & filters.user(ADMINS))
async def add_fsub(client: Bot, message: Message):
    try:
        if len(message.command) != 2:
            await message.reply_text("Usage: /addfsub <channel_id>")
            return

        channel_id = int(message.command[1])
        await add_fsub_channel(channel_id)
        await message.reply_text(f"Channel {channel_id} added to forced subscription list.")
    except Exception as e:
        await message.reply_text(f"Error adding channel: {e}")
        print(f"Error adding channel: {e}")

@Bot.on_message(filters.private & filters.command('rmfsub') & filters.user(ADMINS))
async def rm_fsub(client: Bot, message: Message):
    try:
        if len(message.command) != 2:
            await message.reply_text("Usage: /rmfsub <channel_id>")
            return

        channel_id = int(message.command[1])
        await remove_fsub_channel(channel_id)
        await message.reply_text(f"Channel {channel_id} removed from forced subscription list.")
    except Exception as e:
        await message.reply_text(f"Error removing channel: {e}")
        print(f"Error removing channel: {e}")

@Bot.on_message(filters.private & filters.command('listfsub') & filters.user(ADMINS))
async def list_fsub(client: Bot, message: Message):
    try:
        channels = await get_fsub_channels()
        if not channels:
            await message.reply_text("No channels in the forced subscription list.")
            return

        channel_list = "\n".join([str(ch) for ch in channels])
        await message.reply_text(f"Forced subscription channels:\n{channel_list}")
    except Exception as e:
        await message.reply_text(f"Error listing channels: {e}")
        print(f"Error listing channels: {e}")

@Bot.on_message(filters.private & filters.command('enablefsub') & filters.user(ADMINS))
async def enable_fsub_command(client: Bot, message: Message):
    try:
        await enable_fsub()
        await message.reply_text("Forced subscription enabled.")
    except Exception as e:
        await message.reply_text(f"Error enabling forced subscription: {e}")
        print(f"Error enabling forced subscription: {e}")

@Bot.on_message(filters.private & filters.command('disablefsub') & filters.user(ADMINS))
async def disable_fsub_command(client: Bot, message: Message):
    try:
        await disable_fsub()
        await message.reply_text("Forced subscription disabled.")
    except Exception as e:
        await message.reply_text(f"Error disabling forced subscription: {e}")
        print(f"Error disabling forced subscription: {e}")
