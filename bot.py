from __future__ import print_function
import os
import sys
import json
import logging
import tweepy
import finagler

creds_file = 'credentials.json'

credentials = {}

if os.path.isfile(creds_file):
    with open(creds_file) as infile:
        credentials = json.load(infile)
else:
    print('Credentials not found. Run auth_setup.py first.')
    sys.exit(1)

auth = tweepy.OAuthHandler(credentials['ConsumerKey'],
                           credentials['ConsumerSecret'])
auth.set_access_token(credentials['AccessToken'],
                      credentials['AccessSecret'])

api = tweepy.API(auth)


def do_tweet(event, context):
    profile = finagler.randomized_profile()
    api.update_profile(**profile)
    return profile

if __name__ == '__main__':
    print(do_tweet(None, None))
