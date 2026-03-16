import os

def list_files(directory):
	return [
		os.path.join(root, file)
		for root, dirs, files in os.walk(directory)
		for file in files
	]