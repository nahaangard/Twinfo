import tweepy
import json
from tweepy import OAuthHandler
import pickle
import time
from datetime import datetime

# Credentials
consumer_key='xxxxxxxxxxxxx'
consumer_secret='xxxxxxxxxxxxxx'
access_token='xxxxxxxxxxxxxx'
access_secret='xxxxxxxxxxxxxx'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
#print '@name | id | screen name'

# print out format : set to be name, if and screen_name
def print_out(twpack):
    print twpack['name'],' | ', twpack['screen_name'], ' | ', 'id: ', twpack['id'],' | ', 'from: ', twpack['location'],\
    ' | ', 'Created on: ', twpack['created_at'],'\n' 'Bio: ', twpack['description'], \
    ' | ',  'Followers:',twpack ['followers_count'], ' | ', 'Followings: ', twpack['friends_count'],'\n', '#' \

# my info
def WhoAmI():
    me_info = api.me()
    print_out(json.loads(json.dumps(me_info._json)))
    response = raw_input('Do you want the followers list to be recorded?(y/n) ')
    if response == 'y':
        latest_kept_record()

# anyone's info
def WhoIsWho():
    scr_name = raw_input('who do you want to get info from? ')
    who_info = api.get_user(scr_name)
    print_out(json.loads(json.dumps(who_info._json)))

# my followers
def my_followers():
    scr_name = json.loads(json.dumps(api.me()._json))['screen_name']
    counter_flr = 0
    for individual in tweepy.Cursor(api.followers, screen_name = scr_name, count=200).items():
        counter_flr += 1
        print_out(json.loads(json.dumps(individual._json)))
    print
    print 'number of followers is equal to: ' + str(counter_flr)

# Someone else's followers
def others_followers():
    scr_name = raw_input('who do you want to get info from? ')
    counter_flr = 0
    for individual in tweepy.Cursor(api.followers, screen_name = scr_name, count=200).items():
        counter_flr += 1
        print_out(json.loads(json.dumps(individual._json)))
    print
    print 'number of followers is equal to: ' + str(counter_flr)

# my 5 latest followers
def my_latest_followers():
    scr_name = json.loads(json.dumps(api.me()._json))['screen_name']
    counter_flr = 0
    for individual in tweepy.Cursor(api.followers, screen_name=scr_name, count=200).items(10):
        counter_flr += 1
        print_out(json.loads(json.dumps(individual._json)))
    print
    print 'number of followers is equal to: ' + str(counter_flr)

# my followings
def my_followings():
    scr_name = json.loads(json.dumps(api.me()._json))['screen_name']
    counter_fnd = 0
    for individual in tweepy.Cursor(api.friends, screen_name = scr_name, count=200).items():
        counter_fnd += 1
        print_out(json.loads(json.dumps(individual._json)))
    print
    print 'number of friends is equal to: ' + str(counter_fnd)

# unfollowing my non-backers
def non_backers():
    scr_name = json.loads(json.dumps(api.me()._json))['screen_name']
    friends = api.friends_ids(screen_name = scr_name)
    followers = api.followers_ids(screen_name = scr_name)
    c = 0
    duty = raw_input('do you want your non-backer to be unfollowed? (y/n) ')
    for individual in friends:
        if individual not in followers:
            c += 1
            status = api.get_user(individual)
            print_out(json.loads(json.dumps(status._json)))
            if duty == 'y':
                api.destroy_friendship(individual)
    print
    print 'number of non-follow-backers: ' + str(c)
    if duty == 'y' and c != 0:
        print 'your non-backers are all unfollowed.'
    elif duty == 'y' and c == 0:
        print 'no one left to be unfollowed'
    if duty == 'n':
        print 'your non-backers are still being followed.'
    print

# sync for the latest followers list record
# This option is necessary to be done before
# new follower welcome message module
def latest_kept_record():
    scr_name = json.loads(json.dumps(api.me()._json))['screen_name']
    my_latest_followersList_record = api.friends_ids(screen_name=scr_name)
    with open('lastlist_id_record.txt', 'wb') as f:
        pickle.dump(my_latest_followersList_record, f)
    print 'followers LIST was recorded!'
    print

