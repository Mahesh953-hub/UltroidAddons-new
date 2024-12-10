import os
import json
import requests
from . import ultroid_cmd

@ultroid_cmd(pattern="bbxp ?(.*)")
async def bbx_pro(e):
    args = e.pattern_match.group(1)
    if not args and not e.is_reply:
         return await e.reply("Please provide a prompt or reply to a message.")  
    if e.is_reply:
        reply_msg = await e.get_reply_message()
        args = reply_msg.text
        
    prompt = args

    try:
        url = "http://104.234.36.24:1337/v1/chat/completions"
        headers = {
            "User-Agent": "Python/requests",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip"
        }
        payload = {
            "model": "blackboxai-pro",
            "stream": False,
            "messages": [
                    {"role": "assistant", "content": prompt}
            ]
        }
        
        msg = await e.eor("✨")
        response = requests.post(url, headers=headers, data=json.dumps(payload)).json().get('choices', [])
        for choice in response:
            resp = choice.get('message', {}).get('content' '')
        if len(resp) > 4095:
            # Save the response as a text file
            file_path = "bbxp.txt"
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(resp)
            await event.client.send_file(
                event.chat_id,
                file_path,
                caption="**Response exceeded limits, Sending as file.**",
                parse_mode="markdown"
            )
            os.remove("bbxp.txt")
            await msg.delete()
        #print(choice.get('message', {}).get('content', ''))
        else:
            await msg.edit(resp, parse_mode="markdown")
    except Exception as exc:
        await msg.edit(f"Error: {exc}")