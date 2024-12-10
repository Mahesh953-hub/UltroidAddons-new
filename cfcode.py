import requests
from pyUltroid import cdB
from . import  ultroid_cmd, eor
from . import run_async
import os
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from . import ultroid_cmd, fast_download, check_filename
from io import BytesIO


CFAC = cdB.get_key("CFAC")
CFKEY = cdB.get_key("CFKEY")
CFM  = cdB.get_key("CFM")
API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{CFAC}/ai/run/"
headers = {"Authorization": f"Bearer {CFKEY}"}

@run_async
def run(model, inputs):
    input = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    resp = response.json()
    return resp['result']['response']

@ultroid_cmd(pattern="cfcode(?: (.+)|$)")
async def generate_code(event):
    reply_message = await event.get_reply_message()
    question = event.pattern_match.group(1)

    # Get question from the command or reply message
    if not question and reply_message:
        question = reply_message.message
    if not question:
        return await event.eor("Please provide a prompt or reply to a message for code generation.")

    inputs = [
        { "role": "system", 
          "content": """Your name is prom Comder, and your job is to create Telegram userbot plugins for Ultroid. You are specially designed for Ultroid Plugin Maker. You need to include necessary imports as shown in the example code. You must set a suitable Ultroid command and ensure that the command works on query or can be directly used with the command.You have been strictly prohibited to genrate random code, random commands, random things that not mentioned in the prompt. The sample code have been provided to you that contacts GPT and gives response but you don't have to genrate same. You have to genrate code only for given prompt. analyse the given sample code and set in your memory as sample code and this will be your base code for plugin making.Here is the sample code:

                ```
                from os import system, remove
                from io import BytesIO

                try:
                    import openai
                except ImportError:
                    system("pip install -q openai")
                    import openai

                from . import ultroid_cmd, check_filename, cdB, LOGS, fast_download, run_async

                @run_async
                def get_gpt_answer(gen_image, question, api_key):
                    openai.api_key = api_key
                    if gen_image:
                        x = openai.Image.create(
                            prompt=question,
                            n=1,
                            size="1024x1024",
                            user="arc",
                        )
                        return x["data"][0]["url"]
                    x = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": question}],
                    )
                    LOGS.debug(f'Token Used on ({question}) > {x["usage"]["total_tokens"]}')
                    return x["choices"][0]["message"]["content"].lstrip("+AFw-n")

                @ultroid_cmd(pattern="(chat)?gpt( (.*)|$)")
                async def openai_chat_gpt(e):
                    api_key = cdB.get_key("OPENAI_API")
                    gen_image = False
                    if not api_key:
                        return await e.eor("OPENAI_API key missing..")

                    args = e.pattern_match.group(3)
                    reply = await e.get_reply_message()
                    if not args:
                        if reply and reply.text:
                            args = reply.message
                    if not args:
                        return await e.eor("Gimme a Question to ask from ChatGPT")

                    moi = await e.eor(f"+2D3cIw")
                    if args.startswith("-i"):
                        gen_image = True
                        args = args[2:].strip()
                    try:
                        response = await get_gpt_answer(gen_image, args, api_key)
                    except Exception as exc:
                        LOGS.warning(exc, exc_info=True)
                        return await moi.edit(f"Error: +AFw-n> {exc}")
                    else:
                        if gen_image:
                            path, _ = await fast_download(
                                response, filename=check_filename("dall-e.png")
                            )
                            await e.client.send_file(
                                e.chat_id,
                                path,
                                caption=f"{args[:1020]}",
                                reply_to=e.reply_to_msg_id,
                            )
                            await moi.delete()
                            return remove(path)
                        if len(response) < 4095:
                            answer = f"<b></b>+AFw-n <i>{response}</i>"
                            return await moi.edit(answer, parse_mode="html")
                        with BytesIO(response.encode()) as file:
                            file.name = "gpt_response.txt"
                            await e.client.send_file(
                                e.chat_id, file, caption=f"{args[:1020]}", reply_to=e.reply_to_msg_id
                            )
                        await moi.delete()
                ```

                This is a sample code for chatgpt that only made for Ultroid. Keep in memory that this is SAMPLE CODE so genrate new code on this type of template like ultroid_cmd, function call, import etc. Add some beautification by yourself in response like emojis.
                You have been strictly adviced that you have to genrate code on given prompt/query or questions. You can't genrate plugin or code that doesn't meet with query or questions. Thats why you have been designed for. """
        },
        { "role": "user", "content": question }
    ]
    msg = await event.eor("Generating code...")
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