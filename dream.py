import requests
import io
import os
from PIL import Image
from . import ultroid_cmd, udB
TOKEN = udB.get_key("DREAM_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/Lykon/DreamShaper"
headers = {"Authorization": f"Bearer {TOKEN}"}

@ultroid_cmd(pattern="drsh ?(.*)")
async def dream_shaper(event):
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        input_text = reply.text
    else:
        input_text = event.pattern_match.group(1)

    if not input_text:
        await event.eor("`Please Give Me Prompt Or Reply To A Message!`")
        return
    pre_msg = await event.eor("`Generating Image...`")
    # Payload with user input
    payload = {
        "inputs": input_text,
    }

    try:
        # Query API
        image_bytes = query(payload)
        file_path = save_image(image_bytes, "generated_image.png")
        if not file_path:
            await pre_msg.edit("`Error occurred while saving the image. Please try again later.`")
            return

        # Caption for the image
        caption = f"<b>🖼️ Genrated Image Using DreamShaper</b>\n\n<b>🌟 Query:</b> <code>{input_text}</code>\n\n <blockquote>©️ @RemainsAlways</blockquote>"
        # Upload the image to Telegram
        file = await event.client.upload_file(file_path)
        await event.client.send_file(
            event.chat_id,
            file=file,
            caption=caption,
            parse_mode="html",
            reply_to=event.reply_to_msg_id or event.id,
            force_document=False
        )
        
        # Delete the pre-message after successful image send
        await pre_msg.delete()

        # Remove the file after sending successfully
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        # Clear and specific error message
        await pre_msg.edit(f"`An unexpected error occurred: {str(e)}`")

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        return None

def save_image(image_bytes, file_name="image.png"):
    if image_bytes:
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.save(file_name)
            return file_name
        except Exception as e:
            print(f"Error saving image: {str(e)}")
            return None
    else:
        print("No image bytes to save.")
        return None
