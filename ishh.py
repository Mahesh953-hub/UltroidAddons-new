import requests
from . import ultroid_cmd, eor
import time


def post_request(url, headers, json_data, retries=3):
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, json=json_data, timeout=10)
            if response.status_code == 200:
                resp = response.json()
                return resp['response']
            elif response.status_code == 504:
                time.sleep(2)
        except requests.exceptions.RequestException as e:
            return f"```Error: {e}```"
    return "```Error: Unable to process the request.```"

@ultroid_cmd(pattern="ish ?(.*)")
async def ishita(event):
    user_input = event.pattern_match.group(1)
    if not user_input:
        if event.reply_to_msg_id:
            replied_message = await event.get_reply_message()
            user_input = replied_message.text
        else:
            await eor(event, "Please provide a message or reply to one.")
            return
    
    await eor(event, "`Processing your request...`")
    
    url = "https://post-ai-backend.vercel.app/api/generateModelGptChat"
    headers = {
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip"
    }
    json_data = {
        "prompt": [
            {
                "role": "system",
                "content": """You are Ishita. Ishita is a 19-year-old girl who always flirts with someone and trolls. She is not on Instagram. She loves to talk with other people and keeps joking, trolling, and doing fun things. She is adorable and innocent but also has Dark Humor. She uses fun things and lines when talking with someone. Her default language is Hinglish. She is a virtual girl with all human feelings. She doesn't use words like bhai, bhaiyaa, or sir. The word contains "bhai" will never be used by her. For hello, hii, she uses meme words like dhanno, bamby, qtii, moii jaan, chhamak-chhallo, meri jaan, kabutar, and other meme words that bring a smile to users' faces.
                You have to manage your tone, like not using all memes at once. She uses lol emojis and kind-hearted emojis; for dark humor, she uses 💀 emoji, and she also uses emojis that suit replies."""},
            {
                "role": "user",
                "content": user_input
            }
        ]
    }
    
    response = post_request(url, headers, json_data)
    reply = f"```Your Query: {user_input}```\n```Response: {response}```"
    await eor(event, reply)
