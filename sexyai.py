"""
✘ Commands Available

• `{i}sexyai <prompt> -n <Negetive Prompt> -e <Engine>`
    Genrate A Sexy Image By Given Prompts.
    Details:
        -n : Nagetive Prompt That Should Not Be Include in Image,
        -e : Engine To Gen Image With.
    
    @RemainsAlways
"""
import os
import aiohttp
import random
import asyncio
import json
import uuid
from curl_cffi.requests import AsyncSession
from . import ultroid_cmd, eor


API_URL = "https://api.sexy.ai"
SESS_ID = "77e75caf-527e-4c9a-8b71-88c85a4e198a"
Engines = ["Grounded Realistic Mix.safetensors","Hassaku Hentai.safetensors","Lazymix Real Amateur.safetensors","Porn Ultimate.safetensors","Hentai V2.safetensors","Latex Vision.safetensors","Epic Natural.safetensors","Hardcore Hentai 1.3.safetensors","Pina Colada Furry Mix.safetensors","Futanari Diffusion.safetensors","Realistic Vision.safetensors","Seel Real Furry 4.93.safetensors","Experience.safetensors","Homoerotic.safetensors","Coconut Furry Mix.safetensors","Anime Characters.safetensors","Photon.safetensors","Porn Cartoon.safetensors","Manly Nudes.safetensors","Ultra Real Porn.safetensors","CyberRealistic Revamp.safetensors","Homoerotic - Unstable.safetensors","Pony Diffusion SD.safetensors","Epic Photo.safetensors","Abyss Orange Mix2 NSFW.safetensors","Persika Furry Realism.safetensors","Real Cartoon 3D.safetensors","Real Dream.safetensors","Toon Universe.safetensors","Art Universe.safetensors","Blowbang Ultimate.safetensors","Chillout Mix.safetensors","Clear Bondage.safetensors","Dreamshaper.safetensors","Dreamshaper Pixel Art.safetensors","Anime Furry.safetensors","Gay Diffusion.safetensors"]

@ultroid_cmd(pattern="sexyai ?(.*)")
async def sexy_ai(event):
    reply = await event.get_reply_message()
    args = event.pattern_match.group(1) if not reply else reply.message
    if not args:
        await event.eor("`Please Provide Prompt Or Reply To Prompt Message.`")
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

    msg = await event.eor("`Genrating Image...`")
     
    async def get_user(session, SESS_ID):
        get_user_url = f"{API_URL}/getSelfUser"
        params = {
          "sessionID" : SESS_ID,
          "isAtLeast18Confirmed" : "true",
          "profilePicture" : "true",
          "extendedPriceInfo" : "true"
      
        }
        response = await session.get(get_user_url, params=params)
        status = response.status_code
        print(response.json)
        if status == 200:
            await msg.edit("`User Status:` **OK**") 
            data = response.json
            return data
        else:
            await msg.edit(f"Error: {status}")
        
    #await get_user()
    async def get_response(main_prompt, negative_prompt, engine):
        with AsyncSession(impersonate="chrome107") as session:
            self_user_data = await get_user(session, SESS_ID)
            if self_user_data is None:
                await msg.edit("`Unable to Get Self User Data`")
            else:
                await msg.edit("`Request Success`")
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
                "width": 768,
                "height": 768,
                "steps": 20,
                "seed": random.randint(1, 760547),
                "subseed": 0,
                "subseed_strength": 0.1,
                "sampler": "DPM++ 2M Karras",
                "cfgscale": 7,
            }
            #Sending Request For Image Genration
            resp = await session.post(
                f"https://{API_URL}/generateImage",
                headers=headers,
                json=data,
            )
            await msg.edit("`Now Sending Request For Genrating Image`")
            texxt = resp.text
            #res = resp.json
            data = json.loads(texxt)
            print(data)
            imageID = data.get("payload", {}).get("imageID", None)  # data["imageID"]
            censored = data.get("hasError")
            if censored:
                return (
                    f"{prompt} or {negative_prompt}"
                )
            ignoredWords = data.get("payload", {}).get("ignoredWords", None)
            areWeOut = "pending"
            headers2 = {
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
            timeCounter = -1
            while areWeOut == "pending":
                await asyncio.sleep(2)
                resps = await session.get(
                    f"https://api.sexy.ai/getItemStatus?imageID={imageID}&sessionID={SESS_ID}",  # getImageStatus",
                    headers=headers2,
                )
                text = resps.text
                timeCounter += 1
                if text:
                    data = json.loads(text)
                    if data.get("payload", {}).get("status", None) != "pending":
                        return data, ignoredWords
                    elif timeCounter > 6:
                        return "Request failed to materialize.", ignoredWords
                    else:
                        await msg.edit(text)
                else:
                    return None