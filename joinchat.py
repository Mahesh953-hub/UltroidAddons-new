# • Made by @e3ris for Ultroid •
# • https://github.com/TeamUltroid/Ultroid •


"""
✘ **Join any Chat**
  ••  `{i}joinchat <username/link>`
"""

from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError
from telethon.tl.types import (
    MessageEntityMention,
    MessageEntityUrl
)

from . import *


@ultroid_cmd(
    pattern="joinchat ?(.*)",
    fullsudo=True,
)
async def let_me_innn(e):
    reply = await e.get_reply_message()
    args = e.pattern_match.group(1)
    if not args and not reply:
        await eod(e, "`Where Should I join, Master Wayne?`")
        return

    eris = await eor(e, "`Processing ..`")
    msg = e if args else reply
    txt = msg.get_entities_text()
    if len(txt) == 0:
        await eod(eris, "`Give me a Valid link, Master Wayne!`")
        return
    ent, link = txt[0]
    if isinstance(ent, MessageEntityUrl):
        try:
            await e.client(ImportChatInviteRequest(
                link.split("/")[-1]
            ))
            await eris.edit("**Successfully Joined the Chat!**")
        except UserAlreadyParticipantError:
            await eris.edit("`You're already in this Chat!`")
            return
        except Exception as ex:
            await eris.edit(f"`#ERROR : {ex}`")
            return

    elif isinstance(ent, MessageEntityMention):
        try:
            await e.client.join_chat(link)
            await eris.edit(f"**Successfully Joined** - `{link}` !!")
        except Exception as ex:
            await eris.edit(f"`#ERROR : {ex}`")
    else:
        await eod(eris, "`Link seems to be Invalid` 🤷‍♀️")
        return
