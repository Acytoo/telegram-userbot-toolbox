"""
Get chat id with name
"""

from telethon import TelegramClient

from config import SESSION_NAME, API_ID, API_HASH
from config import CHAT_ID_FILE_NAME


async def get_list():
  dialogs = await client.get_dialogs(limit=None)
  res = ""
  for dialog in dialogs:
    res += f"{dialog.name} | {dialog.entity.id}\n"
  with open(CHAT_ID_FILE_NAME, "w", encoding="utf-8") as f:
    f.write(res)
  print("Done")

if __name__ == "__main__":
  client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
  with client:
    client.loop.run_until_complete(get_list())
