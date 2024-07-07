from pyrogram import Client, filters
from pyrogram.types import Message


from database.users_db import USERS
from helper.force_join import *
from vars import OWNER_ID

owner_filt = filters.user(OWNER_ID)


@Client.on_message(filters.command("addfsub") & owner_filt)
async def add_new_force_sub(c: Client, m: Message):
    if len(m.command) != 2:
        await m.reply_text("Usage\n /addfsub [channel id]")
        return
    try:
        channel = int(m.command[1])
    except ValueError:
        await m.reply_text("Channel id should be integer")
        return
    await add_one_fsub(channel)
    await m.reply_text("Added channel to force sub")
    return


@Client.on_message(filters.command("rmfsub") & owner_filt)
async def rm_force_subs(_, m: Message):
    if len(m.command) != 2:
        await m.reply_text("Usage\n /rmfsub [channel id | all]: Pass all to remove all channels from fsubs")
        return

    if m.command[1].lower() == "all":
        await remove_all_force_sub()
        await m.reply_text("Removed all channels from force sub")
        return
    try:
        channel = int(m.command[1])
    except ValueError:
        await m.reply_text("Channel id should be integer")
        return

    await remove_one(channel)
    await m.reply_text("Removed channel from force sub")
    return


@Client.on_message(filters.command("getfsub") & owner_filt)
async def get_curr_fsubs(_, m: Message):
    all_channels = await get_all_force_sub()

    if not all_channels:
        await m.reply_text("No channel found in force sub")
        return

    txt = "Here are channels in foce sub\n\n"
    for i, j in enumerate(all_channels):
        i += 1
        txt += f"{i}. {j}"

    await m.reply_text(txt)
    return
