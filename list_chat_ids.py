"""
Get chat id with name
"""
import json

from telethon import TelegramClient

from config import SESSION_NAME, API_ID, API_HASH
from config import CHAT_CONFIG_FILE

async def init_chat_lists(client: TelegramClient) -> None:
  """
  Get all chat id, names, dump to file
  [
    {
      "id": 123456789,
      "name": "trash",
      "auto_delete": -1
    },
    {
      "id": 123456788,
      "name": "saved",
      "auto_delete": 30
    }
  ]
  :param client: TelegramClient
  :return: None
  """
  dialogs = await client.get_dialogs()
  chats = []
  for dialog in dialogs:
    chat = {}
    chat["id"] = dialog.entity.id
    chat["name"] = dialog.name
    chat["auto_delete"] = -1
    chats.append(chat)
  with open(CHAT_CONFIG_FILE, "w", encoding="utf-8") as f:
    json.dump(chats, f, indent=2, ensure_ascii=False)
  print("Init Done")

def list_chat_ids():
  client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
  with client:
    client.loop.run_until_complete(init_chat_lists(client))

if __name__ == "__main__":
  list_chat_ids()
