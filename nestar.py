import importlib
import requests
import glob
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
		'endpoint':'https://api.telegram.org',
		'pluginHandler':PluginHandler(),
	}

	offset = None

	def __init__(self, token):
		if sys.version_info[0] < 3:
			reload(sys)
			sys.setdefaultencoding("utf-8")
		self.config['token'] = token
		self.config['pluginHandler'].loadPlugins()

	def apiRequest(self, method, params):
		data = requests.post('{}/bot{}/{}'.format(self.config['endpoint'], self.config['token'], method), data=params).json()
		if data["ok"] == False:	raise TelegramExecption({"error_code":data["error_code"], "description":data["description"]})
		return data
	
	def loop(self, callback=0):
		while 1:
			r = self.getUpdates(offset=self.offset, timeout=10)
			for update in r["result"]:
				if "update_id" in update:
					self.offset = update["update_id"] + 1
					if callback == 0 and self.config['pluginHandler'].loaded == []:
						raise NestarException('No handler found')
					if callback != 0:
						callback(self, update)
					if self.config['pluginHandler'].loaded != []:
						for plugin in self.config['pluginHandler'].loaded:
							if 'NestarPlugin' in dir(plugin):
								plugin.NestarPlugin().handle(self, update)
							else:
								raise NestarException('Invalid plugin "{}"'.format(plugin))

	def __getattr__(self, method):
		def function(**kwargs):
			return self.apiRequest(method, kwargs)
		return function
