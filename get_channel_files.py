"""
Get channel file document id, save in file
"""
import json

from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChannel

from config import SESSION_NAME, API_ID, API_HASH
from config import MONITORED_CHANNEL_IDS
from utils import id_to_filename


async def get_file_info(client, channel_id):
  document_ids = []
  src_chat = PeerChannel(channel_id)
  async for message in client.iter_messages(src_chat):
    # only save video/gif ids
    # details: https://docs.telethon.dev/en/latest/quick-references/objects-reference.html#properties
    if message.video:
      document_ids.append(message.document.id)
  with open(id_to_filename(channel_id), "w", encoding="utf-8") as f:
    json.dump(document_ids, f, indent=0)

def dump_chat_file_id(channel_id):
  client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
  with client:
    client.loop.run_until_complete(get_file_info(client, channel_id))


if __name__ == "__main__":
  dump_chat_file_id(MONITORED_CHANNEL_IDS[0])