"""
Auto delete message in channel/groups
Auto reply with fixed words
"""
import os.path
import time
from random import randint
import asyncio
import json

from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChannel

from config import API_ID, API_HASH, SESSION_NAME, CMD_REPLY, CMD_DELETE, AUTO_DELETE_TIME, AUTO_DELETE_WAIT_TIME
from config import COMMAND_PREFIX, SAVED_CHANNEL_ID, CHAT_CONFIG_FILE, SELF_ID, CMD_LIST
from list_chat_ids import list_chat_ids

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
chats = [] # list of dict
id_name = {}
peer_self = PeerUser(SELF_ID)


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
        deactive_autodelete(channel_id)
        tmp_message = await event.reply("Automatic deletion deactivated")
      else:
        tmp_message = await event.reply("Automatic deletion deactivated")
    else:
      try:
        delete_time = int(cmd[1])
      except ValueError:
        delete_time = AUTO_DELETE_TIME
      active_autodelete(channel_id, delete_time)
      print("twice")
      tmp_message = await event.reply(f"Automatic deletion activated, set timer to {delete_time} minute(s)")
    await asyncio.sleep(3) # delete hint after 3 seconds
    await client.delete_messages(tmp_message.to_id, tmp_message.id)
  elif event.message.to_id == peer_self: # send to self, other commands
    if cmd[0] == CMD_LIST:
      await client.send_message(peer_self, get_auto_delete_chats())


def get_auto_delete_chats() -> str:
  res = "Auto delete chats:\n"
  for item in group_delete_time:
    res += f"{id_name[item]}: {group_delete_time[item]} minute(s)\n"
  return res


@client.on(events.NewMessage(outgoing=True)) # monitor outgoing messages
async def outgoing_message_handler(event):
  global group_delete_time
  if event.message.raw_text and event.message.raw_text[0] == COMMAND_PREFIX:
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
    for item in auto_delete_jobs[:]:
      if item[0] < int(time.time()):
        await client.delete_messages(item[1], item[2])
        auto_delete_jobs.remove(item)

def deactive_autodelete(channel_id: int) -> None:
  """
  Remove channel_id from dict, save info to file
  :param channel_id:
  :return:
  """
  global chats
  global group_delete_time
  group_delete_time.pop(channel_id)
  for item in chats:
    if item["id"] == channel_id:
      item["auto_delete"] = -1
  dump_config()

def active_autodelete(channel_id: int, delete_time: int) -> None:
  """
  Set auto_delete timer for channel_id, and save info to file
  :param channel_id:
  :param delete_time:
  :return:
  """
  global chats
  global group_delete_time
  group_delete_time[channel_id] = delete_time
  for item in chats:
    if item["id"] == channel_id:
      item["auto_delete"] = delete_time
  dump_config()


def load_config():
  """
  Load chat id name auto_delete information to chats: dict
  :return:
  """
  global chats
  if not os.path.exists(CHAT_CONFIG_FILE):
    list_chat_ids()
  with open(CHAT_CONFIG_FILE, "r", encoding="utf-8") as f:
    chats = json.load(f)
  for chat in chats:
    id_name[chat["id"]] = chat["name"]
    if chat["auto_delete"] > 0:
      group_delete_time[chat["id"]] = chat["auto_delete"]


def dump_config():
  """
  Dump chat info to json
  :return:
  """
  with open(CHAT_CONFIG_FILE, "w", encoding="utf-8") as f:
    json.dump(chats, f, indent=2, ensure_ascii=False)

def start():
  load_config()
  with client:
    client.loop.create_task(auto_delete(client))
    client.run_until_disconnected()


if __name__ == "__main__":
  start()
