import requests
from fake_useragent import UserAgent
import os
from . import ultroid_cmd, eor

# Function to generate a random user-agent
ua = UserAgent()

# Headers for the API request, with a dynamic User-Agent
def get_headers():
    return {
        "Cookie": "_ga=GA1.1.188708367.1729936606; crisp-client%2Fsession%2Fb21d4851-f776-4e10-bd26-bef59f54886b=session_f95d4e02-7495-464f-9873-b205f99a153a; ph_phc_sUBgtFpFGfL4lIY24ZS4PcZTNaRvtHCCh3XdWQE29CO_posthog=%7B%22distinct_id%22%3A%220192c842-7bca-7f1d-8d94-72971a0ad7e5%22%2C%22%24sesid%22%3A%5Bnull%2Cnull%2Cnull%5D%7D; _ga_9LCF2TJ2CY=GS1.1.1729936606.1.1.1729936653.0.0.0; _iidt=GV1B20OemN3fY585MVWzobBlRTw9Eaz3+AyxrJPv0LPA/yWG2qc29vFTgnAytPmkV0kVcW/+7xLDUeV6UwveWGNLVrcZrdTG; _vid_t=mifUVudiBkLkNFyR8VY69AGUl/5EfSqqiO2P+J9rpieoWHPSDiPlQGkDsT2Dzhp4YLLQvpQ+CIMknbsLpHywwz1PAr1yV2xO",
        "Origin": "https://koala.sh",
        "Referer": "https://koala.sh/images",
        "User-Agent": ua.random,  # Generate a new user-agent each time
        "Visitor-ID": "U1HPfgp3Ghg2wpyRY3AQ",
        "sec-ch-ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Linux"
    }

API_URL = "https://koala.sh/api/image-generation/"

@ultroid_cmd(pattern="koa(?: (.+)|$)")
async def koala_image(event):
    user_input = event.pattern_match.group(1)
    if not user_input:
        await event.eor("`Please provide a prompt for image generation.`")
        return

    pre = await event.eor("`Generating image...`")

    # Data for the API request
    data = {
        "prompt": user_input,
        "style": "photo",
        "size": "1024x1024",
        "model": "standard",
        "numImages": 1
    }

    try:
        # Use dynamic headers with a random user-agent
        response = requests.post(API_URL, headers=get_headers(), json=data)
        response.raise_for_status()
    except Exception as e:
        await pre.edit(f"`Error: {str(e)}`")
        return

    # Parsing the response
    try:
        result = response.json()
        image_url = result[0].get("url")
        image_caption = result[0].get("alt")
        cap = image_caption
        caption = (f"<b>🖼️ Image Genrated!</b>\n\n<b>🌟 Details:</b> <code>{cap}</code>\n\n <blockquote>©️ @RemainsAlways</blockquote>")
        
        if not image_url:
            await pre.edit("`Failed to retrieve image URL from the response.`")
            return

        # Download the image
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        # Save the image locally
        image_path = "Genrated_image.jpg"
        with open(image_path, "wb") as f:
            f.write(image_response.content)
        
        # Send the image
        await event.client.send_file(
            event.chat_id,
            file=image_path,
            caption=caption,
            force_document=False,
            reply_to=event.reply_to_msg_id or event.id,
            parse_mode="html"
        )
        
        # Delete the temporary image file after sending
        os.remove(image_path)
        await pre.delete()
        
    except Exception as e:
        await pre.edit(f"`Error in processing the response: {str(e)}`")
