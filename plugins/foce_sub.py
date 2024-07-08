# import logging

# from pyrogram import filters
# from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
# from bot import Bot
# from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
# from helper_func import subscribed, encode, decode, get_messages
# from database.database import add_user, del_user, full_userbase, present_user, add_fsub_channel, remove_fsub_channel, get_fsub_channels, enable_fsub, disable_fsub, is_fsub_enabled

# logger = logging.getLogger(__name__)

# @Bot.on_message(filters.command('addfsub') & filters.private & filters.user(ADMINS))
# async def add_fsub(client: Bot, message: Message):
#     logger.info("Processing /addfsub command")
#     try:
#         if len(message.command) != 2:
#             await message.reply_text("Usage: /addfsub <channel_id>")
#             return

#         channel_id = int(message.command[1])
#         await add_fsub_channel(channel_id)
#         await message.reply_text(f"Channel {channel_id} added to forced subscription list.")
#         logger.info(f"Channel {channel_id} added to forced subscription list.")
#     except Exception as e:
#         await message.reply_text(f"Error adding channel: {e}")
#         logger.error(f"Error adding channel: {e}")

# @Bot.on_message(filters.command('rmfsub') & filters.private & filters.user(ADMINS))
# async def rm_fsub(client: Bot, message: Message):
#     logger.info("Processing /rmfsub command")
#     try:
#         if len(message.command) != 2:
#             await message.reply_text("Usage: /rmfsub <channel_id>")
#             return

#         channel_id = int(message.command[1])
#         await remove_fsub_channel(channel_id)
#         await message.reply_text(f"Channel {channel_id} removed from forced subscription list.")
#         logger.info(f"Channel {channel_id} removed from forced subscription list.")
#     except Exception as e:
#         await message.reply_text(f"Error removing channel: {e}")
#         logger.error(f"Error removing channel: {e}")

# @Bot.on_message(filters.command('listfsub') & filters.private & filters.user(ADMINS))
# async def list_fsub(client: Bot, message: Message):
#     logger.info("Processing /listfsub command")
#     try:
#         channels = await get_fsub_channels()
#         if not channels:
#             await message.reply_text("No channels in the forced subscription list.")
#             return

#         channel_list = "\n".join([str(ch) for ch in channels])
#         await message.reply_text(f"Forced subscription channels:\n{channel_list}")
#         logger.info("Listed forced subscription channels")
#     except Exception as e:
#         await message.reply_text(f"Error listing channels: {e}")
#         logger.error(f"Error listing channels: {e}")

# @Bot.on_message(filters.command('enablefsub') & filters.private & filters.user(ADMINS))
# async def enable_fsub_command(client: Bot, message: Message):
#     logger.info("Processing /enablefsub command")
#     try:
#         await enable_fsub()
#         await message.reply_text("Forced subscription enabled.")
#         logger.info("Forced subscription enabled.")
#     except Exception as e:
#         await message.reply_text(f"Error enabling forced subscription: {e}")
#         logger.error(f"Error enabling forced subscription: {e}")

# @Bot.on_message(filters.command('disablefsub') & filters.private & filters.user(ADMINS))
# async def disable_fsub_command(client: Bot, message: Message):
#     logger.info("Processing /disablefsub command")
#     try:
#         await disable_fsub()
#         await message.reply_text("Forced subscription disabled.")
#         logger.info("Forced subscription disabled.")
#     except Exception as e:
#         await message.reply_text(f"Error disabling forced subscription: {e}")
#         logger.error(f"Error disabling forced subscription: {e}")

 import logging

 from pyrogram import filters
 from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
 from bot import Bot
 from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
 from helper_func import subscribed, encode, decode, get_messages
 from database.database import add_user, del_user, full_userbase, present_user, add_fsub_channel, remove_fsub_channel, get_fsub_channels, enable_fsub, disable_fsub, is_fsub_enabled

@Bot.on_message(filters.command('adminpanel') & filters.private & filters.user(ADMINS))
async def admin_panel(client: Bot, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Add FSub Channel", callback_data="add_fsub"),
         InlineKeyboardButton("Remove FSub Channel", callback_data="rm_fsub")],
        [InlineKeyboardButton("List FSub Channels", callback_data="list_fsub")],
        [InlineKeyboardButton("Enable FSub", callback_data="enable_fsub"),
         InlineKeyboardButton("Disable FSub", callback_data="disable_fsub")]
    ])
    await message.reply_text("Admin Panel:", reply_markup=keyboard)

@Bot.on_callback_query(filters.regex("add_fsub"))
async def on_add_fsub(client: Bot, query: CallbackQuery):
    await query.message.reply_text("Please send the channel ID to add to the forced subscription list:")
    client.waiting_for_channel_id = "add_fsub"
    await query.answer()

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.reply)
async def handle_channel_id(client: Bot, message: Message):
    if getattr(client, "waiting_for_channel_id", None) == "add_fsub":
        try:
            channel_id = int(message.text)
            add_fsub_channel(channel_id)
            await message.reply_text(f"Channel {channel_id} added to the forced subscription list.")
            client.waiting_for_channel_id = None
        except ValueError:
            await message.reply_text("Invalid channel ID. Please send a valid channel ID.")
        except Exception as e:
            await message.reply_text(f"Error adding channel: {e}")
            logger.error(f"Error adding channel: {e}")

@Bot.on_callback_query(filters.regex("rm_fsub"))
async def on_rm_fsub(client: Bot, query: CallbackQuery):
    await query.message.reply_text("Please send the channel ID to remove from the forced subscription list:")
    client.waiting_for_channel_id = "rm_fsub"
    await query.answer()

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.reply)
async def handle_channel_id(client: Bot, message: Message):
    if getattr(client, "waiting_for_channel_id", None) == "rm_fsub":
        try:
            channel_id = int(message.text)
            remove_fsub_channel(channel_id)
            await message.reply_text(f"Channel {channel_id} removed from the forced subscription list.")
            client.waiting_for_channel_id = None
        except ValueError:
            await message.reply_text("Invalid channel ID. Please send a valid channel ID.")
        except Exception as e:
            await message.reply_text(f"Error removing channel: {e}")
            logger.error(f"Error removing channel: {e}")

@Bot.on_callback_query(filters.regex("list_fsub"))
async def on_list_fsub(client: Bot, query: CallbackQuery):
    try:
        channels = get_fsub_channels()
        if not channels:
            await query.message.edit_text("No channels in the forced subscription list.")
        else:
            channel_list = "\n".join([str(ch) for ch in channels])
            await query.message.edit_text(f"Forced subscription channels:\n{channel_list}")
    except Exception as e:
        await query.message.edit_text(f"Error listing channels: {e}")
        logger.error(f"Error listing channels: {e}")
    await query.answer()

@Bot.on_callback_query(filters.regex("enable_fsub"))
async def on_enable_fsub(client: Bot, query: CallbackQuery):
    try:
        enable_fsub()
        await query.message.edit_text("Forced subscription enabled.")
    except Exception as e:
        await query.message.edit_text(f"Error enabling forced subscription: {e}")
        logger.error(f"Error enabling forced subscription: {e}")
    await query.answer()

@Bot.on_callback_query(filters.regex("disable_fsub"))
async def on_disable_fsub(client: Bot, query: CallbackQuery):
    try:
        disable_fsub()
        await query.message.edit_text("Forced subscription disabled.")
    except Exception as e:
        await query.message.edit_text(f"Error disabling forced subscription: {e}")
        logger.error(f"Error disabling forced subscription: {e}")
    await query.answer()

