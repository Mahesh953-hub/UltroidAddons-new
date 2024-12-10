# Import necessary modules for Ultroid and Telethon
from . import ultroid_cmd
from telethon import events
import requests
from telethon.tl.types import InputFile
import os

@ultroid_cmd(pattern="t2i ?(.*)")
async def text_to_image(event):
    """
    A command to generate an image from text using the Widipe API.
    Usage: /t2i <prompt>
    """
    # Get the user's prompt from the command
    prompt = event.pattern_match.group(1).strip()
    
    if not prompt:
        await eor(event, "**Please provide a prompt for image generation!**")
        return
    
    # Send a temporary message indicating processing
    processing_msg = await eor(event, f"🔄 **Generating image for prompt:** `{prompt}`...")
    
    try:
        # Make a request to the API with the user's prompt
        api_url = f"https://widipe.com/ai/text2img?text={prompt}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            # Save the image temporarily
            image_path = "generated_image.png"
            with open(image_path, "wb") as file:
                file.write(response.content)
            
            # Send the image with the formatted caption
            caption = f"🖼️ **Image successfully generated!**\n\n**Prompt:** `{prompt}`\n\n©️ @RemainsAlways"
            await event.client.send_file(event.chat_id, image_path, caption=caption)
            
            # Delete the temporary file after sending
            os.remove(image_path)
            await processing_msg.delete()
        else:
            # Handle error if the API call fails
            await eor(event, "**Failed to generate image. Please try again later.**")
    
    except Exception as e:
        # Catch any other exceptions and display an error message
        await eor(event, f"**An error occurred:** `{str(e)}`")
