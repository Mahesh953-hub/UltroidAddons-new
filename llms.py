import requests
import asyncio
import random
import json
import os
from . import ultroid_cmd, eor

# List of all available models
MODELS = [
    "gpt-3", "gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini", "gpt-4", "gpt-4-turbo",
    "llama-2-7b", "llama-2-13b", "llama-3-8b", "llama-3-70b", "llama-3.1-8b", "llama-3.1-70b",
    "llama-3.1-405b", "llama-3.2-1b", "llama-3.2-3b", "llama-3.2-11b", "llama-3.2-90b",
    "llamaguard-7b", "llamaguard-2-8b", "mistral-7b", "mixtral-8x7b", "mixtral-8x22b",
    "mistral-nemo", "mixtral-8x7b-dpo", "hermes-3", "yi-34b", "phi-2", "phi_3_medium-4k",
    "phi-3.5-mini", "gemini-pro", "gemini-flash", "gemma-2b", "gemma-2b-9b", "gemma-2b-27b",
    "gemma-7b", "gemma-2", "gemma-2-27b", "claude-2.1", "claude-3-opus", "claude-3-sonnet",
    "claude-3-haiku", "claude-3.5-sonnet", "blackboxai", "blackboxai-pro", "command-r+",
    "dbrx-instruct", "sparkdesk-v1.1", "qwen", "qwen-1.5-0.5b", "qwen-1.5-7b",
    "qwen-1.5-14b", "qwen-1.5-72b", "qwen-1.5-110b", "qwen-1.5-1.8b", "qwen-2-72b",
    "glm-3-6b", "glm-4-9b", "yi-1.5-9b", "solar-mini", "solar-10-7b", "solar-pro",
    "deepseek", "llava-13b", "wizardlm-2-8x22b", "minicpm-llama-3-v2.5", "openchat-3.5",
    "openchat-3.6-8b", "phind-codellama-34b-v2", "dolphin-2.9.1-llama-3-70b", "cosmosrp",
    "german-7b", "tinyllama-1.1b", "cybertron-7b", "nemotron-70b"
]

BASE_MODEL = "gpt-4o-mini"
BASE_URL = "http://104.234.36.24:1337/v1/chat/completions"

headers = {
    "Content-Type": "application/json"
}

@ultroid_cmd(pattern="llms ?(.*)")
async def llms(event):
    reply = await event.get_reply_message()
    args = event.pattern_match.group(1) if not reply else reply.message
    if not args:
        await event.reply("`Please provide a prompt or reply to a message with the prompt.`")
        return

    # Set the default model and main prompt
    model = BASE_MODEL
    main_prompt = args.strip()

    # Check for random model selection or specified model flag
    if "-r" in args:
        model = random.choice(MODELS)
    elif "--" in args:
        model_flag = args.split("--")[1].split()[0].strip()
        if model_flag in MODELS:
            model = model_flag
            main_prompt = main_prompt.replace(f"--{model_flag}", "").strip()
        else:
            no_msg = await event.eor(f"`Specified model '{model_flag}' not found in MODELS. Using default model.`")
            await asyncio.sleep(2)
            await no_msg.delete()
            main_prompt = main_prompt.replace(f"--{model_flag}", "").strip()
            #return
    if "-r" or f"--{model_name}" in main_prompt:
    
        main_prompt = main_prompt.replace("-r", "").strip()
    else:
        main_prompt = main_prompt
    
    # Notify user of the selected model
    msg = await event.eor(f"`Processing your request with {model}.`")

    # Prepare the data for the API request
    data = {
        "model": model,
        "stream": False,
        "messages": [{"role": "assistant", "content": main_prompt}]
    }

    # Send the request to the API
    try:
        response = requests.post(BASE_URL, headers=headers, data=json.dumps(data)).json().get('choices', [])
        response_text = response[0].get('message', {}).get('content', '') if response else "No response received."

        # Handle response size and display or send as a file if needed
        if response_text and len(response_text) > 4096:
            file_path = "LLMs_Response.txt"
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response_text)
            await event.client.send_file(
                event.chat_id,
                file=file_path,
                caption="**Response exceeded limits, Sending as file.**",
                parse_mode="markdown"
            )
            os.remove(file_path)
            await msg.delete()
            
        elif response_text:
            await msg.edit(f"👾 Model: {model}\n⚡: {response_text}", parse_mode="markdown")
        else:
            await msg.edit("No response received.")
    except Exception as exc:
        await msg.edit(f"Error: {exc}")
