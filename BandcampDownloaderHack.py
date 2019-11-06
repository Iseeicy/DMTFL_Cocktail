from ApplicationSettings import ApplicationSettings
from bandcampdl.bandcampdownloader import BandcampDownloader
from bandcampdl.bandcamp import Bandcamp
import os

class BandcampDownloaderHack:
	APPLICATION_SETTINGS = None


	def __init__(self, appsettings):
		global APPLICATION_SETTINGS

		APPLICATION_SETTINGS = appsettings
		print("Initialized BandcampDownloaderHack.")

	def download_bandcamp_track(self, track_link, destination):
		global APPLICATION_SETTINGS

		basedir = os.getcwd()
		template = APPLICATION_SETTINGS.get_setting("musicCacheTemplate")
		overwrite = False
		embedLyrics = False
		group = False
		embedArt = False
		noSlugify = False
		debug = True

		bandcamp = Bandcamp()
		downloader = BandcampDownloader(destination + template, basedir, overwrite, 
			embedLyrics, group,
			embedArt, noSlugify,
			debug, track_link)

		album = bandcamp.parse(track_link, embedArt, embedLyrics, debug)
		downloader.start(album)