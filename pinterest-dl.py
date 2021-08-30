# Download all images in board

from py3pin.Pinterest import Pinterest as PinterestBase
import requests
import json
import shutil
import os
import sys
from pathlib import Path


class Pinterest(PinterestBase):

	def __init__(self, settings):
		super().__init__(username=settings['username'])

		self.path = os.path.join(Path(os.getcwd()).parent.absolute(), 'Pins')
		self.create_dir()
		self.boards = self.get_boards(settings['board_names'])
		self.downloaded_images = self.get_downloaded_images()
		self.new_downloads_count = 0

	def create_dir(self):
		if not os.path.exists(self.path):
			os.mkdir(self.path)

	def create_dir_board(self, board):
		path = os.path.join(self.path, board['name'])
		if not os.path.exists(path):
			os.mkdir(path)

		return path

	def get_boards(self, board_names):
		if not board_names:
			return self.boards()

		return [i for i in self.boards() if i['name'] in board_names]

	def get_downloaded_images(self):

		downloaded_images = []
		for folder in os.listdir(self.path):
			path = os.path.join(self.path, folder)
			if os.path.isfile(path):
				continue
			downloaded_images.extend([i.split('.')[0] for i in os.listdir(path)])

		return downloaded_images

	def delete_temp_files(self):
		data_path = os.path.join(os.getcwd(), 'data')
		if os.path.exists(data_path):
			shutil.rmtree(data_path)

	def get_board_pins(self, board):
		pins = []
		pin_batch = pinterest.board_feed(board_id=board['id'])
		while len(pin_batch) > 0:
			pins += pin_batch
			pin_batch = pinterest.board_feed(board_id=board['id'])

		return pins

	def download_image(self, url, path, name):
		response = requests.get(url,)
		if response.status_code == 200:
			print("Downloading:", name)
			with open(path, 'wb') as f:
				f.write(response.content)

			self.new_downloads_count += 1

	def download_boards(self):
		for board in self.boards:
			print('\n' + board['name'])

			path = self.create_dir_board(board)
			board['pins'] = self.get_board_pins(board)
			for pin in board['pins']:
				if pin['id'] in self.downloaded_images:
					print("Skipping:", pin['id'])
					continue
				try:
					url = pin['images']['orig']['url']
					extension = os.path.splitext(url)[1]
					self.download_image(url, f"{path}/{pin['id']}{extension}", pin['id'])
				except KeyError:
					pass

		print(f"\n{self.new_downloads_count} images were downloaded")


if __name__ == "__main__":
	settings = {
		"username": sys.argv[1],
		"board_names": sys.argv[2:]
	}
	print(f"Username: {settings['username']}")
	print(f"Boards: {settings['board_names'] or 'all'}")
	pinterest = Pinterest(settings)
	pinterest.download_boards()
