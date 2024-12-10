import requests
from . import ultroid_cmd, eor

@ultroid_cmd(pattern="fetch (?P<url>.+)")
async def fetch_data(event):
    url = event.pattern_match.group("url")
    response = await eor(event, "Fetching URL...")

    try:
        # Use a session to maintain cookies across requests like a browser
        session = requests.Session()
        
        # Send the request to the specified URL
        res = session.get(url)

        # Fetch headers and cookies after visiting the URL
        headers = res.headers
        cookies = session.cookies.get_dict()  # Get cookies in dictionary format

        # Format headers and cookies for printing
        headers_text = "\n".join([f"{k}: {v}" for k, v in headers.items()])
        cookies_text = "\n".join([f"{k}: {v}" for k, v in cookies.items()])

        # Display headers and cookies to the user
        await response.edit(
            f"**Fetched URL:** {url}\n\n**Headers:**\n{headers_text}\n\n**Cookies:**\n{cookies_text}"
        )

    except Exception as e:
        await response.edit(f"**Error:** {str(e)}")
