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
        