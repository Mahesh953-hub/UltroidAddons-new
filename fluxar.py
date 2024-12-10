"""
✘ Commands Available

• `{i}flux [-p1 or -p2] <query>`
    Genrate A Beautiful Image Using Flux.
    Details : 
    The Default Value of Image Gen is 9:16 and Seed Value is Random.
    
        -p1 : Image Size 4:3
        -p2 : Image Size 16:9
"""


import requests
import random
from telethon.tl.types import InputMessagesFilterPhotos
from . import ultroid_cmd
import os

# Helper constants for aspect ratios
SIZE_MAP = {
    "-p1": "4:3",
    "-p2": "16:9",
}

@ultroid_cmd(pattern="flx(.*)")
async def flux(event):
    args = event.pattern_match.group(1).split()
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        prompt = reply.text
    else:
        prompt = args
    seed = random.randint(1, 100)  # Default random seed
    size = "9:16"  # Default size
    prompt = ""

    # Check for flags and construct the prompt
    for arg in args:
        if arg in SIZE_MAP:
            size = SIZE_MAP[arg]
        else:
            prompt += f"{arg} "

    # Use a default prompt if none is provided
    prompt = prompt.strip() 
    if not prompt:
        await event.eor("Please Provide Prompt Or Reply To Message")

    msg = await event.eor("⚡")
    # Prepare the API request
    api_url = f"https://api.airforce/imagine2?model=flux&prompt={prompt}&size={size}&seed={seed}"
    
    # Request the image from the API
    try:
        response = requests.get(api_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        await msg.edit(f"❌ Error: {e}")
        return

    # Save and send the image
    image_path = "flux_image.jpg"
    with open(image_path, "wb") as file:
        file.write(response.content)

    caption = f"<b>🖼️ Flux Image Generated</b>\n\n<b>🌟 Prompt:</b> <code>{prompt}</code>\n<b>📏 Size:</b> <code>{size}</code> \n <b>🌱 Seed:</b> <code>{seed}</code>\n\n<blockquote>©️ @RemainsAlways</blockquote>"
    await event.client.send_file(
        event.chat_id,
        file=image_path,
        caption=caption,
        parse_mode="html",
        reply_to=event.reply_to_msg_id or event.id
    )
    await msg.delete()
    await os.remove(image_path)
