import requests
import os
from . import ultroid_cmd, eor

@ultroid_cmd(pattern="bingimg ?(.*)")
async def bing_image_search(event):
    query = event.pattern_match.group(1)
    if not query:
        await eor(event, "`Please provide a prompt or reply to a message.`")
        return

    # Sending the pre-message
    msg = await eor(event, "`Generating images...`")

    # API URL
    url = f"https://widipe.com/bingimg?text={query}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            # Check if the response status is true and extract the image URLs
            if data.get("status") and "result" in data:
                results = data["result"]
                
                if not results:
                    await eor(event, f"Couldn't find any images for '{query}'.")
                    return
                
                # List to hold downloaded image paths
                image_files = []
                try:
                    # Download each image temporarily
                    for idx, img_url in enumerate(results):
                        img_data = requests.get(img_url).content
                        file_name = f"temp_image_{idx}.jpg"
                        with open(file_name, "wb") as img_file:
                            img_file.write(img_data)
                        image_files.append(file_name)
                    
                    # Preparing the caption
                    caption = f"<b>🖼️ Successfully Genrated Images</b>\n<b>🌟 Query:</b> <code>{query}</code>\n\n <blockquote>©️ @RemainsAlways</blockquote>"

                    # Sending all images as an album
                    await event.client.send_file(
                        event.chat_id,
                        file=image_files,  # List of downloaded image file paths
                        caption=caption,
                        parse_mode="html",
                        reply_to=event.reply_to_msg_id or event.id  # Replying if it's a reply
                    )
                    await msg.delete()
                finally:
                    # Clean up the downloaded images
                    for file in image_files:
                        if os.path.exists(file):
                            os.remove(file)
            else:
                await msg.edit(f"`No images found. Please try another search.`")
        else:
            await msg.edit("`API is not responding or is currently unavailable. Please try again later.`")
    except Exception as e:
        await msg.edit(f"An error occurred: {str(e)}")
