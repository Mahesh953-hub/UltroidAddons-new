import os
import aiohttp
import random
import asyncio
import json
import io
from curl_cffi.requests import AsyncSession
from . import ultroid_cmd, eor
from PIL import Image

API_URL = "https://api.sexy.ai"
SESS_ID = "77e75caf-527e-4c9a-8b71-88c85a4e198a"
Engines = ["Grounded Realistic Mix.safetensors","Hassaku Hentai.safetensors","Lazymix Real Amateur.safetensors","Porn Ultimate.safetensors","Hentai V2.safetensors","Latex Vision.safetensors","Epic Natural.safetensors","Hardcore Hentai 1.3.safetensors","Pina Colada Furry Mix.safetensors","Futanari Diffusion.safetensors","Realistic Vision.safetensors","Seel Real Furry 4.93.safetensors","Experience.safetensors","Homoerotic.safetensors","Coconut Furry Mix.safetensors","Anime Characters.safetensors","Photon.safetensors","Porn Cartoon.safetensors","Manly Nudes.safetensors","Ultra Real Porn.safetensors","CyberRealistic Revamp.safetensors","Homoerotic - Unstable.safetensors","Pony Diffusion SD.safetensors","Epic Photo.safetensors","Abyss Orange Mix2 NSFW.safetensors","Persika Furry Realism.safetensors","Real Cartoon 3D.safetensors","Real Dream.safetensors","Toon Universe.safetensors","Art Universe.safetensors","Blowbang Ultimate.safetensors","Chillout Mix.safetensors","Clear Bondage.safetensors","Dreamshaper.safetensors","Dreamshaper Pixel Art.safetensors","Anime Furry.safetensors","Gay Diffusion.safetensors"]

