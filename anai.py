import requests
from . import ultroid_cmd

API_URL = "https://api.anonchatgpt.com/query?"

@ultroid_cmd(pattern="anai(?:\s|$)([\s\S]*)")
async def gpt4_query(event):
    msg = await event.eor("⚡")
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        user_text = reply.text
    else:
        user_text = event.pattern_match.group(1)
    if not user_text:
        await msg.edit("`Please provide the text after the command or reply to a message.`", parse_mode="markdown")
        return
    
    # API parameters
    params = {'queryText': f" {user_text}"}
    headers = {
        "Cookie": "_ga=GA1.1.783862639.1729873586; __gads=ID=bfbd48bd3ad52099:T=1729873590:RT=1729873590:S=ALNI_MYZi5DfvO-UJyV0er7d1OU6Lc0IxQ; __gpi=UID=00000f351bdbc806:T=1729873590:RT=1729873590:S=ALNI_Mb8W78A2EZrAjtYV19ZykvfDZsETA; __eoi=ID=cd4d4ba1a6507519:T=1729873590:RT=1729873590:S=AA-AfjaIb-iJUkDQ6AABJ9b1wITR; FCNEC=%5B%5B%22AKsRol-FuWogUlb283LMCVsBS9ZVrKpGipT2rWcvfe-e8WELBLN_biXWCV3_QnEnwOjmuoWzx7t66U3JyAHgNSSwohP2GNmKZGh47i8J1WMVE_3Ly4tmrzAMdIy3RmgJ_JxFpvyW5veKjtJliFiQINvQF_OF-SpnYw%3D%3D%22%5D%5D; _ga_TL9D1DRZ5H=GS1.1.1729873585.1.1.1729873621.0.0.0; session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiJhYWNjYTRjNi01ZmI2LTRkYjItYTQxZi1mZDZhZmMyZDZmN2UiLCJ2ZXJpZmllZEF0IjoxNzI5ODczNjI0NTE1LCJpYXQiOjE3Mjk4NzM2MjR9.vA-psb99jkOw9sx6s4wJ2Vd2_Vk2IXbvMdnyKyDNvH0",
        "Origin": "https://anonchatgpt.com",
        "Referer": "https://anonchatgpt.com",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    try:
        # Sending the request to the API
        response = requests.get(API_URL, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'responseText' in data:
                result_text = data['responseText']
                if len(result_text) > 4096:
                    with open("anai.txt", "w", encoding="utf-8") as file:
                        file.write(result_text)
                    await event.client.send_file(
                        event.chat_id,
                        "anai.txt",
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
        
#=============================#
#=============================#
