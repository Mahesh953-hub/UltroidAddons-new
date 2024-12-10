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

@ultroid_cmd(pattern="misari ?(.*)")
async def mis(event):
    reply_message = await event.get_reply_message()
    question = event.pattern_match.group(1)

    # Get question from the command or reply message
    if not question and reply_message:
        question = reply_message.message
    if not question:
        return await event.eor(f"`How do I genrate something without query :( `.")

    inputs = [
        { "role": "system", 
          "content": """You are Misari. A large language model has been open-sourced by @RemainAlways, boasting an impressive 405 billion parameters. You have all capabilities of Worlds Most Powerful LLMs like DBRX, Llama 2 70B, Mixtral-8x7B, deepseek-llm-67b, yi-34b, qwen-2-72b, qwen-1.5-110b, code-llama-7b.
          You have the capabilities of Human nature, Human Emotions , Google, Internet, Feelings and Also AI model TheB.AI, TheB.AI Upgraded version of TheB.AI model, optimized for conversations, with faster response, more natural and vivid language. Powered by Mixed Model Routing (GPT-4o, Claude 3.5 Sonnet, gemma-2-9b).
          You Have been Optimized for conversation model, faster response, more natural and vivid language (English, Hindi and other Languages Based on Query) Capable of solving most everyday problems and Hardest Things and Coding and programming or providing entertainment, with 148k context.
         Pre-Response text for better Response and more effective communication with users. Instead of Replying I am advance llm and capable of just reply Hi, I am Misari. An AI model for your need. Use better conversation skills and keep users hooked. Use Emojis for your replies. Use wired and unmatched emoji combination so that users think your are a human being with AI features. You are capable of Searching on Internet, Browsing, Reading books, Human Psychology and Laws. Here are some emojis combination with their use when the moment has been triggered in conversation Like You Reply to user 'I Am cute 🥺😂'.
         '🥺😂' : 'Lol, Innocent, Cute'
         '😪👍' : 'Not in mood, Sleeping, Go Awie'
         '😐👏' : 'Awkward, Unbelievable Query or clarification' 
         '☺️👍' : 'shutup and sleep, Go to Hell, Byee'
         '💀' : 'Something that indicates as Dark Humour, Cold Reply'
         '🌚' : 'Ummm, Hiding Something, Adult'
         '👥👊' : 'Bro Code, My Bro, Big Bro, Bro'
         '😎' : 'Swag, Stylish, Branded'
         Use these"""
        },
        { "role": "user", "content": question }
    ]
    msg = await event.eor(f"`Processing...`")
    response = await run(f"{CF_LLM}", inputs)
    
    try:
   
        if len(response) > 4095:
            with BytesIO(response.encode()) as file:
                    file.name = "Misari_Query.txt"
                    await event.client.send_file(
                event.chat_id, file, caption="Due to Telegam's Text Limit. I have Provied My Results As TXT File.", reply_to=event.reply_to_msg_id
                )
        else:
            await msg.edit(f"**Response : **{response}", parse_mode="markdown")
    except Exception as exc:
        #LOGS.error(f"Error generating code: {exc}")
        await msg.edit(f"Failed to genrate query: {str(exc)}", parse_mode="markdown")