@ultroid_cmd(pattern="seai ?(.*)")
async def se_ai(event):
    reply = await event.get_reply_message()
    args = event.pattern_match.group(1) if not reply else reply.message
    if not args:
        await event.reply("`Please Provide Prompt Or Reply To Prompt Message.`")
        return

    negative_prompt = None
    engine = None
    main_prompt = args.split("-n")[0].strip()
    if "-n" in args:
        negative_prompt = args.split("-n")[1].split("-")[0].strip()
    if "-e" in args:
        engine = args.split("-e")[1].split("-")[0].strip()
    else:
        engine = random.choice(Engines)       

    msg = await event.eor("`Generating Image...`")

    async def get_user(session, SESS_ID):
        get_user_url = f"{API_URL}/getSelfUser"
        params = {
            "sessionID": SESS_ID,
            "isAtLeast18Confirmed": "true",
            "profilePicture": "true",
            "extendedPriceInfo": "true"
        }
        response = await session.get(get_user_url, params=params)
        if response.status_code == 200:
            data = response.json
            return data
        else:
            await msg.reply(f"Error fetching user info: {response.status_code}")
            return None
        
    async def get_response(main_prompt, negative_prompt, engine):
        async with AsyncSession(impersonate="chrome107") as session:
            self_user_data = await get_user(session, SESS_ID)
            if self_user_data is None:
                await msg.reply("`Unable to Get Self User Data`")
                return

            headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Content-Type": "text/plain;charset=UTF-8",
                "Origin": "https://sexy.ai",
                "Referer": "https://sexy.ai/",
                "Sec-Ch-Ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"macOS"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            }
            data = {
                "modelName": engine,
                "folderID": "",
                "prompt": main_prompt,
                "negprompt": negative_prompt,
                "restoreFaces": True,
                "sessionID": SESS_ID,
                "width": 736,
                "height": 768,
                "steps": 25,
                "seed": -1,
                "subseed": 0,
                "subseed_strength": 0,
                "sampler": "DPM++ 2M Karras",
                "cfgscale": 7,
            }

           # await msg.edit("`Submitting image generation request...`")
            response = await session.post(f"{API_URL}/generateImage", headers=headers, json=data)
            response_data = json.loads(response.text)
            if "hasError" in response_data and response_data["hasError"]:
                await msg.reply(f"`Error in prompt or negative prompt. {response_data}")
                return None
                

            image_id = response_data.get("payload", {}).get("imageID")
            if not image_id:
                await msg.reply("`Failed to get image ID from response.`")
                return None
            
            await msg.edit("`Image generation in progress...`")
            return await check_image_status(session, image_id, headers)

    async def check_image_status(session, image_id, headers):
        time_counter = 0
        max_retries = 30  # Timeout limit (12 * 2 seconds = 24 seconds)

        while time_counter < max_retries:
            await asyncio.sleep(3)
            response = await session.get(f"{API_URL}/getItemStatus?imageID={image_id}&sessionID={SESS_ID}", headers=headers)
            response_data = json.loads(response.text)
            status = response_data.get("payload", {}).get("status", "pending")
            statuss =status = response_data.get("payload", {}).get("status")

        # Check if status is "complete"
            if status == "complete":
                image_url = response_data.get("payload", {}).get("url")
                if image_url:
                # Download and convert the image to PNG
                    async with aiohttp.ClientSession() as download_session:
                        async with download_session.get(image_url) as resp:
                            if resp.status == 200:
                                image_data = await resp.read()
                                image = Image.open(io.BytesIO(image_data)).convert("RGB")
                                png_image_path = "GenratedImage.png"
                                image.save(png_image_path, "PNG")

                            # Send the PNG image to Telegram
                                #await msg.reply(file=png_image_path)

                            # Clean up the saved file after sending
                                #os.remove(png_image_path)
                                await msg.edit("`Image Has Been Saved! Uploading...`")
                                return png_image_path
                            else:
                                await msg.reply("`Failed to download the image.`")
                                return None
                else:
                    await msg.reply("`Image URL not found. Generation failed.`")
                    return None
        
        # Status is still "generating" or "pending"
            try:
                await msg.edit("`Image is still generating. Checking again in 2 seconds...`")
            except:
                pass
            await asyncio.sleep(3)
            time_counter += 1

    # Timeout reached
        await msg.reply("`Image generation timed out.`")
        return None

    image_url = await get_response(main_prompt, negative_prompt, engine)
    if image_url:
        caption = f"<b>🖼️ Genrated Image</b>\n\n<b>🌟 Prompt:</b> <code>{main_prompt}</code>\n<b>🌟 Negetive Prompt:</b> <code>{negative_prompt}</code>\n<b>🚀 Engine:</b> <code>{engine}</code>\n\n<blockquote>©️ @RemainsAlways</blockquote>"
        await event.client.send_file(
            event.chat_id, 
            file="GenratedImage.png",
            force_document=False, 
            caption=caption, 
            parse_mode="html",
            reply_to=event.reply_to_msg_id or event.id
        )
        await msg.delete()
        os.remove("GenratedImage.png")
    else:
        await msg.reply(f"`Maybe Error: So Image Url Is {image_url}`")
"""
    if image_url:
        try:
        # Download the image from the URL
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    if resp.status == 200:
                        image_data = await resp.read()

                    # Convert to PNG if needed
                        image = Image.open(io.BytesIO(image_data)).convert("RGB")
                        png_image_path = "converted_image.png"
                        image.save(png_image_path, "PNG")

                    # Send the converted PNG image to Telegram
                        await event.client.send_file(
                            event.chat_id,
                            png_image_path,
                            caption=f"**Prompt:** `{main_prompt}`\n**Negative Prompt:** `{negative_prompt}`\n**Engine:** `{engine}`"
                        )

                    # Clean up by deleting the saved PNG file
                        os.remove(png_image_path)
                    else:
                        await msg.reply("`Failed to download the image from the provided URL.`")
        except Exception as e:
            await msg.reply(f"`Error during image processing: {e}`")

    # Delete the processing message if the image was sent successfully
        await msg.delete()
    else:
        await msg.reply(f"`Error: Image URL returned is {image_url}`")
"""