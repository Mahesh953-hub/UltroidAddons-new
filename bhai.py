import json
import requests
from . import ultroid_cmd

@ultroid_cmd(pattern="bhai ?(.*)")
async def chatgpt_cmd(e):
    args = e.pattern_match.group(1)
    if not args and not e.is_reply:
         return await e.reply("Please provide a prompt or reply to a message.")

    additional_text = ("<p>You are user's friend. You don't need to talk about SEO. "
    "You need to reply to the query in a friendly tone in Hindi using emojis "
     "and address the user as 'bhai' using words like 'Arey bhai', 'Nahi bhai', 'Haan bhai', 'Theek bhai', etc. "
        "Your query is:</p>")
        
    if e.is_reply:
        reply_msg = await e.get_reply_message()
        args = reply_msg.text
        
    prompt = additional_text + args

    try:
        url = "https://post-ai-backend.vercel.app/api/generateModelGptChat"
        headers = {
            "User-Agent": "Python/requests",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip"
        }
        payload = {
            "prompt": [
            {
            "role": "user",
            "content": prompt
        }
        ]
    }

        eor_message = await e.eor("✨")

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_json = response.json()

        response_text = response_json.get("response", "No response from API.")
        #await eor_message.delete()

        await eor_message.edit(response_text)
    except Exception as exc:
        await eor_message.reply(f"Error: {exc}")