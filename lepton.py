import requests
from . import ultroid_cmd

API_URL = "https://widipe.com/lepton"

@ultroid_cmd(pattern="lepton(?:\s|$)([\s\S]*)")
async def gpt4_query(event):
    # Pre-message while processing
    msg = await event.eor("💕")

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
            if 'answer' in data:
                result_text = data['answer']
            #elif
               # result_text = data['answer']
                
                # Check if the result exceeds the Telegram character limit
                if len(result_text) > 4095:
                    # Save the response as a text file
                    with open("lepton.txt", "w", encoding="utf-8") as file:
                        file.write(result_text)
                    
                    # Send the file and delete the initial processing message
                    await event.client.send_file(
                        event.chat_id,
                        "lepton.txt",
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
        await msg.edit(f"`An error occurred:\n{e}`", parse_mode="markdown")