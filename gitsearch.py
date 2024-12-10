"""
âœ˜ Commands Available

â€¢ `{i}gitsearch <query>`
    Search for a query on GitHub and return the results.
"""
import requests
from . import ultroid_cmd

GITHUB_API_URL = "https://api.github.com/search/repositories"

@ultroid_cmd(pattern="gitsearch ?(.*)")
async def git_search(event):
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        query = reply.text
    else:
        query = event.pattern_match.group(1)

    if not query:
        await event.eor("`ğŸ”� Please provide a search query or reply to a message!`")
        return

    msg = await event.eor("`Searching for repositories...`")

    try:
        response = requests.get(GITHUB_API_URL, params={"q": query})
        repos = response.json().get('items', [])

        if not repos:
            await msg.edit("`ğŸ˜¿ No results found for your query!`")
            return

        result = "ğŸ“� <b>Search Results:</b>\n"
        for repo in repos[:5]:  # Limit to top 5 results
            result += f"\nğŸ”— <a href='{repo['html_url']}'>{repo['name']}</a>  \n" \
                      f"â­�ï¸� Stars: {repo['stargazers_count']}  \n" \
                      f"ğŸ“„ Description: {repo['description'] or 'No description available.'}\n"

        await msg.edit(result, parse_mode="html")
    
    except Exception as exc:
        await msg.edit(f"ğŸš« An error occurred: {exc}")