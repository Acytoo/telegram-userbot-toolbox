"""
Delete chat document
No backup, delete forever
"""

from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChannel

from config import SESSION_NAME, API_ID, API_HASH
from config import TRASH_CHANNEL_ID, SAVED_CHANNEL_ID


async def delete_media(client, target_chat):
  async for message in client.iter_messages(target_chat):
    await client.delete_messages(target_chat, message.id)
  print("Done")

if __name__ == "__main__":
  client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
  target_chat = PeerChannel(SAVED_CHANNEL_ID)
  with client:
    client.loop.run_until_complete(delete_media(client, target_chat))
