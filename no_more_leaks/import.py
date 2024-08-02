#!/usr/bin/env python3

import argparse
import sqlite3
import os
import progressbar

# Main

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Import No More Leaks dataset into a sqlite3 database', allow_abbrev=False)
	parser.add_argument('--database', '-d', type=str, default='../data/nomoreleaks.sqlite3', metavar="<path to database>", required=False, help="path of directory to create member md files")
	parser.add_argument('--shas', '-s', type=argparse.FileType('r'), default='/dev/stdin', metavar="<path to hash database>", required=False, help="path of file containing the SHA512 hashes")

	args = parser.parse_args()

	print(args.database)
	conn = sqlite3.connect(args.database)
	cur = conn.cursor()
	cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='hashes'; ")
	cur.execute("""
		CREATE TABLE IF NOT EXISTS hashes(
			hash TEXT
		)
	""")
	cur.execute("""
		CREATE UNIQUE INDEX IF NOT EXISTS hashes_index ON hashes(hash)
	""")
	cur.execute("DELETE FROM hashes")

	bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
	i = 0
	for line in args.shas.readlines():
		cur.execute("INSERT INTO hashes VALUES(?)", ( line.strip(), ) )
		bar.update(i)
		i=i+1
	conn.commit()
	args.shas.close()
	