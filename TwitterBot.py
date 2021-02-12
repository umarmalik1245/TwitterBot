#!/usr/bin/env python3
"""TwitterBot.py is a simple twitter bot script, it utilizes twitter api to reply to tweets with specific hashtags tweeted at the bot, along with tweet and user/users on a timely basis - Umar Malik"""
import tweepy #Importing Python Library to use Twitter API
import time
print('This is my twitter bot!')

apiKey = ''
apiSecret = ''
accessKey = ''
accessSecret = ''

AUTH = tweepy.OAuthHandler(apiKey, apiSecret)
AUTH.set_access_token(accessKey, accessSecret)
API = tweepy.API(AUTH, wait_on_rate_limit=False)

fileName = 'last_seen_id.txt'
countTweet=0
countRemind=0

def retrieveLastSeenID(fileName):
    f_read = open(fileName, 'r')
    lastSeenID = int(f_read.read().strip())
    f_read.close()
    return lastSeenID


def storeLastSeenID(lastSeenID, fileName):
    f_write = open(fileName, 'w')
    f_write.write(str(lastSeenID))
    f_write.close()
    return

def replyToTweets():
    print('Checking for new Tweets and Replying to Tweets...')
    global countTweet
    print(countTweet)
    lastSeenID = retrieveLastSeenID(fileName)
    mentions = API.mentions_timeline(lastSeenID, tweet_mode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        lastSeenID = mention.id
        storeLastSeenID(lastSeenID, fileName)

        if '#SubtleBot' in mention.full_text.lower():
            print('Found #SubtleBot')
            print('Responding Back....')
            API.update_status('@' + mention.user.screen_name + ' Hey, thats the name dont wear it out! :)', mention.id)
            countTweet += 1

        elif '#Hi' in mention.full_text.lower():
            print('Found #Hi')
            print('Responding Back....')
            API.update_status('@' + mention.user.screen_name + ' Hey, whatsup!', mention.id)
            countTweet += 1

        else:
            print('Found Random!')
            print('Replying to Random....')
            API.update_status('@' + mention.user.screen_name + ' Hey Friend, Check Your DM! :)', mention.id)
            user=API.get_user(screen_name=mention.user.screen_name)
            API.send_direct_message(user.id, 'Do I Know You Friend? - Subtle Bot')
            countTweet += 1
            continue


def Reminder(userName): #Function to tweet reminders on a timely basis to specified user/users
    global countRemind
    print('Reminders')
    API.update_status('@' + userName + ' *Put Message Here*', userName)
    print(countRemind)
    countRemind+=1


def directMessage(userName): #Function to message
    global countDM
    print('Direct Message')
    user = API.get_user(screen_name='@' + userName)
    API.send_direct_message(user.id, 'message')
    print(countDM)
    countDM += 1


while True:
    replyToTweets()
    Reminder('userName')
    directMessage('userName')
    time.sleep(600)






