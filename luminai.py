import aiohttp
import asyncio
import json,os
from . import ultroid_cmd

API_URL = "https://luminai.my.id/"

async def tanya(text):
    payload = {
        "content": text
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json;charset=UTF-8",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{API_URL}",
                headers=headers,
                data=json.dumps(payload),
            ) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Error: {response.status}, {await response.text()}")
                    return None
    except aiohttp.ClientError as e:
        await print(f"Request error: {str(e)}")
        return None

@ultroid_cmd(pattern="asg(?: (.*))?$")
async def asg_handler(event):
    # Pre-message while processing
    msg = await event.eor("`Processing request...`", parse_mode="markdown")
    
    # Fetching user input from reply or message
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        prompt = reply.text
    else:
        prompt = event.pattern_match.group(1)
    
    # Check if user provided the input
    if not prompt:
        await msg.edit("`Gib Prompt or Remply to Message sarr!!!`", parse_mode="markdown")
        return

    try:
        hasil = await tanya(prompt)

        # Check if the response exceeds Telegram's character limit
        if len(hasil) > 4095:
            file_path = "asg_response.txt"
            with open(file_path, "w", encoding="utf-8") as out_file:
                out_file.write(hasil)

            # Send the file and delete the initial processing message
            await event.client.send_file(
                event.chat_id,
                file_path,
                caption="**Response Exceeded Limits. Sending as File.**",
                parse_mode="markdown"
            )
            await msg.delete()
        else:
            # Send the response if within limits
            await msg.edit(f"**Response:**\n\n{hasil}", parse_mode="markdown")
    except Exception as e:
        await msg.edit(f"`An Error Occurred: {str(e)}`", parse_mode="markdown")