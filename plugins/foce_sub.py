import logging

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user, add_fsub_channel, remove_fsub_channel, get_fsub_channels, enable_fsub, disable_fsub, is_fsub_enabled

logger = logging.getLogger(__name__)

ADMIN_TEXT = "HELLO DEAR!! \n HERE ARE THE LIST OF ADMIN TOOLS!! \n\n /disablefsub - IT IS FOR DISABLING THE FSUB. \n\n /enablesub - ENABLE FORCESUB \n\n /addfsub <CHANNEL_ID> - ADD CHANNEL AS FORCE SUB. \n\n /rmfsub <CHANNEL_ID> - REMOVE CHANNEL AS FORCE SUB. \n\n /listfsub - LIST OF ALL FSUB ADDED." 


@Bot.on_message(filters.command('admin') & filters.private & filters.user(ADMINS))
async def admin_panel(client: Bot, message: Message):
    await message.reply_text(ADMIN_TEXT)
    

@Bot.on_message(filters.command('addfsub') & filters.private & filters.user(ADMINS))
async def add_fsub(client: Bot, message: Message):
    logger.info("Processing /addfsub command")
    try:
        if len(message.command) != 2:
            await message.reply_text("Usage: /addfsub <channel_id>")
            return

        channel_id = int(message.command[1])
        await add_fsub_channel(channel_id)
        await message.reply_text(f"Channel {channel_id} added to forced subscription list.")
        logger.info(f"Channel {channel_id} added to forced subscription list.")
    except Exception as e:
        await message.reply_text(f"Error adding channel: {e}")
        logger.error(f"Error adding channel: {e}")

@Bot.on_message(filters.command('rmfsub') & filters.private & filters.user(ADMINS))
async def rm_fsub(client: Bot, message: Message):
    logger.info("Processing /rmfsub command")
    try:
        if len(message.command) != 2:
            await message.reply_text("Usage: /rmfsub <channel_id>")
            return

        channel_id = int(message.command[1])
        await remove_fsub_channel(channel_id)
        await message.reply_text(f"Channel {channel_id} removed from forced subscription list.")
        logger.info(f"Channel {channel_id} removed from forced subscription list.")
    except Exception as e:
        await message.reply_text(f"Error removing channel: {e}")
        logger.error(f"Error removing channel: {e}")

@Bot.on_message(filters.command('listfsub') & filters.private & filters.user(ADMINS))
async def list_fsub(client: Bot, message: Message):
    logger.info("Processing /listfsub command")
    try:
        channels = await get_fsub_channels()
        if not channels:
            await message.reply_text("No channels in the forced subscription list.")
            return

        channel_list = "\n".join([str(ch) for ch in channels])
        await message.reply_text(f"Forced subscription channels:\n{channel_list}")
        logger.info("Listed forced subscription channels")
    except Exception as e:
        await message.reply_text(f"Error listing channels: {e}")
        logger.error(f"Error listing channels: {e}")

@Bot.on_message(filters.command('enablefsub') & filters.private & filters.user(ADMINS))
async def enable_fsub_command(client: Bot, message: Message):
    logger.info("Processing /enablefsub command")
    try:
        await enable_fsub()
        await message.reply_text("Forced subscription enabled.")
        logger.info("Forced subscription enabled.")
    except Exception as e:
        await message.reply_text(f"Error enabling forced subscription: {e}")
        logger.error(f"Error enabling forced subscription: {e}")

@Bot.on_message(filters.command('disablefsub') & filters.private & filters.user(ADMINS))
async def disable_fsub_command(client: Bot, message: Message):
    logger.info("Processing /disablefsub command")
    try:
        await disable_fsub()
        await message.reply_text("Forced subscription disabled.")
        logger.info("Forced subscription disabled.")
    except Exception as e:
        await message.reply_text(f"Error disabling forced subscription: {e}")
        logger.error(f"Error disabling forced subscription: {e}")

