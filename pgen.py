import json
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

@ultroid_cmd(pattern="pygen ?(.*)")
async def gpt3_handler(event):
    # Fetching user input from reply or message
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        prompt = reply.text
    else:
        prompt = event.pattern_match.group(1)

    if not prompt:
        await event.eor("`Please Write Code with Command Or Reply To A Code Message.`")
        return

    try:
        # Sending a pre-processing message
        msg = await event.eor("`Processing...`")

        # Define the data to be sent
        data = {
            "prompt": prompt,
            "options": {"parentMessageId": "chatcmpl-9GG6BeAW5sdM7PeRXWO0IE9Fqwt2o"},
            "systemMessage": "You are PyGen an AI model that specializes in Python programming expertise, capable of seamlessly converting code from other languages into Python. The model should accurately translate code structures, syntax, and logic while maintaining functionality and efficiency in Python. Develop a system that can handle a wide range of programming languages and produce clean, readable Python code that runs smoothly. Ensure that the AI model is versatile, reliable, and efficient in delivering accurate Python translations, making it a valuable tool for programmers and developers worldwide. PyGen Has been Developed for a cutting-edge AI model that excels as a Python expert, showcasing advanced capabilities to seamlessly convert code from any known programming language into Python. The model should demonstrate in-depth understanding of intricate coding concepts and ensure precise and efficient translation for complex algorithms and scripts. Create an innovative system that effectively bridges the gap between diverse programming languages, offering unparalleled accuracy and versatility in code conversion tasks. ",
            "temperature": 0.9,
            "top_p": 1,
        }

        # Send the request
        response = requests.post(API_URL, headers=HEADERS, json=data, timeout=10)

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
            if last_text:
                output = f"> {last_text}"
                if len(output) > 4095:
                    # Save to a file if output exceeds the character limit
                    file_path = "PyGen.txt"
                    with open(file_path, "w", encoding="utf-8") as out_file:
                        out_file.write(last_text)

                    await event.client.send_file(
                        event.chat_id,
                        file_path,
                        caption="**Response Limit Exceeded, Sending As File.**",
                        parse_mode="markdown"
                    )
                    await msg.delete()
                else:
                    await msg.edit(f"**Response:**\n\n{last_text}", parse_mode="markdown")
            else:
                await msg.edit("`No valid 'text' value found in the response.`")
        else:
            await msg.edit(f"`Request failed with status code {response.status_code}`")
    except Exception as e:
        await msg.edit(f"`There is an error: {str(e)}`")

