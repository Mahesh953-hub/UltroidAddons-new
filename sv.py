import os
from telethon import events

@ultroid_cmd(pattern="sv$")
async def save_self_destruct_media(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        
        # Check if the message contains media (photo, video, etc.)
        if reply_message and (reply_message.photo or reply_message.video or reply_message.media):
            try:
                # Download the media (photo or video) to a temporary location
                media_path = await reply_message.download_media()
                
                # Forward the media to your saved messages with the caption "Saved self-destruct media by @PragalX"
                if media_path:
                    await event.client.send_file("me", media_path, caption="Saved self-destruct media by @PragalX")
                    
                    # Delete the temporary media file after forwarding
                    if os.path.exists(media_path):
                        os.remove(media_path)
                    
                    # Delete the command message and reply to prevent clutter
                    await event.delete()
                else:
                    await event.edit("Failed to download media.")
            except Exception as e:
                await event.edit(f"Error: {str(e)}")
        else:
            await event.edit("Reply to a self-destruct media (photo or video) message.")
    else:
        await event.edit("Please reply to a media message.")