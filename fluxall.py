"""
✘ Commands Available

• `{i}fluxr [-p1 or -p2] <prompt>`
    - Genrate A Realistic Image Using Flux-Realism.
    - Details : 
    The Default Value of Image Gen is 9:16 and Seed Value is Random.
        [APPLIED FOR ALL CMDS]
        -p1 : Image Size 4:3
        -p2 : Image Size 16:9

• `{i}fluxa [-p1 or -p2] <prompt>`
    - Genrate A Anime Image Using Flux-Anime.
    
• `{i}flux3d [-p1 or -p2] <prompt>`
    - Genrate A 3D Image Using Flux-3D.
    
• `{i}fluxd [-p1 or -p2] <prompt>`
    - Genrate A Beautiful Fantasy Image Using Flux-Disney.

• `{i}fluxp [-p1 or -p2] <prompt>`
    - Genrate A Pixel Image Using Flux-Pixel.

• `{i}dark [-p1 or -p2] <prompt>`
    - Genrate A Beautiful Image..

"""
MODEL_R = "Flux Realism"
MODEL_A = "Flux Anime"
MODEL_3 = "Flux-3D"
MODEL_D = "Flux Disney"
MODEL_P = "Flux Pixel"

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

@ultroid_cmd(pattern="fluxr ?(.*)")
async def flux_r(event):
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

    msg = await event.eor("🐣")
    # Prepare the API request
    api_url = f"https://api.airforce/imagine2?model=flux-realism&prompt={prompt}&size={size}&seed={seed}"
    
    # Request the image from the API
    try:
        response = requests.get(api_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        await msg.edit(f"❌ Error: {e}")
        return

    # Save and send the image
    image_path = "FluxReal.png"
    with open(image_path, "wb") as file:
        file.write(response.content)

    caption = f"<b>🖼️ Flux Image Generated</b>\n\n<b>🌟 Prompt:</b> <code>{prompt}</code>\n<b>📏 Size:</b> <code>{size}</code> \n <b>🌱 Seed:</b> <code>{seed}</code>\n <b>🐣 Model:</b> <code>{MODEL_R}</code>\n\n<blockquote>©️ @RemainsAlways</blockquote>"
    await event.client.send_file(
        event.chat_id,
        file=image_path,
        caption=caption,
        parse_mode="html",
        reply_to=event.reply_to_msg_id or event.id
    )
    await msg.delete()
    if image_path:
        os.remove(image_path)
    else:
        os.remove("FluxReal.png")
#============================#
#============================#


@ultroid_cmd(pattern="fluxa ?(.*)")
async def flux_anime(event):
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

    msg = await event.eor("🐾")
    # Prepare the API request
    api_url = f"https://api.airforce/imagine2?model=flux-anime&prompt={prompt}&size={size}&seed={seed}"
    
    # Request the image from the API
    try:
        response = requests.get(api_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        await msg.edit(f"❌ Error: {e}")
        return

    # Save and send the image
    image_path = "FluxAnime.png"
    with open(image_path, "wb") as file:
        file.write(response.content)

    caption = f"<b>🖼️ Flux Image Generated</b>\n\n<b>🌟 Prompt:</b> <code>{prompt}</code>\n<b>📏 Size:</b> <code>{size}</code> \n <b>🌱 Seed:</b> <code>{seed}</code>\n <b>🐾 Model:</b> <code>{MODEL_A}</code>\n\n<blockquote>©️ @RemainsAlways</blockquote>"
    await event.client.send_file(
        event.chat_id,
        file=image_path,
        caption=caption,
        parse_mode="html",
        reply_to=event.reply_to_msg_id or event.id
    )
    await msg.delete()
    if image_path:
        os.remove(image_path)
    else:
        os.remove("FluxAnime.png")
#============================#
#============================#


@ultroid_cmd(pattern="flux3d ?(.*)")
async def flux3d(event):
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

    msg = await event.eor("🌱")
    # Prepare the API request
    api_url = f"https://api.airforce/imagine2?model=flux-3d&prompt={prompt}&size={size}&seed={seed}"
    
    # Request the image from the API
    try:
        response = requests.get(api_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        await msg.edit(f"❌ Error: {e}")
        return

    # Save and send the image
    image_path = "Flux3D.png"
    with open(image_path, "wb") as file:
        file.write(response.content)

    caption = f"<b>🖼️ Flux Image Generated</b>\n\n<b>🌟 Prompt:</b> <code>{prompt}</code>\n<b>📏 Size:</b> <code>{size}</code> \n <b>🌱 Seed:</b> <code>{seed}</code>\n <b>🐧 Model:</b> <code>{MODEL_3}</code>\n\n<blockquote>©️ @RemainsAlways</blockquote>"
    await event.client.send_file(
        event.chat_id,
        file=image_path,
        caption=caption,
        parse_mode="html",
        reply_to=event.reply_to_msg_id or event.id
    )
    await msg.delete()
    if image_path:
        os.remove(image_path)
    else:
        os.remove("Flux3D.png")
#============================#
#============================#

@ultroid_cmd(pattern="fluxd ?(.*)")
async def flux_disney(event):
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

    msg = await event.eor("✨")
    # Prepare the API request
    api_url = f"https://api.airforce/imagine2?model=flux-disney&prompt={prompt}&size={size}&seed={seed}"
    
    # Request the image from the API
    try:
        response = requests.get(api_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        await msg.edit(f"❌ Error: {e}")
        return

    # Save and send the image
    image_path = "FluxDisney.png"
    with open(image_path, "wb") as file:
        file.write(response.content)

    caption = f"<b>🖼️ Flux Image Generated</b>\n\n<b>🌟 Prompt:</b> <code>{prompt}</code>\n<b>📏 Size:</b> <code>{size}</code> \n <b>🌱 Seed:</b> <code>{seed}</code>\n <b>🦚 Model:</b> <code>{MODEL_D}</code>\n\n<blockquote>©️ @RemainsAlways</blockquote>"
    await event.client.send_file(
        event.chat_id,
        file=image_path,
        caption=caption,
        parse_mode="html",
        reply_to=event.reply_to_msg_id or event.id
    )
    await msg.delete()
    if image_path:
        os.remove(image_path)
    else:
        os.remove("FluxDisney.png")
#============================#
#============================#


@ultroid_cmd(pattern="fluxp ?(.*)")
async def flux_pixel(event):
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

    msg = await event.eor("👾")
    # Prepare the API request
    api_url = f"https://api.airforce/imagine2?model=flux-pixel&prompt={prompt}&size={size}&seed={seed}"
    
    # Request the image from the API
    try:
        response = requests.get(api_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        await msg.edit(f"❌ Error: {e}")
        return

    # Save and send the image
    image_path = "FluxPixel.png"
    with open(image_path, "wb") as file:
        file.write(response.content)

    caption = f"<b>🖼️ Flux Image Generated</b>\n\n<b>🌟 Prompt:</b> <code>{prompt}</code>\n<b>📏 Size:</b> <code>{size}</code> \n <b>🌱 Seed:</b> <code>{seed}</code>\n <b>👾 Model:</b> <code>{MODEL_P}</code>\n\n<blockquote>©️ @RemainsAlways</blockquote>"
    await event.client.send_file(
        event.chat_id,
        file=image_path,
        caption=caption,
        parse_mode="html",
        reply_to=event.reply_to_msg_id or event.id
    )
    await msg.delete()
    if image_path:
        os.remove(image_path)
    else:
        os.remove("FluxPixel.png")
#============================#
#============================#

@ultroid_cmd(pattern="dark ?(.*)")
async def any_dark(event):
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

    msg = await event.eor("🎈")
    # Prepare the API request
    api_url = f"https://api.airforce/imagine2?model=any-dark&prompt={prompt}&size={size}&seed={seed}"
    
    # Request the image from the API
    try:
        response = requests.get(api_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        await msg.edit(f"❌ Error: {e}")
        return

    # Save and send the image
    image_path = "Dark_Image.png"
    with open(image_path, "wb") as file:
        file.write(response.content)

    caption = f"<b>🖼️ Image Generated</b>\n\n<b>🌟 Prompt:</b> <code>{prompt}</code>\n<b>📏 Size:</b> <code>{size}</code> \n <b>🌱 Seed:</b> <code>{seed}</code>\n\n<blockquote>©️ @RemainsAlways</blockquote>"
    await event.client.send_file(
        event.chat_id,
        file=image_path,
        caption=caption,
        parse_mode="html",
        reply_to=event.reply_to_msg_id or event.id
    )
    await msg.delete()
    if image_path:
        os.remove(image_path)
    else:
        os.remove("Dark_Image.png")
    
#============================#
#============================#

