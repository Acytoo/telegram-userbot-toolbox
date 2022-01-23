"""
Delete duplicate documents in channel/group chat
Documents are backed up in trash can before deletion
"""

from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChannel

from config import SESSION_NAME, API_ID, API_HASH
from config import TRASH_CHANNEL_ID, SAVED_CHANNEL_ID


async def dedup(client, target_chat, trash_channel=PeerChannel(TRASH_CHANNEL_ID)):
  document_id_set = set()
  async for message in client.iter_messages(target_chat):
    if message.video: # video, audio, photo, etc
      if message.document.id in document_id_set:
        await client.send_file(trash_channel, message.video) # backup
        await client.delete_messages(target_chat, message.id) # delete the message
      else:
        document_id_set.add(message.document.id)
  print("Done")

if __name__ == "__main__":
  client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
  target_chat = PeerChannel(SAVED_CHANNEL_ID) # deduplicate documents in saved channel
  with client:
    client.loop.run_until_complete(dedup(client, target_chat))


