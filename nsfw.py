"""
This module can search images in danbooru and send in to the chat!
──「 **Danbooru Search** 」──
"""

import os
import urllib
import requests
from . import ultroid_cmd, eor

plugin_category = "fun"

@ultroid_cmd(
    pattern=r"ani(mu|nsfw) ?([\s\S]*)",
    command=("ani", plugin_category),
    info={
        "header": "Contains NSFW 🔞.\nTo search images in danbooru!",
        "usage": [
            "{tr}animu <query>",
            "{tr}aninsfw <nsfw query>",
        ],
        "examples": [
            "{tr}animu naruto",
            "{tr}aninsfw naruto",
        ],
    },
)
async def danbooru(event):
    "Get anime charecter pic or nsfw"
    msg = await eor(event, "`Processing…`")
    rating = "Explicit" if "nsfw" in event.pattern_match.group(1) else "Safe"
    search_query = event.pattern_match.group(2)
    params = {
        "limit": 1,
        "random": "true",
        "tags": f"Rating:{rating} {search_query}".strip(),
    }
    with requests.get(
        "http://danbooru.donmai.us/posts.json", params=params
    ) as response:
        if response.status_code == 200:
            response = response.json()
        else:
            return await eor(
                event, f"**An error occurred, response code: **`{response.status_code}`"
            )

    if not response:
        return await eor(event, f"**No results for query:** __{search_query}__")
    valid_urls = [
        response[0][url]
        for url in ["file_url", "large_file_url", "source"]
        if url in response[0].keys()
    ]
    if not valid_urls:
        return await eor(
            event, f"**Failed to find URLs for query:** __{search_query}__"
        )
    for image_url in valid_urls:
        try:
            cap = (f"[SOURCE]({image_url})")
            await event.eor(file=image_url)
            await msg.delete()
            return event.eor(image_url)
        except Exception as e:
            await eor(event, f"{e}")
    await eor(event, f"**Failed to fetch media for query:** __{search_query}__")


@ultroid_cmd(
    pattern=r"boobs(?:\s|$)([\s\S]*)",
    command=("boobs", plugin_category),
    info={
        "header": "NSFW 🔞\nYou know what it is, so do I !",
        "usage": "{tr}boobs",
        "examples": "{tr}boobs",
    },
)
async def boobs(e):
    "Search boobs"
    a = await eor(e, "`Sending boobs...`")
    nsfw = requests.get("http://api.oboobs.ru/noise/1").json()[0]["preview"]
    urllib.request.urlretrieve(f"http://media.oboobs.ru/{nsfw}", "boobs.jpg")
    await e.eor(file="boobs.jpg")
    os.remove("boobs.jpg")
    await a.delete()


@ultroid_cmd(
    pattern=r"butts(?:\s|$)([\s\S]*)",
    command=("butts", plugin_category),
    info={
        "header": "NSFW 🔞\nBoys and some girls likes to Spank this 🍑",
        "usage": "{tr}butts",
        "examples": "{tr}butts",
    },
)
async def butts(e):
    "Search beautiful butts"
    a = await eor(e, "`Sending beautiful butts...`")
    nsfw = requests.get("http://api.obutts.ru/butts/10/1/random").json()[0]["preview"]
    urllib.request.urlretrieve(f"http://media.obutts.ru/{nsfw}", "butts.jpg")
    await e.eor(file="butts.jpg")
    os.remove("butts.jpg")
    await a.delete()
