"""
Forward chat history to another chat, aka backup
can specify document type
"""

import json
import os
from typing import List

from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChannel

from config import SESSION_NAME, API_ID, API_HASH
from get_channel_files import dump_chat_file_id
from utils import id_to_filename


# Forward Video
async def forward_history(client, src_channel_id: int, dst_channel_id: int,
                          document_ids: List,
                          ignore_existing: bool, delete_after_send: bool) -> None:
  """
  forward history file(currently video only)
  :param client:
  :param src_channel_id: int, source channel id
  :param dst_channel_id: int, destination channel id
  :param document_ids: List of document ids
  :param ignore_existing: bool, if true: forward all files; if false: forward new files only
  :param delete_after_send: bool, if true: delete original message after send
  :return: None
  """
  src_channel = PeerChannel(src_channel_id) # channel only, src = PeerUser() if user as source
  dst_channel = PeerChannel(dst_channel_id) # destination channel
  async for message in client.iter_messages(src_channel): # iterate messages in source channel
    if message.video and message.document.id not in document_ids: # forward videos, deduplicated
      document_ids.append(message.document.id) # add document ids to List, dedup
      await client.send_file(dst_channel, message.video) # send data to destination channel
      if delete_after_send:
        await client.delete_messages(src_channel, message.id) # delete data from old channel

  if ignore_existing:
    # if ignore existing, skip dumping filename
    dst_channel_files = id_to_filename(dst_channel_id)
    with open(dst_channel_files, "w", encoding="utf-8") as f:
      json.dump(document_ids, f, indent=0)
  print("Done")


def forward_history_files(src_channel_id: int, dst_channel_id: int,
                          ignore_existing=False, delete_after_send=False) -> None:
  """
  Forward history file to another chat
  :param src_channel_id:
  :param dst_channel_id:
  :param ignore_existing:
  :param delete_after_send:
  :return:
  """
  if not ignore_existing:
    dst_channel_files = id_to_filename(dst_channel_id) # get existing_file name
    if not os.path.exists(dst_channel_files): # if file not exist, dump files' name
      dump_chat_file_id(dst_channel_id)
    with open(dst_channel_files, "r", encoding="utf-8") as f:
      document_ids = json.load(f) # load existing file names
  else:
    document_ids = [] # ignore existing

  client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
  with client:
    client.loop.run_until_complete(forward_history(client, src_channel_id,
                                                   dst_channel_id,
                                                   document_ids,
                                                   ignore_existing,
                                                   delete_after_send))


if __name__ == "__main__":
  from config import SAVED_CHANNEL_ID, SELECTED_CHANNEL_ID, MONITORED_CHANNEL_IDS
  forward_history_files(MONITORED_CHANNEL_IDS[0], SAVED_CHANNEL_ID)

