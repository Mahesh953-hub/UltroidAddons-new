import requests
from . import ultroid_cmd

API_URL = "https://widipe.com/turbo"
API_V1 = "https://widipe.com/v1/turbo"
API_V2 = "https://widipe.com/v2/turbo"

@ultroid_cmd(pattern="turbo(?:\s|$)([\s\S]*)")
async def gpt4_query(event):
    msg = await event.eor("💘")
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        user_text = reply.text
    else:
        user_text = event.pattern_match.group(1)
    if not user_text:
        await msg.edit("`Please provide the text after the command or reply to a message.`", parse_mode="markdown")
        return
    
    # API parameters
    params = {'text': user_text}
    headers = {'accept': 'application/json'}
    
    try:
        # Sending the request to the API
        response = requests.get(API_URL, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'result' in data:
                result_text = data['result']
                if len(result_text) > 4095:
                    with open("turbo.txt", "w", encoding="utf-8") as file:
                        file.write(result_text)
                    await event.client.send_file(
                        event.chat_id,
                        "turbo.txt",
                        caption="**Response is too long, sent as a file.**",
                        parse_mode="markdown"
                    )
                    await msg.delete()
                else:
                    beautified_response = f"**Response:**\n\n{result_text}"
                    await msg.edit(beautified_response, parse_mode="markdown")
            else:
                await msg.edit(f"`Unexpected response structure:\n{response.text}`", parse_mode="markdown")
        else:
            await msg.edit(f"`Error {response.status_code}: Unable to fetch data from API.`", parse_mode="markdown")
    except Exception as e:
        await msg.edit(f"`An error occurred:\n{e}`", parse_mode="markdown")
        
#========================#
#========================#
@ultroid_cmd(pattern="turbov1(?:\s|$)([\s\S]*)")
async def gpt4_query(event):
    msg = await event.eor("🎉")
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        user_text = reply.text
    else:
        user_text = event.pattern_match.group(1)
    if not user_text:
        await msg.edit("`Please provide the text after the command or reply to a message.`", parse_mode="markdown")
        return
    
    # API parameters
    params = {'text': user_text}
    headers = {'accept': 'application/json'}
    
    try:
        # Sending the request to the API
        response = requests.get(API_V1, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'result' in data:
                result_text = data['result']
                if len(result_text) > 4095:
                    with open("turbo_V1.txt", "w", encoding="utf-8") as file:
                        file.write(result_text)
                    await event.client.send_file(
                        event.chat_id,
                        "turbo_V1.txt",
                        caption="**Response is too long, sent as a file.**",
                        parse_mode="markdown"
                    )
                    await msg.delete()
                else:
                    beautified_response = f"**Response:**\n\n{result_text}"
                    await msg.edit(beautified_response, parse_mode="markdown")
            else:
                await msg.edit(f"`Unexpected response structure:\n{response.text}`", parse_mode="markdown")
        else:
            await msg.edit(f"`Error {response.status_code}: Unable to fetch data from API.`", parse_mode="markdown")
    except Exception as e:
        await msg.edit(f"`An error occurred:\n{e}`", parse_mode="markdown")
        
#=========================#
#=========================#

@ultroid_cmd(pattern="turbov2(?:\s|$)([\s\S]*)")
async def gpt4_query(event):
    msg = await event.eor("🎊")
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        user_text = reply.text
    else:
        user_text = event.pattern_match.group(1)
    if not user_text:
        await msg.edit("`Please provide the text after the command or reply to a message.`", parse_mode="markdown")
        return
    
    # API parameters
    params = {'text': f"Response should be in English {user_text}"}
    headers = {'accept': 'application/json'}
    
    try:
        # Sending the request to the API
        response = requests.get(API_V2, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'result' in data:
                result_text = data['result']
                if len(result_text) > 4095:
                    with open("turbo_V2.txt", "w", encoding="utf-8") as file:
                        file.write(result_text)
                    await event.client.send_file(
                        event.chat_id,
                        "turbo_V2.txt",
                        caption="**Response is too long, sent as a file.**",
                        parse_mode="markdown"
                    )
                    await msg.delete()
                else:
                    beautified_response = f"**Response:**\n\n{result_text}"
                    await msg.edit(beautified_response, parse_mode="markdown")
            else:
                await msg.edit(f"`Unexpected response structure:\n{response.text}`", parse_mode="markdown")
        else:
            await msg.edit(f"`Error {response.status_code}: Unable to fetch data from API.`", parse_mode="markdown")
    except Exception as e:
        await msg.edit(f"`An error occurred:\n{e}`", parse_mode="markdown")