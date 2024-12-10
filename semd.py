import os
import requests  # Make sure to install this with `pip install requests`
from . import *


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    return None


def send(fn):
    lst = ["plugins", "addons"]
    if not fn.endswith(".py"):
        fn += ".py"
    for i in lst:
        path = os.path.join(i, fn)
        if os.path.exists(path):
            return path
    else:
        return


def alt_send(fn):
    for k, v in LIST.items():
        for fx in v:
            if re.findall(fn, fx):
                return send(k)
    else:
        return


async def pastee(path):
    with open(path, "r") as f:
        data = f.read()
    err, linky = await get_paste(data)
    if err:
        return f"<b>>> <a href='https://spaceb.in/{linky}'>Pasted Here!</a></b> \n"
    else:
        LOGS.error(linky)
        return ""


@ultroid_cmd(pattern="semd ?(.*)")
async def semd_plugin(ult):
    repo = "https://github.com/TeamUltroid/Ultroid"
    args = ult.pattern_match.group(1)
    if not args:
        return await ult.eod("`Give a plugin name too`")

    eris = await ult.eor("`...`")
    path = send(args)
    if not path:
        path = alt_send(args)
    if not path:
        return await eris.edit(f"No plugins were found for: `{args}`")

    paste = await pastee(path)
    caption = (
        f"<b>>> </b><code>{path}</code> \n{paste} \n"
        f"© <a href='{repo}'>Team Ultroid</a>"
    )
    
    # Fetch custom thumbnail from cdB
    custom_thumbnail = cdB.get_key("CUSTOM_THUMBNAIL")
    if custom_thumbnail.startswith("http"):
        # If it's a URL, download the image
        download_path = "downloaded_thumbnail.jpg"  # Temporary local file path
        thumbnail_path = download_image(custom_thumbnail, download_path)
    else:
        thumbnail_path = custom_thumbnail if custom_thumbnail else "resources/extras/ultroid.jpg"

    try:
        await ult.client.send_file(
            ult.chat_id, path,
            caption=caption, parse_mode="html",
            thumb=thumbnail_path,
            silent=True, reply_to=ult.reply_to_msg_id,
        )
        await eris.delete()
    except Exception as fx:
        return await eris.edit(str(fx))
    finally:
        # Clean up the downloaded file
        if thumbnail_path == download_path and os.path.exists(download_path):
            os.remove(download_path)