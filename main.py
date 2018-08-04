# Brian Norlander 07-22-2018

import pandas as pd

def main():
	#lyrics = pd.read_excel('input/LFID_WordIDs.xlsx', sheet_name='Sheet1')
	#corpus = pd.read_excel('input/LF_SUBTLEX_merged_20150719.xlsx', sheet_name='LF_20150302')
	metadata = pd.read_excel('input/metadata_plus_LNS_360919_lyrics_20150707.xlsx', sheet_name='Sheet2')

	albums = dict()

	for i in metadata.index:
		if metadata['song_artist_name'][i] == 'Lil Wayne':
			if metadata['album_title'][i] in albums:
				albums[metadata['album_title'][i]] += 1
			else:
				albums[metadata['album_title'][i]] = 1\

	for album, count in albums.items():
		print(str(album) + ' : ' + str(count))

if __name__ == "__main__":
	main()