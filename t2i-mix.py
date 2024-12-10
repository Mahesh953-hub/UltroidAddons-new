from . import ultroid_cmd
from telethon import events
import requests
from telethon.tl.types import InputFile
import os

@ultroid_cmd(pattern="tii ?(.*)")
async def text_to_image(event):
    """
    A command to generate an image from text using the Widipe API.
    Usage: /t2i <prompt>
    """
    reply_message = await event.get_reply_message()
    prompt = event.pattern_match.group(1).strip()
    if not prompt and reply_message:
        prompt = reply_message.message
    if not prompt:
        await eor(event, "`Please provide a prompt for image generation!`")
        return
    
    processing_msg = await eor(event, f"🔄 **Generating image for prompt:** `{prompt}`...")
    
    api_paths = ["v1/text2img", "v2/text2img", "v4/text2img", "v5/text2img", "v6/text2img"]

    for idx, path in enumerate(api_paths):
        try:
            api_url = f"https://widipe.com/{path}?text={prompt}"
            response = requests.get(api_url)
            if response.status_code == 200:
                image_path = "generated_image.png"
                with open(image_path, "wb") as file:
                    file.write(response.content)
                    
                caption = f"🖼️ <b>Image successfully generated!</b>\n\n<b>Prompt:</b> <code>{prompt}</code>\n\n<blockquote>©️ @RemainsAlways</blockquote>"
                await event.client.send_file(event.chat_id, image_path, caption=caption, parse_mode="html")
                
                os.remove(image_path)
                await processing_msg.delete()
                return
            else:
                if idx == 0:
                    await processing_msg.edit("`⚠️ Request Failed! Trying Again...`")
        
        except Exception as e:
            if idx == 0:
                await processing_msg.edit("`⚠️ Request Failed! Trying Again...`")
            if idx == len(api_paths) - 1:
                await eor(event, f"**All attempts failed. Unable to generate image.**\nError: `{str(e)}`")
                return
