#import time
#start = time.time()
from flask import Flask, request, render_template
#import psutil
#import os
from main import TwitterClient

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
# return "<h1>"+TwitterClient.xyz()+"</h1>"
@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        # print (result.get('val'))

        api = TwitterClient()

        tweets = api.get_tweets(query = result.get('val'), count = 1000000)
        if len(tweets)==0:
            return render_template('notfound.html')
        #Positive tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

        foo = []
        bar = []

        for tweet in ptweets[:10]:
            foo.append([tweet['text']])

        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

        for twee in ntweets[:10]:
            bar.append(twee['text'])

        nPer = 100*len(ntweets)/len(tweets)
        pPer = 100*len(ptweets)/len(tweets)
        return render_template('result.html', ptwee = foo, ntwee = bar, nPer = ('%.2f'%nPer), pPer = ('%.2f'%pPer))
#process = psutil.Process(os.getpid())
#print("Total memory used")
#print(process.memory_info().rss)      
#end = time.time()
#print("Total time taken")
#print(end - start)
if __name__ == '__main__':
    app.run(debug = True)
                       
