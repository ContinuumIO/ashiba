import pandas as pd
import requests, json

#the number of commits per hour in each day
def daily_commit_timeline(user, repo):
    r = requests.get('https://api.github.com/repos/%s/%s/stats/punch_card' % (user, repo) )
    data = r.json()
    df = pd.DataFrame(data, columns=['day', 'hour', 'commits'])
    return df


#Get the weekly commit count for the repo owner and everyone else
def weekly_commit_timeline(user, repo):
    r = requests.get("https://api.github.com/repos/%s/%s/stats/participation" % (user, repo) )
    data = r.json()
    df = pd.DataFrame(data['all'], columns=['commits'])
    return df
