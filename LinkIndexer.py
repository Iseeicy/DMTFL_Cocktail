from ApplicationSettings import ApplicationSettings
from bs4 import BeautifulSoup
import requests
import random
import urllib.request
import pickle

class LinkIndexer:
	APPLICATION_SETTINGS = None
	SITE_DICT = {}

	def __init__(self, appsettings):
		global APPLICATION_SETTINGS
		global SITE_DICT

		SITE_DICT = {}
		APPLICATION_SETTINGS = appsettings

		self.load_sitedict()

		print("Initialized LinkIndexer.")

	def load_sitedict(self):
		global APPLICATION_SETTINGS
		global SITE_DICT

		try:
			f = open(APPLICATION_SETTINGS.get_setting("filepathSiteIndex"), "rb")
			SITE_DICT = pickle.load(f)
			f.close()

			print("Loaded site index.")
		except FileNotFoundError:
			print('Warining: no site index. Run "indexsite" or "autorun" to generate this.')

		except IOError:
			print("CRITICAL ERROR: Python can't acccess site index file.")
			raise IOError()

	def write_sitedict(self):
		global APPLICATION_SETTINGS
		global SITE_DICT

		try:
			f = open(APPLICATION_SETTINGS.get_setting("filepathSiteIndex"), "wb")
			pickle.dump(SITE_DICT, f)
			f.close()
			print("Wrote to site index.")

		except IOError:
			print("CRITICAL ERROR: Python can't write site index file.")
			raise IOError()




	def get_site_dict(self):
		global SITE_DICT
		return SITE_DICT




	def index_site(self):
		new_links = self.index_album_links()
		for link in new_links:
			self.index_album_track_links(link)
		

	def index_album_links(self):
		global APPLICATION_SETTINGS
		global SITE_DICT

		print("Starting album index process...")
		response = requests.get(APPLICATION_SETTINGS.get_setting("baseURL"))
		soup = BeautifulSoup(response.text, "html.parser")
		print("Recieved web response...")


		list_items = soup.find_all("li", {"class": "music-grid-item square"})
		new_links = []

		for item in list_items:
			link = item.find("a")["href"]

			if self.add_album_link(link):
				new_links.append(link)
				print("Found new album: " + link)

		print("Added " + str(len(new_links)) + " new links to index.")
		self.write_sitedict()

		return new_links

	def index_album_track_links(self, album_link):
		global APPLICATION_SETTINGS
		global SITE_DICT

		print("Starting album track index process...")
		response = requests.get(APPLICATION_SETTINGS.get_setting("baseURL") + album_link)
		soup = BeautifulSoup(response.text, "html.parser")
		print("Recieved web response...")


		list_items = soup.find_all("div", {"class": "title"})
		new_tracks = []

		for item in list_items:
			link = item.find("a")["href"]

			if self.add_track_link(album_link, link):
				new_tracks.append(link)
				print("Found new track: " + link)

		print("Added " + str(len(new_tracks)) + " new track links to index.")
		self.write_sitedict()

		return new_tracks


	def add_album_link(self, album_link):
		global SITE_DICT

		if not album_link in SITE_DICT:
			SITE_DICT[album_link] = []
			return True

		else:
			return False

	def add_track_link(self, album_link, track_link):
		global SITE_DICT

		if not album_link in SITE_DICT:
			SITE_DICT[album_link] = []

		if not track_link in SITE_DICT[album_link]:
			SITE_DICT[album_link].append(track_link)
			return True
		else:
			return False

	def get_random_songs(self, song_count):
		dict = self.get_site_dict()
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

	def get_random_song(self):
		dict = self.get_site_dict()
		keys = list(dict.keys())


		for x in range(0, 900):
			album = random.choice(keys)
			if len(dict[album]) > 0:
				song = random.choice(dict[album])
				return song

		print("CRITICAL ERROR: track arrays are empty?")
		return
