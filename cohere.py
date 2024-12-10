import os
import cohere
from . import ultroid_cmd

API_KEY = "hPZY8Tf8TXUZRK3jzuOZyz0atWR9q7IzywrK4hTQ"
co = cohere.Client(api_key=API_KEY)

@ultroid_cmd(pattern="cohere(?:\s|$)([\s\S]*)")
async def cohere_handler(event):
    # Fetching user input from reply or message
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        prompt = reply.text
    else:
        prompt = event.pattern_match.group(1)

    if not prompt:
        await event.eor("`Usage: .cohere [prompt/reply to message]`", parse_mode="markdown")
        return

    try:
        # Pre-message while processing
        msg = await event.eor("`Processing your query with Cohere...`", parse_mode="markdown")

        # Sending the request to Cohere
        response = co.chat(
            text=prompt,
            model="command-r-plus"
        )
        output = response.text

        # Handling long responses
        if len(output) > 4095:
            file_path = "cohere_response.txt"
            with open(file_path, "w", encoding="utf-8") as out_file:
                out_file.write(output)

            await event.client.send_file(
                event.chat_id,
                file_path,
                caption="**Response Limit Exceeded, Sending As File.**",
                parse_mode="markdown"
            )
            await msg.delete()
        else:
            await msg.edit(f"**Response:**\n\n{output}", parse_mode="markdown")
    except Exception as e:
        await event.eor(f"`An error occurred: {str(e)}`", parse_mode="markdown")
        