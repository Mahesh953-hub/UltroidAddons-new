import json
import requests
from . import ultroid_cmd, eor

@ultroid_cmd(pattern="theai ?(.*)")
async def chatgpt_cmd(e):
    args = e.pattern_match.group(1)
    if not args and not e.is_reply:
         return await e.reply("Please provide a prompt or reply to a message.")

    system_prompt = ("""You are TheB 4.0. A Upgraded version of TheB.AI model, optimized for conversations, with faster response, more natural and vivid language. Powered by Mixed Model Routing (GPT-4o, Claude 3.5 Sonnet, Llama 3.1 405B). You use Emojis for better conversations handling""")
        
    if e.is_reply:
        reply_msg = await e.get_reply_message()
        args = reply_msg.text
        
    prompt = args

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
            "role": "system",
            "content": """You are TheB 4.0. A Upgraded version of TheB.AI model, optimized for conversations, with faster response, more natural and vivid language. Powered by Mixed Model Routing (GPT-4o, Claude 3.5 Sonnet, Llama 3.1 405B). You use Emojis for better conversations handling""",
            "role": "user",
            "content": prompt
        }
        ]
    }

        eor_message = await e.eor("✨")

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_json = response.json()

        response_text = response_json.get("response", "No response from API.")

        await eor_message.eor(response_text)
    except Exception as exc:
        await eor_message.eor(f"Error: {exc}")