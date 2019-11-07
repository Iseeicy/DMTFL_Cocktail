from LinkIndexer import LinkIndexer
from ApplicationSettings import ApplicationSettings
from BandcampDownloaderHack import BandcampDownloaderHack
from datetime import datetime
from mutagen.mp3 import MP3
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
	command_names = ["autorun", "indexsite", "generate", "generatelength", "printsettings", "exit"]
	command_funcs = [command_autorun, command_index_site, command_generate, command_generate_length, command_printsettings, command_exit]

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

	
	songs = LINK_INDEXER.get_random_songs(int(APPLICATION_SETTINGS.get_setting("playlistLength")))
	baseURL = APPLICATION_SETTINGS.get_setting("baseURL")
	track_destination = datetime.now().strftime('%Y-%m-%d %H %M %S') + "/"
	print("Picked songs...")


	for x in songs:
		print("Downloading " + x)
		BANDCAMP_DOWNLOADER.download_bandcamp_track(baseURL + x, track_destination)

	print("Done!")

def command_generate_length():
	global APPLICATION_SETTINGS
	global LINK_INDEXER
	global BANDCAMP_DOWNLOADER

	def get_audio_length(mp3_path):
		audio = MP3(mp3_path)
		return audio.info.length

	baseURL = APPLICATION_SETTINGS.get_setting("baseURL")
	track_destination = datetime.now().strftime('%Y-%m-%d %H %M %S') + "/"

	desired_length = -1
	input_done = False
	while(not input_done):
		try:
			inp = input(">Enter desired length in seconds (or type exit):\n")
			if inp == "exit":
				return
			desired_length = float(inp)
			input_done = True
		except Exception as e:
			print("Invalid input entered.\n")
			pass
		

	current_length = 0

	while(True):
		song = LINK_INDEXER.get_random_song()
		print("Downloading " + song)
		path = BANDCAMP_DOWNLOADER.download_bandcamp_track(baseURL + song, track_destination)
		length = get_audio_length(path[:-4])
		current_length += length

		if current_length >= desired_length:
			print("Done!")
			return


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