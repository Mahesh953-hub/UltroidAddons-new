from telethon import events
from . import ultroid_cmd, eor

PRINTABLE_ASCII = range(0x21, 0x7F)

def aesthetify(string):
    for c in string:
        c = ord(c)
        if c in PRINTABLE_ASCII:
            c += 0xFF00 - 0x20
        elif c == ord(" "):
            c = 0x3000
        yield chr(c)


@ultroid_cmd(pattern="ae(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    text = event.pattern_match.group(1)
    text = "".join(aesthetify(text))
    await event.eor(text=text, parse_mode=None, link_preview=False)
    raise events.StopPropagation