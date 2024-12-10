import requests
from telethon import events
from telethon.tl.types import MessageEntityTextUrl
from io import BytesIO
import asyncio
from . import ultroid_cmd, eor

@ultroid_cmd(pattern="git ?(.*)")
async def git_handler(event):
    args = event.pattern_match.group(1)
    if args.startswith("-u "):
        # Fetch user details
        username = args.split("-u ")[1]
        await fetch_user_details(event, username)
    elif args.startswith("-z "):
        # Download repo as ZIP
        repo_url = args.split("-z ")[1]
        await download_repo_zip(event, repo_url)
    elif args.startswith("-s "):
        # Search for repos
        query = args.split("-s ")[1]
        await search_repositories(event, query)
    elif args.startswith("-c "):
        # Search for code snippets
        code_query = args.split("-c ")[1]
        await search_code(event, code_query)
    else:
        await event.reply("Invalid command!\n Use `.git -u username`,\n `.git -z repo_url`, \n `.git -s search_term`, \n `.git -c code_query`.")

async def fetch_user_details(event, username):
    try:
        url = f"https://api.github.com/users/{username}"
        user_data = requests.get(url).json()
        
        if "message" in user_data:
            await event.reply(f"Error: {user_data['message']}")
            return
        
        # Prepare user details message
        name = user_data.get("name", "N/A")
        bio = user_data.get("bio", "N/A")
        repos = user_data.get("public_repos", "N/A")
        followers = user_data.get("followers", "N/A")
        following = user_data.get("following", "N/A")
        stars = fetch_starred_count(username)
        
        userss = await event.reply(f"`Searching User {username} on Git`")
        user_details = f"**^^🎀 GitHub User**: `{username}`\n" \
                       f"**📝 Name**: {name}\n" \
                       f"**📒 Bio**: {bio}\n" \
                       f"**⛓️ Repos**: {repos}\n" \
                       f"**⭐ Stars**: {stars}\n" \
                       f"**🧏 Followers**: {followers}\n" \
                       f"**🙇 Following**: {following}\n" \
                       f"**🌚 URL**: [GitHub Profile]({user_data['html_url']})^^"
        
        await userss.edit(user_details, link_preview=False)
    except Exception as e:
        await userss.edit(f"`An error occurred: {str(e)}`")

def fetch_starred_count(username):
    url = f"https://api.github.com/users/{username}/starred"
    starred_repos = requests.get(url).json()
    return len(starred_repos) if isinstance(starred_repos, list) else "N/A"

async def download_repo_zip(event, repo_url):
    try:
        owner_repo = repo_url.replace("https://github.com/", "")
        api_url = f"https://api.github.com/repos/{owner_repo}"
        
        repo_data = requests.get(api_url).json()
        
        if "message" in repo_data:
            await event.reply(f"Error: {repo_data['message']}")
            return
        
        default_branch = repo_data.get("default_branch", "main")
        repo_name = owner_repo.split("/")[-1]
        
        zip_url = f"{repo_url}/archive/refs/heads/{default_branch}.zip"
        zip_data = requests.get(zip_url)
        zipp = await event.reply(f"`Downloading repo as ZIP`")
        await asyncio.sleep(2)
        if zip_data.status_code == 200:
            file = BytesIO(zip_data.content)
            file.name = f"{repo_name}.zip"
            await event.client.send_file(event.chat_id, file, caption=f"Downloaded ZIP of {repo_name}")
            await zipp.delete()
        else:
            await zipp.edit("`Failed to download the repository as ZIP. Please check the URL or try again.`")
    except Exception as e:
        await zipp.edit(f"`An error occurred: {str(e)}`")

async def search_repositories(event, query):
    try:
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
        search_results = requests.get(url).json()
        
        if "items" not in search_results:
            await event.reply("`No repositories found.`")
            return
        searchh = await event.reply(f"`Searching for {query} ...`") 
        repos = search_results["items"][:10] 
        result_text = f"<b>🗃️ Search Results for</b> <code>{query}</code>:\n\n"
        
        for repo in repos:
            repo_name = repo["full_name"]
            stars = repo["stargazers_count"]
            forks = repo["forks_count"]
            last_update = repo["updated_at"]
            description = repo["description"] or "No description"
            description = description[:60] + "..." if len(description) > 60 else description
            
            result_text += f"<blockquote>• <a href='https://github.com/{repo_name}'>{repo_name}</a> - ⭐ {stars} : 🍴 {forks}\n" \
                           f"  <b>♻️ Update:</b> <em>{last_update}</em>\n" \
                           f"  <b>📚 Desc:</b> <em>{description}</em></blockquote>\n" \
        
        if len(search_results["items"]) > 5:
            result_text += f"<blockquote><a href='https://github.com/search?q={query}'>View All</a></blockquote>"
        
        await searchh.edit(result_text, link_preview=False, parse_mode="html")
    except Exception as e:
        await searchh.edit(f"`An error occurred: {str(e)}`")

async def search_code(event, code_query):
    searchc = await event.reply(f"`Searching code for {code_query} ...`") 
    try:
        url = f"https://api.github.com/search/code?q={code_query}+in:file"
        
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {cdB.get_key('GIT_AUTH_TOKEN')}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        code_results = requests.get(url, headers=headers).json()
        
        if "items" not in code_results:
            await searchc.edit(f"`No code snippets found. Full Error:\n{code_results}`")
            return

        total_count = code_results.get("total_count", 0)
        if total_count >= 1_000_000:
            human_readable_total = f"{total_count // 1_000_000}M"
        elif total_count >= 1000:
            human_readable_total = f"{total_count // 1000}k"
        else:
            human_readable_total = str(total_count)

        codes = code_results["items"][:10]  
        result_text = f"<b>📄 Code Search Results for</b> <code>{code_query}</code>:\n<b>Total:</b> {human_readable_total}\n\n"
        
        for code in codes:
            repo_name = code["repository"]["full_name"]
            file_name = code["name"]
            file_url = code["html_url"]
            
            result_text += f"<blockquote>• <a href='{file_url}'>{file_name}</a> in <a href='https://github.com/{repo_name}'>{repo_name}</a></blockquote>\n\n"
        
        await searchc.edit(result_text, link_preview=False, parse_mode="html")
    except Exception as e:
        await searchc.edit(f"`An error occurred: {str(e)}`")
