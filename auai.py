import requests
from . import ultroid_cmd
from telethon.tl.types import Message

API_URL = "https://api.botcahx.eu.org/api/search/openai-custom"
API_KEY = "LwulPck3"  # Replace with your API key

async def ai_hadeh(client, user_id, user_name, text):
    gwa = "<a href='tg://user?id=6340125899'>@RemainsAlways</a>"
    bahan = [
        {
            "role": "system",
            "content": f"You are the telegram assistant of my user {gwa}",
        },
        {
            "role": "assistant",
            "content": f"You are powerfull Assistant of Telegram User {gwa} and capable of doing simple tasks to hard coding solutions. Desiged and Developed by {gwa}",
        },
        {"role": "user", "content": f"{text}"},
    ]
    payload = {"message": bahan, "apikey": API_KEY}
    
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get("result", "No Response From API 😕.")
    else:
        return f"API Error: {response.text}"

@ultroid_cmd(pattern="au(?:\s|$)([\s\S]*)")
async def handle_message(event):
    # Pre-message while processing
    msg = await event.eor("`Processing...`", parse_mode="markdown")
    
    # Fetching user input from reply or message
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        user_text = reply.text
    else:
        user_text = event.pattern_match.group(1)

    # Check if user provided the input
    if not user_text:
        await msg.edit("`Please provide the text after the command or reply to a message.`", parse_mode="markdown")
        return

    try:
        user_id = event.sender_id
        user_name = (await event.client.get_me()).first_name
        response_text = await ai_hadeh(event.client, user_id, user_name, user_text)

        # Check if the response exceeds the Telegram character limit
        if len(response_text) > 4095:
            # Save the response as a text file
            file_path = "ai_response.txt"
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response_text)

            # Send the file and delete the initial processing message
            await event.client.send_file(
                event.chat_id,
                file_path,
                caption="Response exceeded limits, Sending as file.",
                parse_mode="html"
            )
            await msg.delete()
        else:
            # Send the response if within limits
            beautified_response = f"<b>⚡ Response:</b>\n\n{response_text}"
            await msg.edit(beautified_response, parse_mode="html")
    except Exception as e:
        await msg.edit(f"`Error: {str(e)}`", parse_mode="md")
