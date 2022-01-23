"""
Forward chat history to another chat, aka backup
can specify document type
"""

import json

from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChannel

from config import SESSION_NAME, API_ID, API_HASH
from config import SAVED_CHANNEL_ID, SELECTED_CHANNEL_ID, DOCUMENT_ID_FILE_NAME

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

src_channel = PeerChannel(SAVED_CHANNEL_ID)
dst_channel = PeerChannel(SELECTED_CHANNEL_ID)
document_ids = []

# Video
async def forward_history(): # forward and then delete
  global document_ids
  print(len(document_ids))
  async for message in client.iter_messages(src_channel):
    if message.video and message.document.id not in document_ids:
      document_ids.append(message.document.id)
      await client.send_file(dst_channel, message.video) # send data to final channel
      await client.delete_messages(src_channel, message.id) # delete data from old channel
  print("Done")


if __name__ == "__main__":
  with open(DOCUMENT_ID_FILE_NAME, "r", encoding="utf-8") as f:
    document_ids = json.load(f)

  with client:
    client.loop.run_until_complete(forward_history())

  with open(DOCUMENT_ID_FILE_NAME, "w", encoding="utf-8") as f:
    json.dump(document_ids, f, indent=0)
