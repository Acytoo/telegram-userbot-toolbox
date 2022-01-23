"""
Auto delete message in channel/groups
Auto reply with fixed words
"""

import time
from random import randint
import asyncio

from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChannel

from config import API_ID, API_HASH, SESSION_NAME, CMD_REPLY, CMD_DELETE, AUTO_DELETE_TIME, AUTO_DELETE_WAIT_TIME
from config import COMMAND_PREFIX, SAVED_CHANNEL_ID

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

fixed_messages = [
  "好的",
  "谢谢",
  "嗯",
  "自动回复",
  "请等我回来"
]
auto_delete_jobs = [] # list of tuples (delete_time, to_id, message_id)
auto_reply = False # Auto Reply in private message only
group_delete_time = {} # dictionary, key: channel id; value: delete time for that channel

async def command_handler(event):
  global auto_reply
  global group_delete_time
  cmd = event.message.raw_text[1:].strip().split(" ")
  if cmd[0] == CMD_REPLY: # auto reply
    if cmd[1] == "on":
      auto_reply = True
    else:
      auto_reply = False
  elif cmd[0] == CMD_DELETE and isinstance(event.message.to_id, PeerChannel): # auto delete
    channel_id = event.message.to_id.channel_id
    if cmd[1] == "off":
      if channel_id in group_delete_time:
        group_delete_time.pop(channel_id)
        tmp_message = await event.reply("Automatic deletion deactivated")
      else:
        tmp_message = await event.reply("Automatic deletion deactivated")
    else:
      try:
        delete_time = int(cmd[1])
      except ValueError:
        delete_time = AUTO_DELETE_TIME
      group_delete_time[channel_id] = delete_time
      tmp_message = await event.reply(f"Automatic deletion activated, set timer to {delete_time} minute(s)")
    await asyncio.sleep(3) # delete hint after 3 seconds
    await client.delete_messages(tmp_message.to_id, tmp_message.id)


@client.on(events.NewMessage(outgoing=True)) # monitor outgoing messages
async def outgoing_message_handler(event):
  global group_delete_time
  if event.message.raw_text[0] == COMMAND_PREFIX:
    await command_handler(event)
    await client.delete_messages(event.message.to_id, event.message.id)
  to_id = event.message.to_id
  if isinstance(to_id, PeerChannel): # message send to channel/group
    channel_id = to_id.channel_id
    if channel_id in group_delete_time:
      auto_delete_jobs.append((int(time.time()) + group_delete_time[channel_id] * 60,
                               channel_id, event.message.id))


@client.on(events.NewMessage(incoming=True))
async def incoming_message_handler(event):
  global auto_reply
  if not auto_reply:
    return
  to_id = event.message.to_id
  if isinstance(to_id, PeerUser):
    await client.forward_messages(SAVED_CHANNEL_ID, event.message)
    await event.mark_read()
    await event.reply(fixed_messages[randint(0, len(fixed_messages) - 1)])


async def auto_delete(client):
  while True:
    await asyncio.sleep(AUTO_DELETE_WAIT_TIME)
    if len(auto_delete_jobs) == 0:
      continue
    while len(auto_delete_jobs) != 0 and auto_delete_jobs[0][0] <= int(time.time()):
      await client.delete_messages(auto_delete_jobs[0][1], auto_delete_jobs[0][2])
      auto_delete_jobs.pop(0)


def start():
  with client:
    client.loop.create_task(auto_delete(client))
    client.run_until_disconnected()


if __name__ == "__main__":
  start()
