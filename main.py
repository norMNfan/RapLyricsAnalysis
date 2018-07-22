# Brian Norlander 07-22-2018

import pandas as pd


def main():
	lyrics = pd.read_excel('input/LFID_WordIDs.xlsx', sheet_name='Sheet1')
	metadata = pd.read_excel('metadata_plus_LNS_360919_lyrics_20150707.xlsx', sheet_name='Sheet1')


if __name__ == "__main__":
	main()