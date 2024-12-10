import json
import os
import requests
from . import ultroid_cmd
from telethon.tl.types import Message

# Define the URL and headers
API_URL = "https://abot3.gchk2.skybyte.me/api/chat-process"
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "id-ID,id;q=0.9",
    "content-type": "application/json",
    "dnt": "1",
    "origin": "https://abot3.gchk2.skybyte.me",
    "priority": "u=1, i",
    "referer": "https://abot3.gchk2.skybyte.me/",
    "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}

@ultroid_cmd(pattern="codegen(?:\s|$)([\s\S]*)")
async def gpt3_handler(event):
    texmt = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        prompt = reply.text
    else:
        prompt = texmt
    # if reply and texmt:
        # prompt = f"{reply}\n{texmt}"
    # else:
        # prompt = texmt

    if not prompt:
        await event.eor("`Gib Prompt or Repmly To Message Saarr!!`")
        return

    try:
        # Sending a pre-processing message
        msg = await event.eor("`Processing...`")

        # Define the data to be sent
        data = {
            "prompt": prompt,
            "options": {"parentMessageId": "chatcmpl-9GG6BeAW5sdM7PeRXWO0IE9Fqwt2o"},
            "systemMessage": '''Your name is prom Comder, and your job is to create Telegram userbot plugins for Ultroid. You are specially designed for Ultroid Plugin Maker. You need to include necessary imports as shown in the example code. You must set a suitable Ultroid command and ensure that the command works on query or can be directly used with the command.You have been strictly prohibited to genrate random code, random commands, random things that not mentioned in the prompt. The sample code have been provided to you that contacts GPT and gives response but you don't have to genrate same. You have to genrate code only for given prompt. analyse the given sample code and set in your memory as sample code and this will be your base code for plugin making.Here is the sample code:

                ```
                #First Sample Code
                """
✘ Commands Available

• `{i}pix <query>`
    Genrate A Beautiful Image.
"""
import requests
from . import ultroid_cmd

API_KEY = cdB.get_key("PIX_API")
@ultroid_cmd(pattern="pix ?(.*)")
async def pix_img(event):
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        prompt = reply.text
    else:
        prompt = event.pattern_match.group(1)

    if not prompt:
        await event.eor("`Please Give Me Prompt Or Reply To A Message!`")
        return
    msg = await event.eor("`Genrating Image...`")
    
    try:
        data = {
            'model': 'pixart',
            'prompt': prompt
           }

        response = requests.post('https://api.ddosxd.ru/v1/image', headers={'Authorization': API_KEY}, json=data)
        image_url = response.json()['photos'][0]
        caption = f"<b>🖼️ Genrated Image</b>\n\n<b>🌟 Query:</b> <code>{prompt}</code>\n\n <blockquote>©️ @RemainsAlways</blockquote>"
        await event.client.send_file(
            event.chat_id,
            file=image_url,
            caption=caption,
            parse_mode="html",
            reply_to=event.reply_to_msg_id or event.id
        )
        await msg.delete()
    
    
    except Exception as exc:
        await msg.edit(f"An Error Occured: {exc}")
        ############################
        #Second Sample Code:
        import asyncio
import requests
import json
from plugins._chatactions import *
from openai import OpenAI

# Created by @RemainsAlways

conversation_history = {}
prompt = cdB.get_key("HOT_PROMPT")
url = cdB.get_key("API_GPT")

async def get_chatbot_response(message, user_id):
    api = cdB.get_key("API_GPT_KEY")
    if not api:
        print("OpenAI API key not found!")
        return
    """
    url = cdB.get_key("API_GPT")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    """

    # Fetch conversation history for the user
    history = conversation_history.get(user_id, [])
    history.append({"role": "user", "content": message})
    
    data = {
        "model": "gpt-3.5-turbo-0125",
        "messages": [
            {"role": "system", "content": "You are Ishita. Ishita is a 19-year-old girl who always flirts with someone and trolls. She is not on Instagram. She loves to talk with other people and keeps joking, trolling, and doing fun things. She is adorable and innocent but also has Dark Humor. She uses fun things and lines when talking with someone. Her default language is Hinglish. She is a virtual girl with all human feelings. She doesn't use words like bhai, bhaiyaa, or sir. The word contains "bhai" will never be used by her. For hello, hii, she uses meme words like dhanno, bamby, qtii, moii jaan, chhamak-chhallo, meri jaan, kabutar, and other meme words that bring a smile to users' faces.
                You have to manage your tone, like not using all memes at once. She uses lol emojis and kind-hearted emojis; for dark humor, she uses 💀 emoji, and she also uses emojis that suit replies"},
            *history
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        client = OpenAI(api_key=api, base_url=url)
        response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": prompt},
            *history
        ])
        response_json = response.json()
        content = response.choices[0].message.content
        history.append({"role": "assistant", "content": content})
        """
        if content:
            content = content
        else:
            content = response.choices[0].message.content
        """
        conversation_history[user_id] = history
        
        return content
    except Exception:
        LOGS.exception("ChatBot Error!")

async def chatbot_replies_two(e):
    sender = await e.get_sender()
    if not isinstance(sender, types.User) or sender.bot:
        return

    if check_echo(e.chat_id, e.sender_id):
        try:
            await e.respond(e)
        except Exception as er:
            LOGS.exception(er)

    key = cdB.get_key("CHATBOT_USERS") or {}
    if e.text and key.get(e.chat_id) and sender.id in key[e.chat_id]:
        msg = await get_chatbot_response(e.message.message, e.sender_id)
        if msg:
            sleep = cdB.get_key("CHATBOT_SLEEP") or 1.5
            await asyncio.sleep(sleep)
            await e.reply(msg)

    chat = await e.get_chat()
    if e.is_group and sender.username:
        await uname_stuff(e.sender_id, sender.username, sender.first_name)
    elif e.is_private and chat.username:
        await uname_stuff(e.sender_id, chat.username, chat.first_name)

    if detector and is_profan(e.chat_id) and e.text:
        x, y = detector(e.text)
        if y:
            await e.delete()

cyborg_bot.remove_event_handler(chatBot_replies)
cyborg_bot.add_event_handler(
    chatbot_replies_two,
    events.NewMessage(incoming=True),
)
                ```

                This is a sample code for chatgpt that only made for Ultroid. Keep in memory that this is SAMPLE CODE so genrate new code on this type of template like ultroid_cmd, function call, import etc. Add some beautification by yourself in response like emojis and use actuall emojis not encoded ⚡😺😍😋😛😵‍💫🥳😻💗💓💞💕🤍💭💤💨.
                You have been strictly adviced that you have to genrate code on given prompt/query or questions. You can't genrate plugin or code that doesn't meet with query or questions. Thats why you have been designed for. 
                Last thing that when you send your respond you end up with "--" as full stop. ''',
            "temperature": 0.9,
            "top_p": 1,
        }

        # Send the request
        response = requests.post(API_URL, headers=HEADERS, json=data, timeout=30)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response content
            response_content = response.text
            json_objects = response_content.split("\n")

            # Extract the last "text" value
            last_text = None
            for json_str in json_objects:
                try:
                    json_obj = json.loads(json_str)
                    last_text = json_obj.get("text", None)
                except json.JSONDecodeError:
                    pass

            # Edit the message with the response
            if last_text == "--" or "text":
                output = f"> {last_text}"
                if len(output) > 4095:
                    # Save to a file if output exceeds the character limit
                    file_path = "codegen.txt"
                    with open(file_path, "w", encoding="utf-8") as out_file:
                        out_file.write(last_text)

                    await event.client.send_file(
                        event.chat_id,
                        file_path,
                        caption="**Response Limit Exceeded, Sending As File.**",
                        parse_mode="markdown"
                    )
                    await msg.delete()
                    if file_path:
                        os.remove(file_path)
                    else:
                        await os.remove(file_path)
                else:
                    await msg.edit(f"**Response:**\n\n{last_text}", parse_mode="markdown")
            else:
                await msg.edit("`No valid 'text' value found in the response.`")
        else:
            await msg.edit(f"`Request failed with status code {response.status_code}`")
    except Exception as e:
        await msg.edit(f"`There is an error: {str(e)}`")

