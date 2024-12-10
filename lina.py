import re
import json
import requests
from telethon import events
from . import ultroid_cmd, eor

json_objects = []
urls = []

@ultroid_cmd(pattern="lina ?(.*)")
async def get_image(event):
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        prompt = reply.text
    else:
        prompt = event.pattern_match.group(1)
    if not prompt:
        await eor(event, "Please provide a prompt.")
        return
    
    msg = await event.eor("`Processing prompt, please wait...`")
    json_objects.clear()
    urls.clear()

    def getinpt(prompt):
        url = 'https://linaqruf-kivotos-xl-2-0.hf.space/queue/join?'
        headers = {
            'authority': 'linaqruf-kivotos-xl-2-0.hf.space',
            'accept': '*/*',
            'content-type': 'application/json',
            'origin': 'https://linaqruf-kivotos-xl-2-0.hf.space',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        data = {
            "data": [prompt, "nsfw, high quality, 3d, watermark, signature", 673571220, 1024, 1024, 7, 28, "Euler a", "896 x 1152", False, 0.55, 1.5, True],
            "fn_index": 6,
            "trigger_id": 41,
            "session_hash": "19lmlrvpgpb"
        }

        response = requests.post(url, headers=headers, json=data)

        data_url = 'https://linaqruf-kivotos-xl-2-0.hf.space/queue/data?session_hash=19lmlrvpgpb'
        data_headers = {
            'authority': 'linaqruf-kivotos-xl-2-0.hf.space',
            'accept': 'text/event-stream',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        resp = requests.get(data_url, headers=data_headers, stream=True).text

        lines = resp.splitlines()
        for line in lines:
            match = re.search(r'\{.*\}', line)
            if match:
                json_str = match.group(0)
                try:
                    json_obj = json.loads(json_str)
                    json_objects.append(json_obj)
                except json.JSONDecodeError:
                    continue

    def extract_urls(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "url":
                    urls.append(v)
                else:
                    extract_urls(v)
        elif isinstance(obj, list):
            for item in obj:
                extract_urls(item)

    getinpt(prompt)
    for json_obj in json_objects:
        extract_urls(json_obj)

    if urls:
        first_image_url = urls[0]
        source = first_image_url
        # Caption with clickable [SOURCE]
        caption = (
            f"<b>🖼️ Generated Image</b>\n\n"
            f"<b>🌟 Query:</b> <code>{prompt}</code>\n\n"
            f"<b>🎠 Link:</b> <a href='{source}'>Source</a>\n\n"
            "<blockquote>©️ @RemainsAlways</blockquote>"
        )

        await event.client.send_file(
            event.chat_id,
            file=first_image_url,
            caption=caption,
            parse_mode="html",
            reply_to=event.reply_to_msg_id or event.id
        )
        await msg.delete()
    else:
        await msg.edit("`**Error:** No image found.`")