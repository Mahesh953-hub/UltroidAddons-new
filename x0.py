import logging
from requests import post
import io
from telethon.tl.types import DocumentAttributeFilename
from . import ultroid_cmd, eor

@ultroid_cmd(pattern="x0(?: (.+)|$)")
async def x0cmd(event):
    pre = await event.eor("`Processing...`")
    reply = await event.get_reply_message()
    if not reply:
        await event.eor("`Reply to a message containing media or text.`")
        return
    file = None

    if reply.media:
        if reply.photo:
            file = io.BytesIO(await event.client.download_file(reply.photo))
            file.name = "photo.jpg"
        elif reply.document:
            if any(isinstance(attr, DocumentAttributeFilename) for attr in reply.document.attributes):
                file_name = next(
                    attr.file_name for attr in reply.document.attributes if isinstance(attr, DocumentAttributeFilename)
                )
            else:
                file_name = reply.file.id + reply.file.ext
            
            file = io.BytesIO(await event.client.download_file(reply.document))
            file.name = file_name
    if not file:
        file = io.BytesIO(bytes(reply.raw_text, "utf-8"))
        file.name = "txt.txt"
    
    try:
        x0at = post("https://x0.at", files={"file": file})
        x0at.raise_for_status()
    except Exception as e:
        await event.eor(f"Error: {e}")
        return
    
    url = x0at.text
    ME = (f"<blockquote>©️ @RemainsAlways </blockquote>")
    output = (f"<blockquote><b>Uploaded Succesfully!</b></blockquote>")
    LINK = (f"<blockquote><b> <a href={url}>LINK</a></b></blockquote>")
    await event.eor(f"{output}\n{LINK}\n\n{ME}", parse_mode="html")
    await pre.delete()