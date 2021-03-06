"""
Configurations
Get your app api id and api hash from https://my.telegram.org/apps
"""

API_ID = 123345
API_HASH = "xxxxxxxxxxxxxxxxxxxxxxx"
SESSION_NAME = "acytoo client" # whatever you like

SELF_ID = 123456
TRASH_CHANNEL_ID = 123456 # Trash can, where deleted message send to
SAVED_CHANNEL_ID = 123456 # Saved messages
SELECTED_CHANNEL_ID = 123456 # Cleaned data channel
MONITORED_CHANNEL_IDS = [
  123456,
  123456
]

COMMAND_PREFIX = "&" # command prefix, if a message start with &, it's a command
AUTO_DELETE_TIME = 3 # in minutes, the message would be deleted at least 3 minutes after send
AUTO_DELETE_WAIT_TIME = 10 # in seconds, for every 10 seconds, check and delete message

CMD_REPLY = "autoreply"
CMD_DELETE = "autodelete"
CMD_LIST = "list"

CHAT_CONFIG_FILE = "chat_ids.json"
