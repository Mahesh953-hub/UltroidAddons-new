import requests
from . import ultroid_cmd, eor

@ultroid_cmd(pattern="hmod ?(.*)")
async def happymod_search(event):
    query = event.pattern_match.group(1)
    if not query or " " in query:
        await eor(event, "Please provide a single word prompt like 'whatsapp' or 'telegram'.")
        return

    # Sending the pre-message
    msg = await eor(event, f"Searching for **{query}** mod on Happymod...")

    # API URL
    url = f"https://widipe.com/happymod?query={query}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            # Extracting results
            results = data.get("result", [])
            if not results:
                await msg.edit(f"No results found for '{query}' on Happymod.")
                return
            
            # Preparing the message
            message = (f"<i>Top 10 results for '{query}' on Happymod:</i>\n\n")
            for i, result in enumerate(results[:10], start=1):
                title = result.get("title")
                link = result.get("link")
                message += f"<blockquote>{i}. <b>Title:</b> {title}\n   <b>Link:</b> <a href='{link}'>Click Here!</a></blockquote>\n\n"

            # Sending the results
            await msg.edit(message, parse_mode="html")
        else:
            await msg.edit("API is not responding or is currently unavailable. Please try again later.")
    except Exception as e:
        await msg.edit(f"An error occurred: {str(e)}")
