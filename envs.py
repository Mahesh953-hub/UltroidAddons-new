"""
envs.sh Image Upload Plugin | THE NULL POINTER
File hosting and URL shortening service.

Usage:
- Reply to an image with `.envs`: Uploads the image and provides a shareable link.
- Reply to an image with `.envs <hours>`: Uploads the image with a specified expiration time (in hours).

Files are stored for a minimum of 30 days and up to 1 year.
Maximum file size: 512.0 MiB.
"""

from telethon import events
from . import ultroid_cmd, eor
import requests

@ultroid_cmd(pattern="envs ?(.*)")
async def upload_image(event):
    args = event.pattern_match.group(1)
    reply = await event.get_reply_message()

    if not reply or not reply.media:
        await eor(event, "Please reply to an image to upload.")
        return

    msg = await eor(event, "Uploading image, please wait...")

    # Set expiration if provided
    expires = args if args.isdigit() else None

    try:
        # Download the replied image in binary mode
        image = await event.client.download_media(reply.media, bytes)

        # Prepare the request data for `envs.sh`
        files = {'file': ('image.png', image, 'image/png')}
        data = {'expires': expires} if expires else {}

        # Send the POST request to `envs.sh`
        response = requests.post("https://envs.sh", files=files, data=data)

        if response.status_code == 200:
            await msg.edit(f"**Upload Success:**\nHere Is Your Link: {response.text}")
        else:
            await msg.edit("`Failed to upload the image.`")
    except Exception as e:
        await msg.edit(f"**Error:** {str(e)}")
