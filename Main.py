from LinkIndexer import LinkIndexer
from ApplicationSettings import ApplicationSettings
from BandcampDownloaderHack import BandcampDownloaderHack
from datetime import datetime
import random
import os

SETTINGS_FILEPATH = "settings.cfg"
APPLICATION_SETTINGS = None
LINK_INDEXER = None
BANDCAMP_DOWNLOADER = None



def load_settings():
	global APPLICATION_SETTINGS
	global SETTINGS_FILEPATH

	APPLICATION_SETTINGS = ApplicationSettings(SETTINGS_FILEPATH)

def load_classes():
	global APPLICATION_SETTINGS
	global LINK_INDEXER
	global BANDCAMP_DOWNLOADER

	LINK_INDEXER = LinkIndexer(APPLICATION_SETTINGS)
	BANDCAMP_DOWNLOADER = BandcampDownloaderHack(APPLICATION_SETTINGS)

def display_main_options():
	command_names = ["autorun", "indexsite", "generate", "printsettings", "exit"]
	command_funcs = [command_autorun, command_index_site, command_generate, command_printsettings, command_exit]

	choice = input("\nEnter a command [" + ", ".join(command_names) + "]\n")
	found_command = False
	print()

	for x in range(0, len(command_names)):
		if choice == command_names[x]:
			command_funcs[x]()
			found_command = True
	
	if not found_command:
		print("Error: no command for \"" + choice + "\" found.")



## COMMANDS ##

def command_autorun():
	command_index_site()
	command_generate()

def command_index_site():
	global LINK_INDEXER

	LINK_INDEXER.index_site()

def command_generate():
	global APPLICATION_SETTINGS
	global LINK_INDEXER
	global BANDCAMP_DOWNLOADER

	def get_random_songs(song_count):
		dict = LINK_INDEXER.get_site_dict()
		keys = list(dict.keys())
		output = []

		for x in range(0, song_count):
			album = random.choice(keys)
			if len(dict[album]) > 0:
				song = random.choice(dict[album])
				output.append(song)
			else:
				x -= 1

		return output

	songs = get_random_songs(int(APPLICATION_SETTINGS.get_setting("playlistLength")))
	baseURL = APPLICATION_SETTINGS.get_setting("baseURL")
	track_destination = datetime.now().strftime('%Y-%m-%d %H %M %S') + "/"
	print("Picked songs...")


	for x in songs:
		print("Downloading " + x)
		BANDCAMP_DOWNLOADER.download_bandcamp_track(baseURL + x, track_destination)

	print("Done!")

def command_printsettings():
	global APPLICATION_SETTINGS

	for key in APPLICATION_SETTINGS.get_setting_keys():
		print(key + "|" + APPLICATION_SETTINGS.get_setting(key))

def command_exit():
	exit()







if __name__ == '__main__':
	print("======================================")
	print("           -| DMTFL_RADIO |-           ")
	print("              version 0.1              ")
	print("    https://dmttapes.bandcamp.com      \n")
	print("           Script by Iseeicy           ")
	print("======================================")

	load_settings()
	load_classes()

	while(True):
		display_main_options()