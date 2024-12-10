import requests
from . import ultroid_cmd

API_GTP = "https://widipe.com/gptgo"
API_KOTOL = "https://widipe.com/openai"

async def tanya(text):
    params = {'text': f" Response should be in English. {text}"}
    headers = {'accept': 'application/json'}
    response = requests.get(API_GTP, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'result' in data:
            return data['result']
        else:
            return f"Unexpected response format: {response.text}"
    else:
        return f"API Error: {response.status_code}: {response.text}"

async def kotol(text):
    params = {'text': f"Response should be in English. {text}"}
    headers = {'accept': 'application/json'}
    response = requests.get(API_KOTOL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'result' in data:
            return data['result']
        else:
            return f"Unexpected response format: {response.text}"
    else:
        return f"API Error: {response.status_code}: {response.text}"

@ultroid_cmd(pattern="gtp(?:\s|$)([\s\S]*)")
async def gtp_handler(event):
    # Pre-message while processing
    msg = await event.eor("`Processing...`", parse_mode="markdown")
    
    # Fetching user input from reply or message
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        prompt = reply.text
    else:
        prompt = event.pattern_match.group(1)

    if not prompt:
        await msg.edit("`Gib Prompt or Remply Message saarrrrr!`", parse_mode="markdown")
        return

    try:
        hasil = await tanya(prompt)

        # Check if the response exceeds Telegram's character limit
        if len(hasil) > 4095:
            file_path = "gtp_response.txt"
            with open(file_path, "w", encoding="utf-8") as out_file:
                out_file.write(hasil)
            await event.client.send_file(
                event.chat_id,
                file_path,
                caption="**Response Limit Exceeded, Sending as File.**",
                parse_mode="markdown"
            )
            await msg.delete()
        else:
            await msg.edit(f"**Response:**\n\n{hasil}", parse_mode="markdown")
    except Exception as e:
        await msg.edit(f"`An Error Occurred: {str(e)}`", parse_mode="markdown")

@ultroid_cmd(pattern="gpt(?:\s|$)([\s\S]*)")
async def gpt_handler(event):
    # Pre-message while processing
    msg = await event.eor("`Processing!`", parse_mode="markdown")
    
    # Fetching user input from reply or message
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        prompt = reply.text
    else:
        prompt = event.pattern_match.group(1)

    if not prompt:
        await msg.edit("`Gib Prompt or Remply Message saarrrrr!`", parse_mode="markdown")
        return

    try:
        hasil = await kotol(prompt)

        # Check if the response exceeds Telegram's character limit
        if len(hasil) > 4095:
            file_path = "gpt_response.txt"
            with open(file_path, "w", encoding="utf-8") as out_file:
                out_file.write(hasil)
            await event.client.send_file(
                event.chat_id,
                file_path,
                caption="**Response Exceeded Limits, Sending as File..**",
                parse_mode="markdown"
            )
            await msg.delete()
        else:
            await msg.edit(f"**Response:**\n\n{hasil}", parse_mode="markdown")
    except Exception as e:
        await msg.edit(f"`An Error Occurred: {str(e)}`", parse_mode="markdown")
        