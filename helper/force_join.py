from pyrogram import Client
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import InlineKeyboardButton as ikb
from pyrogram.types import InlineKeyboardMarkup as ikm

from database.force_join_db import FSUBS
from database.pending_request_db import REQUESTED_USERS
from vars import BOT_USERNAME, FORCE_SUB


def add_force_sub():
    if not FORCE_SUB:
        return

    fsub = FSUBS()
    for i in FORCE_SUB:
        fsub.inser_fsub(int(i))

    print(f"Added {len(FORCE_SUB)} channel in database")
    return


async def add_one_fsub(chat):
    FSUBS().inser_fsub(chat)
    return


async def get_all_force_sub():
    fsub = FSUBS()
    channels = fsub.get_fsubs()
    return channels


async def remove_all_force_sub():
    FSUBS().remove_all()
    return


async def remove_one(channel_id):
    FSUBS().remove_fsub(channel_id)
    return


async def genrate_fsub_kb(c: Client, data="start"):
    all_fsubs = await get_all_force_sub()
    btns = []
    for i, j in enumerate(all_fsubs):
        i += 1
        chat_type = bool((await c.get_chat(int(j))).username)
        invite_link = await c.create_chat_invite_link(int(j), creates_join_request=chat_type)
        btns.append(ikb(f"Join channel {i}", url=invite_link.invite_link))

    kb = [btns[i:i+3] for i in range(0, len(btns), 3)]
    kb.append([(ikb("Get The File", url=f"t.me/{BOT_USERNAME}?start={data}"))])

    return ikm(kb)


async def check_fsub(c: Client, user):
    all_fsubs = await get_all_force_sub()
    if not all_fsubs:
        return False

    for i in all_fsubs:
        try:
            chat_user = await c.get_chat_member(i, user)
            if chat_user.status in [CMS.ADMINISTRATOR, CMS.MEMBER, CMS.OWNER]:
                continue
            else:
                reqq = REQUESTED_USERS(i).get_pending_users(user)
                if not reqq:
                    return True
        except:
            reqq = REQUESTED_USERS(i).get_pending_users(user)
            if not reqq:
                return True
    return False