# direct message to the new followers
# it'll use the previously created list
def dm_to_my_new_followers():
    scr_name = json.loads(json.dumps(api.me()._json))['screen_name']
    with open('lastlist_id_record.txt', 'rb') as f:
        latest_list_record_id = pickle.load(f)

    new_followers_list = api.followers_ids(screen_name=scr_name)
    dm_message_body = raw_input('What is your welcome message: ')
    for individual in new_followers_list:
        if individual not in latest_list_record_id:
            response = raw_input('do you want your DM to be sent now?(y/n) ')
            if response == 'y':
                api.send_direct_message(user_id=individual, text = dm_message_body)
                print ('your DM was sent to your new followers')

def follow_back_new_followers():
    scr_name = json.loads(json.dumps(api.me()._json))['screen_name']
    with open('lastlist_id_record.txt', 'rb') as f:
        latest_list_record_id = pickle.load(f)

    new_followers_list = api.followers_ids(screen_name=scr_name)
    response = raw_input('do you want to follow your all new follower?(y/n) ')
    if response == 'y':
        for individual in new_followers_list:
            if individual not in latest_list_record_id:
                follower = json.loads(json.dumps(api.get_user(individual)._json))
                api.create_friendship(individual)
                print (follower['screen_name'] + ' followed')

# Delete my Old Tweets
def delete_my_old_tweets():
    print
    print '*** BE CARFUL ***'
    print
    print 'Tweets before the TIME you enter now will be deleted for good!'
    print 'Example: 12-05-2014 for dd-mm-yy or type "n" to cancel'
    print
    time_thereshold = raw_input('Please enter your time: ')
    if time_thereshold == 'n':
            return
    else:
        time_thereshold = datetime.strptime(time_thereshold, '%d-%m-%Y')
        print 'I''m collecting your tweets...'
        collected_tweets = tweepy.Cursor(api.user_timeline).items()
        print 'Tweet were collected.'
        deleted_tweets = 0
        mode = raw_input('Do you wanna delete them All or One by ONE: (all/one): ')
        for tweet in collected_tweets:
            if tweet.created_at < time_thereshold:
                if mode == 'all':
                    response = raw_input('are you sure?(y/n) ')
                    if response == 'y':
                        api.destroy_status(tweet.id)
                        deleted_tweets += 1
                    elif response == 'n':
                        break
                elif mode == 'one':
                    while tweet:
                        print "Deleting %d: [%s] %s" % (tweet.id, tweet.created_at, tweet.text)
                        response = raw_input('are you sure?(y/n) ')
                        if response == 'y':
                            api.destroy_status(tweet.id)
                            time.sleep(5)
                            print 'Deleted.'
                            deleted_tweets += 1
                        elif response == 'n':
                            break
        print
        print str(deleted_tweets) + ' Tweets were deleted.'

# Send a tweet for me
def tweet_for_me():
    twpack = raw_input('what do you wanna tweet: ')
    api.update_status(twpack)

def main():
    try:
        while True:
            print '----------------------------------'
            print 'make your decision from the list: '
            print '----------------------------------'
            print
            print '[000]  tell me who am I (and SYNC me)?'
            print '[001]  list ALL my Followers'
            print '[002]  list my 10 Latest Followers'
            print '[003]  list my Followings'
            print '[004]  Unfollow my non-Backers'
            print '[005]  follow BACK all my new Followers'
            print '[006]  set a DM to new Followers'
            print '[007]  Delete my OLD tweets'
            print '[011]  Send a Tweet for me'
            print
            print '[100]  tell me who is WHO?'
            print '[101]  list the Followers of WHO'
            print '[9]   to QUIT me!'
            options = {
                000 : WhoAmI,
                001 : my_followers,
                002 : my_latest_followers,
                003 : my_followings,
                004 : non_backers,
                005 : follow_back_new_followers,
                006 : dm_to_my_new_followers,
                007 : delete_my_old_tweets,
                011 : tweet_for_me,
                100 : WhoIsWho,
                101 : others_followers,
                9 : quit
            }
            dcsn = int(raw_input('make your decision: '))
            if dcsn == 9:
                return
            else:
                options[dcsn]()
    except:
        print
        print '------------------------------------'
        print 'not an option!'
        print 'choose a proper number from the list'
        print '------------------------------------'
        print
        main()

if __name__ == "__main__":
    main()
