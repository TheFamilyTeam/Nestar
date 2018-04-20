# Nestar
![python](https://img.shields.io/badge/python-2.7,%203.x-red.svg)
[![telegram](https://img.shields.io/badge/Telegram-Channel-blue.svg)](https://t.me/TheFamilyTeam)

Python Framework for Telegram's Bot API 

# Dependence
* [requests](https://pypi.org/project/requests/)

Install it this way:

```
pip install requests
```

# Usage
_Bot Sample_
```python
import nestar

def handle(bot, update):
	print(update)

bot = nestar.Nestar("YOUR:TOKEN")
bot.getUpdates()
```


_Plugin Sample_
```python
class NestarPlugin:
	def handle(self, bot, update):
		bot.apiRequest("sendMessage", chat_id=update["message"]["from"]["id"], text="Hi! Welcome to Nestar, {}".format(update["message"]["from"]["first_name"]))
```

You won't need an handler if there is at least one plugin in the _plugins_ folder.
