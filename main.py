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
	twfollowers = twapi.followers()
	# Sqlite3 Connection
	sqlconn = sqlite3.connect("follow.db")
	sqlc = sqlconn.cursor()
	# CREATE TABLE IF NOT EXISTS and INSERT followers
	sqlc.execute("CREATE TABLE IF NOT EXISTS followers (id INTEGER PRIMARY KEY ASC, name TEXT, screen_name TEXT)")
	sqle = sqlc.execute("SELECT * FROM followers ORDER BY id")
	sqlfollowers_data = sqle.fetchall()
	if len(sqlfollowers_data) == 0:
		for follower in twfollowers:
			sqlc.execute("INSERT INTO followers VALUES (" + str(follower.id) + ", '" + follower.name + "', '" + follower.screen_name + "')")
			print follower.screen_name + " added"
		sqlconn.commit()
		sqlconn.close()
		return 0
	# UPDATE Database
	for follower in twfollowers:
		sqle = sqlc.execute("SELECT * FROM followers WHERE ID = " + str(follower.id))
		user_data = sqle.fetchone()
		if user_data == None:
			sqlc.execute("INSERT INTO followers VALUES (" + str(follower.id) + ", '" + follower.name+"', '" + follower.screen_name + "')")
		elif user_data[1] != follower.name or user_data[2] != follower.screen_name:
			sqlc.execute("UPDATE followers SET name = '" + follower.name + "', screen_name = '" + follower.screen_name + "' WHERE id = " + str(follower.id))
	# Unfollower
	sqlfollower_ids = list()
	for follower in sqlfollowers_data:
		sqlfollower_ids.append(follower[0])
	unfollower_ids = set(sqlfollower_ids)
	for follower in twfollowers:
		unfollower_ids = unfollower_ids - set([follower.id])
	for follower_id in unfollower_ids:
		sqle = sqlc.execute("SELECT * FROM followers WHERE id = " + str(follower_id))
		follower_data = sqle.fetchone()
		print "@" + follower_data[2]
		sqlc.execute("DELETE FROM followers WHERE id = " + str(follower_id))
	sqlconn.commit()
	sqlconn.close()

if __name__ == "__main__":
	main()
