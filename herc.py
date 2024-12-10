import requests
import os
from . import ultroid_cmd, eor

BASE_URL = "https://hercai.onrender.com/v3/hercai"

@ultroid_cmd(pattern="herc ?(.*)")
async def herc_ai(event):
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        prompt = reply.text
    else:
        prompt = event.pattern_match.group(1)

    if not prompt:
        await event.eor("`Please Give Me Prompt Or Reply To A Message!`")
        return
    
    msg = await event.eor("⚡")
    try:
        params={"question" : prompt}
        response = requests.get(BASE_URL, params=params, timeout=30).json()
        result = response["reply"]
        if len(result) > 4096:
            file_path = "Herc.txt"
            with open(file_path, "r", encoding="utf-8") as f:
                f.write(result)
            await event.client.send_file(
                event.chat_id,
                file=file_path,
                caption="**Response Chars Limit Exceeded. Sent As file**",
                reply_to=event.reply_to_msg_id or event.id
            )
            
            if file_path:
                os.remove(file_path)
            else:
                os.remove("Herc.txt")
        else:
            await msg.edit(f"__Query__ : `{prompt}`\n\n__Response__ : {result}")
    except requests.Timeout:
        await msg.edit("`Request TimedOut!`")
    except Exception as e:
        await msg.edit(f"`An Error Occurred : \n {e}`")