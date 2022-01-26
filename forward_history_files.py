"""
Forward chat history to another chat, aka backup
can specify document type
"""

import json
import os

from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChannel

from config import SESSION_NAME, API_ID, API_HASH
from config import SAVED_CHANNEL_ID, SELECTED_CHANNEL_ID, MONITORED_CHANNEL_IDS
from get_channel_files import dump_chat_file_id
from utils import id_to_filename


# Forward Video
async def forward_history(client, src_channel_id, dst_channel_id, document_ids,
                          ignore_existing=False, delete_after_send=False):

  src_channel = PeerChannel(src_channel_id)
  dst_channel = PeerChannel(dst_channel_id)
  async for message in client.iter_messages(src_channel):
    if message.video and message.document.id not in document_ids:
      document_ids.append(message.document.id)
      await client.send_file(dst_channel, message.video) # send data to final channel
      if delete_after_send:
        await client.delete_messages(src_channel, message.id) # delete data from old channel

  dst_channel_files = id_to_filename(dst_channel_id)
  with open(dst_channel_files, "w", encoding="utf-8") as f:
    json.dump(document_ids, f, indent=0)
  print("Done")


def forward_history_files(src_channel_id, dst_channel_id):
  dst_channel_files = id_to_filename(dst_channel_id)
  if not os.path.exists(dst_channel_files):
    dump_chat_file_id(dst_channel_id)
  with open(dst_channel_files, "r", encoding="utf-8") as f:
    document_ids = json.load(f)
  client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
  with client:
    client.loop.run_until_complete(forward_history(client, src_channel_id, dst_channel_id, document_ids))


if __name__ == "__main__":
  forward_history_files(MONITORED_CHANNEL_IDS[0], SAVED_CHANNEL_ID)

