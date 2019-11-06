import os

class ApplicationSettings:
	SETTINGS_FILE_PATH = ""
	SETTINGS = {}

	def __init__(self, settings_path):
		global SETTINGS_FILE_PATH
		global SETTINGS

		SETTINGS = {}
		SETTINGS_FILE_PATH = settings_path
		self.load_settings()


	def load_settings(self):
		global SETTINGS_FILE_PATH
		global SETTINGS

		try:
			f = open(SETTINGS_FILE_PATH, "r")
			lines = f.readlines()
			f.close()

			SETTINGS = {}
			for line in lines:
				equalsIndex = line.find("=")
				if equalsIndex != -1:
					key = line[:equalsIndex].strip()
					value = line[equalsIndex + 1:].strip()
					SETTINGS[key] = value


			print("Loaded settings file.")

		except FileNotFoundError:
			print('Couldn\'t find settings file, writing new one.')
			self.load_default_settings()
			self.write_settings()

		except IOError:
			print("CRITICAL ERROR: Python can't acccess settings file.")
			raise IOError()


	def write_settings(self):
		global SETTINGS_FILE_PATH
		global SETTINGS

		try:
			f = open(SETTINGS_FILE_PATH, "w")
			lines = []
			
			for key in SETTINGS.keys():
				lines.append(key + "=" + SETTINGS[key] + "\n")

			f.writelines(lines)
			f.close()

		except IOError:
			print("CRITICAL ERROR: Python can't write settings file.")
			raise IOError()


	def load_default_settings(self):
		global SETTINGS

		SETTINGS["filepathSiteIndex"] = "site_index.icy"
		SETTINGS["baseURL"] = "https://dmttapes.bandcamp.com"
		SETTINGS["musicCacheTemplate"] = "%{artist} - %{title}"
		SETTINGS["playlistLength"] = "5"




	def get_setting_keys(self):
		global SETTINGS

		return SETTINGS.keys()

	def get_setting(self, key):
		global SETTINGS

		return SETTINGS[key]

	def set_setting(self, key, value):
		global SETTINGS

		SETTINGS[key] = value
		self.write_settings()