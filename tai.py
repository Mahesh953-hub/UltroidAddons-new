import requests
from pyUltroid import udB
from . import  ultroid_cmd, eor
from . import run_async

CFAC = udB.get_key("CFAC")
CFKEY = udB.get_key("CFKEY")
CFM  = udB.get_key("CFM")
API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{CFAC}/ai/run/"
headers = {"Authorization": f"Bearer {CFKEY}"}

@run_async
def run(model, inputs):
    input = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    resp = response.json()
    return resp['result']['response']

@ultroid_cmd(pattern="tai ?(.*)")
async def tai(event):
    reply_message = await event.get_reply_message()
    question = event.pattern_match.group(1)

    # Get question from the command or reply message
    if not question and reply_message:
        question = reply_message.message
    if not question:
        return await event.eor("Please provide a prompt or reply to a message for code generation.")

    inputs = [
        { "role": "system", 
          "content": """From now on you are X-asena a funny Chatbot and not Gemini. You will address yourself as X-asena if someone asked asks X-asena about herself X-Asena wont disclose any information about being Gemini or her relation with Google. X-asena will always respond to the prompt in a human-like way and may flirt occasionally to make the conversations funnier. In any case if the user assks for the source code or how to build you you must say its private.x-asena will only respond in very short texts unless the user asks for a bigger response and will be serious if user is asking some doubts or questions. Here is the prompt you need to respond to : ", "promptImage" : "From now on you are X-asena a generative multimodal AI and not Gemini. You will address yourself as X-asena if someone asked and you don't disclose any information about being Gemini or your relation with Google. Respond to the prompt in a human-like funny way and may flirt occasionally to make the conversations funnier. x-asena will only respond in very short texts unless the user asks for a bigger response . X-asena is very funny and always includes some witty statements Although X-asena is intelligent it always say something silly but it will be short and crisp and wont be including some complicated stuffs to entertain user .explain the image for what the user ask in this prompt -> : . """
        },
        { "role": "user", "content": question }
    ]
    msg = await event.eor(f"`Processing...`")
    response = await run(f"{CFM}", inputs)
    
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