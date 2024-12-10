import random
import requests
from . import ultroid_cmd, eor

@ultroid_cmd(pattern="voicegen ?(.*)")
async def voice_generator(event):
    try:
        # Extract the command input and set defaults
        args = event.pattern_match.group(1)
        if "-m" not in args or len(args.split("-m")) < 2:
            await eor(event, "Usage: `.voicegen -m <model> <text>`\nExample: `.voicegen -m miku Hello!`")
            return

        # Parsing model type and text from the input
        model_flag_split = args.split("-m")
        model_and_text = model_flag_split[1].strip().split(" ", 1)
        
        if len(model_and_text) < 2:
            await eor(event, "Please specify a model and text. Example: `.voicegen -m miku Hello!`")
            return

        type = model_and_text[0].lower()
        text = model_and_text[1]
        
        # Generate random IP and User-Agent
        generate_random_ips = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        ins_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.1.2 Safari/602.3.12",
            "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36"
        ]
        random_ins_agent = random.choice(ins_agents)

        # Voice models dictionary
        models = {
            "miku": {"voice_id": "67aee909-5d4b-11ee-a861-00163e2ac61b", "voice_name": "Hatsune Miku"},
            "nahida": {"voice_id": "67ae0979-5d4b-11ee-a861-00163e2ac61b", "voice_name": "Nahida (Exclusive)"},
            "nami": {"voice_id": "67ad95a0-5d4b-11ee-a861-00163e2ac61b", "voice_name": "Nami"},
            "ana": {"voice_id": "f2ec72cc-110c-11ef-811c-00163e0255ec", "voice_name": "Ana(Female)"},
            "optimus_prime": {"voice_id": "67ae0f40-5d4b-11ee-a861-00163e2ac61b", "voice_name": "Optimus Prime"},
            "goku": {"voice_id": "67aed50c-5d4b-11ee-a861-00163e2ac61b", "voice_name": "Goku"},
            "taylor_swift": {"voice_id": "67ae4751-5d4b-11ee-a861-00163e2ac61b", "voice_name": "Taylor Swift"},
            "elon_musk": {"voice_id": "67ada61f-5d4b-11ee-a861-00163e2ac61b", "voice_name": "Elon Musk"},
            "mickey_mouse": {"voice_id": "67ae7d37-5d4b-11ee-a861-00163e2ac61b", "voice_name": "Mickey Mouse"},
            "kendrick_lamar": {"voice_id": "67add638-5d4b-11ee-a861-00163e2ac61b", "voice_name": "Kendrick Lamar"},
            "angela_adkinsh": {"voice_id": "d23f2adb-5d1b-11ee-a861-00163e2ac61b", "voice_name": "Angela Adkinsh"},
            "eminem": {"voice_id": "c82964b9-d093-11ee-bfb7-e86f38d7ec1a", "voice_name": "Eminem"}
        }
        
        # Check if voice model type is available
        if type not in models:
            await eor(event, f"Error: Model '{type}' not found.\nAvailable models: {', '.join(models.keys())}")
            return
        
        # Prepare request data and headers
        voice_id = models[type]['voice_id']
        ngeloot = {
            "raw_text": text,
            "url": "https://filme.imyfone.com/text-to-speech/anime-text-to-speech/",
            "product_id": "200054",
            "convert_data": [
                {
                    "voice_id": voice_id,
                    "speed": "1",  # default speed
                    "volume": "50",  # default volume
                    "text": text,
                    "pos": 0
                }
            ]
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'X-Forwarded-For': generate_random_ips,
            'User-Agent': random_ins_agent
        }

        # Make request to the TTS API
        response = requests.post('https://voxbox-tts-api.imyfone.com/pc/v1/voice/tts', json=ngeloot, headers=headers)
        response.raise_for_status()  # Raise exception for non-200 status
        data = response.json()
        
        # Get URL from response
        convert_result = data.get("data", {}).get("convert_result", [{}])[0]
        audio_url = convert_result.get("oss_url")
        
        # Reply to user with audio link
        if audio_url:
            reply_message = (
                f"**Voice Generation Successful**\n\n"
                f"**Model**: {models[type]['voice_name']} \n"
                f"**Voice ID**: `{voice_id}`\n"
                f"**Generated Voice URL**: [Click to Listen]({audio_url})\n"
            )
            await event.respond(reply_message, link_preview=False, reply_to=event.reply_to_msg_id or event.id)
        else:
            await eor(event, "Failed to retrieve the audio URL.")

    except Exception as e:
        await eor(event, f"Error: {str(e)}")
