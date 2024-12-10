from telethon import functions, types
from . import ultroid_cmd, run_async, LOGS

@run_async
@ultroid_cmd(pattern="msgreq (.+)")
async def eval_message(e):
    try:
        # Get the message ID and other required details
        reply_to_msg_id = 64538
        quote_text = e.pattern_match.group(1)
        reply_to_peer_id = 7499308670
        
        # Send a message with reply
        await e.client(functions.messages.SendMessageRequest(
            peer=reply_to_peer_id,
            message=quote_text,
            reply_to=types.InputReplyToMessage(
                reply_to_msg_id=reply_to_msg_id,
                top_msg_id=reply_to_msg_id,
                reply_to_peer_id=reply_to_peer_id,
                quote_text=quote_text,
                quote_entities=[types.MessageEntityUnknown(
                    offset=42,
                    length=42
                )],
                quote_offset=42
            )
        ))
        
        await e.eor("Message sent successfully! ✉️")
        
    except Exception as exc:
        LOGS.warning(f'Error occurred: {exc}', exc_info=True)
        await e.eor(f"Something went wrong! ⚠️\n{exc}")