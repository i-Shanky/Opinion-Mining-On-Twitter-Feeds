from flask import Flask, request, render_template
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

		#Positive tweets
		ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

		foo = []
		bar = []
		
		for tweet in ptweets[:10]: 
			foo.append(tweet['text'])		

		# print(foo)

		# print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))

		#Negative tweets
		ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

		for twee in ntweets[:10]: 
			bar.append(twee['text'])

		# print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))

		nPer = 100*len(ntweets)/len(tweets)

		pPer = 100*len(ptweets)/len(tweets)
		# print("\n\nPositive tweets:") 
		# for tweet in ptweets[:10]: 
		# 	print(tweet['text']) 

		# print("\n\nNegative tweets:") 
		# for tweet in ntweets[:10]: 
		# 	print(tweet['text'])
		# bar = "Aditya"
		# print(ptweets)
		return render_template('result.html', ptwee = foo, ntwee = bar, nPer = ('%.2f'%nPer), pPer = ('%.2f'%pPer))

if __name__ == '__main__':
	app.run(debug = True)
