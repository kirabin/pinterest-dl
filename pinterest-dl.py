# Download all images in board

from py3pin.Pinterest import Pinterest
import requests
import json
import shutil
import os 

############################################################################
############################################################################
# Customize here


filter_boards = ["Reference", "Art"]        # Boards you need
pinterest = Pinterest(username='username')  # Username

############################################################################
############################################################################




new_downloads_count = 0
download_dir = os.getcwd() + '/pinterest/'



if not os.path.exists(download_dir):
	os.mkdir(download_dir)



boards = pinterest.boards()

downloaded_images = []
for folder in os.listdir(download_dir):
	path = os.path.join(download_dir, folder)
	if os.path.isfile(path):
		continue
	downloaded_images.extend([i.split('.')[0] for i in os.listdir(path)])



boards = boards if not filter_boards else [i for i in boards if i['name'] in filter_boards]


for target_board in boards: 

	print('\n' + target_board['name'], "\n")

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

			new_downloads_count += 1

	for pin in board_pins:

		if pin['id'] in downloaded_images:
			print("Skipping:", pin['id'])
			continue

		try: 
			url = pin['images']['orig']['url']
			indx = str(url).rfind('.')
			extension = str(url)[indx:]
			download_image(url, download_dir + pin['id'] + extension, pin['id'])
		except KeyError: 
			pass

print(F"\n\n{new_downloads_count} images were downloaded")


data_path = os.path.join(os.getcwd(), 'data')
print(data_path)
if os.path.exists(data_path):
	shutil.rmtree(data_path)