# -*- coding: utf-8 -*-
import tweepy
import json
from tweepy import OAuthHandler
import time
import sys
import urllib2
import re
from collections import OrderedDict
from tqdm import tqdm

# Credentials
#consumer_key='TOMgP9u0C0rd7zo51qLbmszbz'
#consumer_secret='VgzJC60lPcwqBK69MnY3Sb1Rx7ypK0Edi8MwReoj5rym3p6FIz'
#access_token='780211428061872128-f9DQB1tv4yC3njpjy0Z8vaf4Efh9Duu'
#access_secret='8cbSymWatNbrqjZhMEqft1lY0vjdR2kTXlaK8qwGFYsyX'

consumer_key = 'LXrCwKJEhPJNuScUt8hSmDjmE'
consumer_secret = 'dMZPrqk8XKWipbovpJWp2QJItmMsgFkEKHG4WSBk6FIXgASs47'
access_token = '1892735628-QFGVGkUddMAbtt16a08v0KSwzagNERLbzGBPEel'
access_secret = '7BnvrVCN77su91GR7YTGm1SDVmHZDedo5GuPTiDPBwHat'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
#api = tweepy.API(auth)
favers_list = []
number_of_tweets = 500


def get_user_ids_of_post_likes(post_id):
    try:
        json_data = urllib2.urlopen('https://twitter.com/i/activity/favorited_popup?id=' + str(post_id)).read()
        found_ids = re.findall(r'data-user-id=\\"+\d+', json_data)
        unique_ids = list(set([re.findall(r'\d+', match)[0] for match in found_ids]))

        for ids in tqdm(unique_ids):

            user = api.get_user(ids)
            user = json.loads(json.dumps(user._json))
            time.sleep(0.1)
            favers_list.append(user['screen_name'])

    except urllib2.HTTPError:
        pass


def list_my_tweets():

    collected_tweets = tweepy.Cursor(api.user_timeline).items(number_of_tweets)
    print 'tweets were collected.'
    print
    time.sleep(2)
    print 'counting favs and collecting favers:'
    for tweet in collected_tweets:
        current_tweet = (json.loads(json.dumps(tweet._json)))
        get_user_ids_of_post_likes(current_tweet['id'])
    print 'you totally had %d favs for the past %d tweets.' % (len(favers_list), number_of_tweets)
    time.sleep(1)
    return favers_list


def favers_list_processing(list):

    favers_list_count = {x:list.count(x) for x in list}
    print 'the favers list was sorted (ascending):'
    #time.sleep(0.5)
    sorted_favers_list = OrderedDict(sorted(favers_list_count.items(), key=lambda x: x[1]))
    print
    for i, j in sorted_favers_list.items():
        print json.loads(json.dumps(api.get_user(i)._json))['name'], ':', j
    print
    return sorted_favers_list


def following_list_processing():
    counter_fnd = 0
    scr_name = json.loads(json.dumps(api.me()._json))['screen_name']
    following_list = []
    print 'now collecting the followings list...'
    #time.sleep(0.5)
    for individual in tweepy.Cursor(api.friends, screen_name = scr_name, count = 200 ).items():
        counter_fnd += 1
        following_list.append((json.loads(json.dumps(individual._json)))['screen_name'])
    print 'the following list was collected.'
    print
    return following_list


def no_interactioners(followings, favers):

    print 'people who did not fav your past %d tweets:' % number_of_tweets
    print
    final_counter = 0
    for following in followings:
        if following not in favers:
            print str(final_counter) + ':   ' + json.loads(json.dumps(api.get_user(following)._json))['name']
            final_counter += 1
    print
    print 'you are following %d people and ' % len(followings)
    print '%d people did not interact with you in the past %d tweets.' % ((final_counter-1), number_of_tweets)
    response = raw_input('do you want to unfollow the non-interactors? (y/n)')
    if response == 'y':
        for following in followings:
            if following not in favers:
                following_name = json.loads(json.dumps(api.get_user(following)._json))['name']
                res = raw_input('do you want to unfollow %s ? (y/n/exit)' % following_name)
                if res == 'y':
                    api.destroy_friendship(following)

                elif res == 'n':
                    pass

                elif res == 'exit':
                    break

    if response == 'n':
        pass


def main():
    print
    print "hey, let's do this!"
    time.sleep(2)
    print
    unsorted_favers_list = list_my_tweets()
    sorted_favers_list = favers_list_processing(unsorted_favers_list)
    following_list = following_list_processing()
    no_interactioners(following_list, sorted_favers_list)
    print
    print 'then khosh galdi :)'
    print 'Amin'

if __name__ == '__main__':
    main()
