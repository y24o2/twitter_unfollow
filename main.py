#!/usr/bin/python
#-*-coding: utf-8-*-

"""
unfollow.py

requires:
        tweepy - python modul
	https://github.com/tweepy/tweepy

	twitter - application
	https://dev.twitter.com/
"""

import tweepy
import sqlite3
import os

# Twitter OAuth
access_token = open(os.path.expanduser("~/.twitter/access_token")).read()
access_token_secret = open(os.path.expanduser("~/.twitter/access_token_secret")).read()
consumer_key = open(os.path.expanduser("~/.twitter/consumer_key")).read()
consumer_secret = open(os.path.expanduser("~/.twitter/consumer_secret")).read()

def main():
	# Tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	twapi = tweepy.API(auth)
	
	# get IDs
	twitter_ids = twapi.followers_ids()
	
	# sqlite
	con = sqlite3.connect("data.db")
	cur = con.cursor()
	
	# sqlite create database
	cur.execute("CREATE TABLE IF NOT EXISTS ids (id INTEGER PRIMARY KEY ASC)")
	if len(cur.execute("SELECT id FROM ids").fetchall()) == 0:
		for i in twitter_ids:
			cur.execute("INSERT INTO ids VALUES (" + str(i) + ")")
		con.commit()
		con.close()
		return 0
	
	# comparison
	sql_ids = []
	for row in cur.execute("SELECT id FROM ids"):
		sql_ids += [row[0]]
	lost_ids = set(sql_ids) - set(twitter_ids)
	new_ids = set(twitter_ids) - set(sql_ids)
	
	# debug
	debug = False
	if debug:
		print "sql ids:"
		print sql_ids
		print "\ntwitter ids:"
		print twitter_ids
		print "\nlost ids:"
		print lost_ids
		print "\nnew ids:"
		print new_ids
		return 0 #debug
	
	# sqlite update db
	for i in lost_ids:
		cur.execute("DELETE FROM ids WHERE id = '" + str(i) + "'")
		user = twapi.get_user(i)
		print user.name + "@" + user.screen_name
	for i in new_ids:
		cur.execute("INSERT INTO ids VALUES ('" + str(i) + "')")
	
	# sqlite save db and exit
	con.commit()
	con.close()
	return 0

if __name__ == "__main__":
	main()
