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
bot.loop(handle)
```


_Plugin Sample_
```python
class NestarPlugin:
	def handle(self, bot, update):
		bot.sendMessage(chat_id=update["message"]["from"]["id"], text="Hi! Welcome to Nestar, {}".format(update["message"]["from"]["first_name"]))
```

_PHP Handler Sample_
```python
import nestar

bot = nestar.Nestar("YOUR:TOKEN")
bot.loop(php_handler="nestar.php")
```

```php
<?php
$update = json_decode($argv[1], true);

function apiRequest($method, $params){
        echo("nestarAnswer".json_encode(["method" => $method, "params" => $params]));
}

if($update["message"]["text"] == "/start"){
        apiRequest("sendMessage", ["chat_id" => $update["message"]["chat"]["id"], "text" => "hello"]);
}
```

_Notes_

You won't need an handler if there is at least one plugin in the _plugins_ folder.
