# Download all images in board

from py3pin.Pinterest import Pinterest
import requests
import json
import os 

download_dir = os.getcwd() + '/pinterest/'

if not os.path.exists(download_dir):
	os.mkdir(download_dir)

pinterest = Pinterest(username='username')  # YOUR USERNAME

boards = pinterest.boards()


for target_board in boards: 

	print('\n', target_board['name'], "\n")

	board_pins = []
	pin_batch = pinterest.board_feed(board_id=target_board['id'])


	download_dir = os.getcwd() + '/pinterest/' + target_board['name'] + '/' 

	if not os.path.exists(download_dir):
		os.mkdir(download_dir)

	while len(pin_batch) > 0:
		board_pins += pin_batch
		pin_batch = pinterest.board_feed(board_id=target_board['id'])


	def download_image(url, path, name):
		r = requests.get(url=url, stream=True)
		if r.status_code == 200:
			print("Downloading:", name)
			with open(path, 'wb') as f:
				for chunk in r.iter_content(1024):
					f.write(chunk)

	for pin in board_pins:

		if pin['id'] in ' '.join(os.listdir(download_dir)):
			print("Skipping:", pin['id'])
			continue

		try: 
			url = pin['images']['orig']['url']
			indx = str(url).rfind('.')
			extension = str(url)[indx:]
			download_image(url, download_dir + pin['id'] + extension, pin['id'])
		except KeyError: 
			pass