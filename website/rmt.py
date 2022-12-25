def search(subreddits,keywords,timesince):
    import pandas as pd
    import time
    import datetime
    CLIENT_ID = "YDKLrV4l3pXymmAXGlgHvg"
    SECRET_KEY = "v6OvjWYj2VvypMolXOKPyaPs5GpJlw"

    import requests

    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    data = {
        'grant_type': 'password',
        'username': 'ACav12',
        'password': 'Captainrex1'
    }

    headers = {'User-Agent': 'MarketingToolkit'} 

    req = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth,
                        data=data,
                        headers=headers
                        )

    TOKEN = req.json()['access_token']

    headers['Authorization'] = f'bearer {TOKEN}'
    df = pd.DataFrame()


    for subreddit in subreddits:
        print("searching"+subreddit)
        time.sleep(2.4)
        output = requests.get('https://oauth.reddit.com/r/'+subreddit+'/new', headers=headers , params={'limit':'100'})
        inrange = True
        while(inrange==True):
            for post in output.json()['data']['children']:
                if time.time() - post['data']['created_utc'] < timesince:
                    inrange = True
                   
                    finalkeywords = ""
                    count = 0
                    for keyword in keywords:
                        
                        date = datetime.datetime.fromtimestamp(post['data']['created_utc'])
                        date = date.strftime( "%m/%d/%Y  %H:%M")
                        postcontent = post['data']['title']+" "+ post['data']['selftext']
                        postcontent = str(postcontent).lower()
                        keyword = keyword.lower()
                        
                        
                        if keyword in postcontent:
                            if count==0:
                                finalkeywords = keyword
                            else:
                                finalkeywords = finalkeywords + ", " + keyword 
                            count += 1
                    if count > 0:
                        df.loc[len(df), ['title','selftext','date','realdate','keyword','subreddit', 'permalink']] = post['data']['title'], post['data']['selftext'], date, post['data']['created_utc'],finalkeywords,subreddit,post['data']['permalink']    
            inrange=False
    if len(df)>0:
        print(df)
        df = df.sort_values(by=['realdate'], ascending=False)
        df = df[:10]
        df = df.reset_index(drop=True)
    return(df)
    


# if __name__ == '__main__':
#     search()

    




