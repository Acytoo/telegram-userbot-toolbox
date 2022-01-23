"""
Forward video files from a user/group/channel to saved channel
"""

from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.tl.types import PeerChannel

from config import SESSION_NAME, API_ID, API_HASH
from config import SAVED_CHANNEL_ID, MONITORED_CHANNEL_IDS

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
destination = PeerChannel(SAVED_CHANNEL_ID)


@client.on(events.NewMessage(incoming=True))
async def handler(event):
  # await event.mark_read() # Mark as read
  to_id = event.message.to_id
  if isinstance(to_id, PeerChannel): # channel/group
    if to_id.channel_id in MONITORED_CHANNEL_IDS and event.message.video: # only forward video from monitored groups
      await client.send_file(destination, event.message.video)

if __name__ == "__main__":
  with client:
    _ = client(UpdateStatusRequest(offline=True)) # not working if send messages
    client.run_until_disconnected()
