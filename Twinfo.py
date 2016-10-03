import tweepy
import json
from tweepy import OAuthHandler
import pickle

# Credentials
# Get them from apps.twitter.com for an authenticated account
consumer_key='xxxxxxxxxxxxxxxxxx'
consumer_secret='xxxxxxxxxxxxxxxxxxx'
access_token='xxxxxxxxxxxxxxxxxxx'
access_secret='xxxxxxxxxxxxxxxxxxxx'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# print '@name | id | screen name'
# print out format : set to be name, id and screen_name
def print_out(twpack):
    print twpack['name'],' | ', twpack['id'],' | ', twpack['screen_name']

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
    scr_name = raw_input('I need the screen name: ')
    counter_flr = 0
    for individual in tweepy.Cursor(api.followers, screen_name = scr_name, count=200).items():
        counter_flr += 1
        print_out(json.loads(json.dumps(individual._json)))
    print
    print 'number of followers is equal to: ' + str(counter_flr)

# my 5 latest followers
def my_latest_followers():
    scr_name = raw_input('I need the screen name: ')
    counter_flr = 0
    for individual in tweepy.Cursor(api.followers, screen_name=scr_name, count=200).items(5):
        counter_flr += 1
        print_out(json.loads(json.dumps(individual._json)))
    print
    print 'number of followers is equal to: ' + str(counter_flr)

# my followings
def my_followings():
    scr_name = raw_input('I need the screen name: ')
    counter_fnd = 0
    for individual in tweepy.Cursor(api.friends, screen_name = scr_name, count=200).items():
        counter_fnd += 1
        print_out(json.loads(json.dumps(individual._json)))
    print
    print 'number of friends is equal to: ' + str(counter_fnd)

# unfollowing my non-backers
def non_backers():
    scr_name = raw_input('I need the screen name: ')
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
    scr_name = raw_input('I need a screen name: ')
    my_latest_followersList_record = api.friends_ids(screen_name=scr_name)
    with open('lastlist_id_record.txt', 'wb') as f:
        pickle.dump(my_latest_followersList_record, f)
    print 'followers LIST was recorded!'
    print

# direct message to the new followers
# it'll use the previously created list
def dm_to_my_new_followers():
    scr_name = raw_input('I need a screen name: ')
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

def main():
    try:
        while True:
            print '----------------------------------'
            print 'make your decision from the list: '
            print '----------------------------------'
            print
            print '[0]  Tell me who am I (and sync me)?'
            print '[1]  Tell me who is Who?'
            print '[2]  List my Followers'
            print '[3]  5 Latest Followers'
            print '[4]  List of My Followings'
            print '[5]  Unfollow my non-Backers'
            print '[6]  Set DM to new Followers'
            print '[9]  To Quit me!'
            options = {
                0 : WhoAmI,
                1 : WhoIsWho,
                2 : my_followers,
                3 : my_latest_followers,
                4 : my_followings,
                5 : non_backers,
                6 : dm_to_my_new_followers,
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
