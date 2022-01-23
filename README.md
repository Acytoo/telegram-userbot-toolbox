## Telegram Tool Box

requirement: telethon, ```pip install telethon```

-------------------
1. Get telegram app api id and api hash from [my.telegram.org/apps](https://my.telegram.org/apps)
2. Update api_id and apt_hash in ```config.py```
3. Run ```python list_chat_ids.py``` get chat name and id
4. Update corresponding ids in ```config.py```
------------------------
```list_chat_id.py```: List all chat(user/channel/group) ids

```dedup.py```: Deduplicate files

```delete_messages.py```: Delete all messages

```forward_history_files.py```: Save history files to another channel

```chat_forwarder.py```: Forward all new chats in specific chats(channel/group/user)

```document_forwarder.py```: Save new files

```get_channel_files.py```: List all files [document id](https://tl.telethon.dev/constructors/document.html)

```auto_delete.py```: Delete messages automatically in specific group, 
send ```&autodelete [time in minutes]``` in target group to activate function, messages would be deleted after chosen time,
send ```&autodelete off``` to deactivate