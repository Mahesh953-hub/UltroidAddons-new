import requests
from . import ultroid_cmd

API_URL = "https://widipe.com/gpt4"
API_V2 = "https://widipe.com/v2/gpt4"

@ultroid_cmd(pattern="gpt4(?:\s|$)([\s\S]*)")
async def gpt4_query(event):
    # Pre-message while processing
    msg = await event.eor("`Processing your request...`")

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
                
                # Check if the result exceeds the Telegram character limit
                if len(result_text) > 4095:
                    # Save the response as a text file
                    with open("gpt4_response.txt", "w", encoding="utf-8") as file:
                        file.write(result_text)
                    
                    # Send the file and delete the initial processing message
                    await event.client.send_file(
                        event.chat_id,
                        "gpt4_response.txt",
                        caption="**Response is too long, sent as a file.**",
                        parse_mode="markdown"
                    )
                    await msg.delete()
                else:
                    # Beautify and send the response if within limits
                    beautified_response = f"**Response:**\n\n{result_text}"
                    await msg.edit(beautified_response, parse_mode="markdown")
            else:
                await msg.edit(f"`Unexpected response structure:\n{response.text}`", parse_mode="markdown")
        else:
            await msg.edit(f"`Error {response.status_code}: Unable to fetch data from API.`", parse_mode="markdown")
    except Exception as e:
        await msg.edit(f"`An error occurred:\n{str(e)}`", parse_mode="markdown")

#====================================#
#====================================#

@ultroid_cmd(pattern="gptv2(?:\s|$)([\s\S]*)")
async def gpt4_v2_query(event):
    # Pre-message while processing
    msg = await event.eor("💤")

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

    # API parameters
    params = {'text': user_text}
    headers = {'accept': 'application/json'}
    
    try:
        # Sending the request to the API
        response = requests.get(API_V2, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'result' in data:
                result_text = data['result']
                
                # Check if the result exceeds the Telegram character limit
                if len(result_text) > 4095:
                    # Save the response as a text file
                    with open("gpt4_v2_response.txt", "w", encoding="utf-8") as file:
                        file.write(result_text)
                    
                    # Send the file and delete the initial processing message
                    await event.client.send_file(
                        event.chat_id,
                        "gpt4_v2_response.txt",
                        caption="**Response is too long, sent as a file.**",
                        parse_mode="markdown"
                    )
                    await msg.delete()
                else:
                    # Beautify and send the response if within limits
                    beautified_response = f"**Response:**\n\n{result_text}"
                    await msg.edit(beautified_response, parse_mode="markdown")
            else:
                await msg.edit(f"`Unexpected response structure:\n{response.text}`", parse_mode="markdown")
        else:
            await msg.edit(f"`Error {response.status_code}: Unable to fetch data from API.`", parse_mode="markdown")
    except Exception as e:
        await msg.edit(f"`An error occurred:\n{str(e)}`", parse_mode="markdown")

#====================================#
#====================================#