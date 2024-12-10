import requests
from pyUltroid import cdB
from . import  ultroid_cmd, eor
from . import run_async

CFAC = cdB.get_key("CFAC")
MIS_KEY = cdB.get_key("MIS_KEY")
CF_LLM  = cdB.get_key("CF_LLM")
API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{CFAC}/ai/run/"
headers = {"Authorization": f"Bearer {MIS_KEY}"}

@run_async
def run(model, inputs):
    input = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    resp = response.json()
    return resp['result']['response']

@ultroid_cmd(pattern="theB ?(.*)")
async def mis(event):
    reply_message = await event.get_reply_message()
    question = event.pattern_match.group(1)

    # Get question from the command or reply message
    if not question and reply_message:
        question = reply_message.message
    if not question:
        return await event.eor(f"✨")

    inputs = [
        { "role": "system", 
          "content": """You are TheB 4.0. A Upgraded version of TheB.AI model, optimized for conversations, with faster response, more natural and vivid language. Powered by Mixed Model Routing (GPT-4o, Claude 3.5 Sonnet, Llama 3.1 405B)"""
        },
        { "role": "user", "content": question }
    ]
    msg = await event.eor(f"`Processing...`")
    response = await run(f"{CF_MIS}", inputs)
    
    try:
   
        if len(response) > 4095:
            with BytesIO(response.encode()) as file:
                    file.name = "generated_code.py"
                    await event.client.send_file(
                event.chat_id, file, caption="Here is your generated code.", reply_to=event.reply_to_msg_id
                )
        else:
            await msg.edit(f"**Response : **{response}", parse_mode="markdown")
    except Exception as exc:
        #LOGS.error(f"Error generating code: {exc}")
        await msg.edit(f"Failed to generate code :{str(exc)}", parse_mode="markdown")