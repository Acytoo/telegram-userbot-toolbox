"""
Get chat id with name
"""
import json

from telethon import TelegramClient

from config import SESSION_NAME, API_ID, API_HASH
from config import CHAT_ID_FILE_NAME


async def get_list():
  dialogs = await client.get_dialogs(limit=None)
  name_id = {}
  for dialog in dialogs:
    name_id[dialog.entity.id] = dialog.name
  with open(CHAT_ID_FILE_NAME, "w", encoding="utf-8") as f:
    json.dump(name_id, f, indent=0, ensure_ascii=False)
  print("Done")

if __name__ == "__main__":
  client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
  with client:
    client.loop.run_until_complete(get_list())
