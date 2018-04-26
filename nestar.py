import subprocess
import importlib
import requests
import glob
import json
import sys
import os

class PluginHandler:
	loaded = []

	def loadPlugins(self):
		if os.path.isdir("plugins"):
			sys.path.insert(0, './plugins')
			files = glob.glob("./plugins/*")
			plugins = [os.path.basename(x) for x in files if x[-2:] == "py"]

			for plugin in plugins:
				self.loaded.append(importlib.import_module(plugin[:-3]))

class TelegramExecption(Exception):
	pass

class NestarException(Exception):
	pass

class Nestar:
	config = {
		'token':None,
		'pluginHandler':PluginHandler(),
	}

	offset = None

	def __init__(self, token, endpoint='https://api.telegram.org'):
		if sys.version_info[0] < 3:
			reload(sys)
			sys.setdefaultencoding("utf-8")
		self.config['token'] = token
		self.config['endpoint'] = endpoint
		self.config['pluginHandler'].loadPlugins()

	def apiRequest(self, method, params):
		data = requests.post('{}/bot{}/{}'.format(self.config['endpoint'], self.config['token'], method), data=params).json()
		if data["ok"] == False:	raise TelegramExecption({"error_code":data["error_code"], "description":data["description"]})
		return data["result"]
	
	def loop(self, callback=0, php_handler=0):
		while 1:
			r = self.getUpdates(offset=self.offset, timeout=10)
			for update in r:
				if "update_id" in update:
					self.offset = update["update_id"] + 1
					
					if callback == 0 and self.config['pluginHandler'].loaded == [] and php_handler == 0:
						raise NestarException('No handler found')
					
					if php_handler == 0:
						if callback != 0:
							callback(self, update)
						if self.config['pluginHandler'].loaded != []:
							for plugin in self.config['pluginHandler'].loaded:
								if 'NestarPlugin' in dir(plugin):
									plugin.NestarPlugin().handle(self, update)
								else:
									raise NestarException('Invalid plugin "{}"'.format(plugin))
					else:
						data = str(subprocess.check_output(["php", php_handler, json.dumps(update)]))[2:][:-1]
						
						if data.startswith('nestarAnswer'):
							data = json.loads(data[12:])
							self.apiRequest(data["method"], data["params"])

	def __getattr__(self, method):
		def function(**kwargs):
			if 'reply_markup' in kwargs:	kwargs['reply_markup'] = json.dumps(kwargs['reply_markup'])
			if 'results' in kwargs:	kwargs['results'] = json.dumps(kwargs['results'])
			if 'mask_position' in kwargs:	kwargs['mask_position'] = json.dumps(kwargs['mask_position'])
			if 'shipping_options' in kwargs:	kwargs['shipping_options'] = json.dumps(kwargs['shipping_options'])
			return self.apiRequest(method, kwargs)
		return function
