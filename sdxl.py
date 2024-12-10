import aiohttp
import asyncio
import os
from . import ultroid_cmd, eor
from telethon import events

@ultroid_cmd(pattern="sdxl ?(.*)")
async def send_generated_image(event):
    prompt = event.pattern_match.group(1).strip()
    if not prompt:
        if event.reply_to_msg_id:
            reply_msg = await event.get_reply_message()
            prompt = reply_msg.text
        else:
            await eor(event, "Please enter the prompt for the image generation:")
            try:
                response = await event.client.wait_for("message", timeout=30, check=lambda e: e.sender_id == event.sender_id)
                prompt = response.text
            except asyncio.TimeoutError:
                await eor(event, "No prompt received. Please try again.")
                return

    msg = await eor(event, "`Generating image, please wait...`")
    try:
        url = "http://104.234.36.24:1337/v1/chat/completions"
        data = {
            "model": "sdxl",
            "stream": False,
            "messages": [
                {"role": "assistant", "content": prompt}
            ]
        }

        # Use async with for aiohttp ClientSession and requests
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    json_response = await response.json()
                    content = json_response["choices"][0]["message"]["content"]
                    image_url = content.split("![Generated image](")[1].split(")")[0]
                else:
                    await msg.edit(f"Error: {response.status}")
                    return
        
        # Check if image URL was retrieved successfully
        if image_url:
            image_path = "sdxl-Image.png"
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as image_response:
                    if image_response.status == 200:
                        # Download the image to a local file
                        with open(image_path, "wb") as image_file:
                            image_file.write(await image_response.read())
                    else:
                        await eor(event, "Failed to download the image.")
                        return
            
            # Send the downloaded image and then delete the local file
            caption = f"<b>🖼️ Genrated Image</b>\n\n<b>🌟 Prompt:</b> <code>{prompt}</code>\n\n <blockquote>©️ @RemainsAlways</blockquote>"
            await event.client.send_file(
                event.chat_id,
                image_path,
                caption=caption,
                parse_mode="html",
                reply_to=event.reply_to_msg_id or event.id
            )
            os.remove(image_path)
            await msg.delete()
        else:
            await msg.edit("`Failed to generate the image. Please try again.`")
    except Exception as e:
        await msg.edit(f"`Unable to send request for image generation.\nError: {e}`")
