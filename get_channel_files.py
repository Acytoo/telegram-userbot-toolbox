"""
Get channel file document id, save in file
"""
import json

from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChannel

from config import SESSION_NAME, API_ID, API_HASH
from config import DOCUMENT_ID_FILE_NAME, MONITORED_CHANNEL_IDS

document_ids = []
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
# src_chat = PeerUser(TARGET_USER)
src_chat = PeerChannel(MONITORED_CHANNEL_IDS[0])

async def get_file_info():
  async for message in client.iter_messages(src_chat):
    # only save video ids
    # details: https://docs.telethon.dev/en/latest/quick-references/objects-reference.html#properties
    if message.video:
      document_ids.append(message.document.id)


with client:
  client.loop.run_until_complete(get_file_info())

with open(DOCUMENT_ID_FILE_NAME, "w", encoding="utf-8") as f:
  json.dump(document_ids, f, indent=0)
