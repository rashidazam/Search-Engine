from flask import Flask, render_template, request
import searchengine, neuralnet
app = Flask(__name__)
e = searchengine.searcher('searchengine.db')
crawler=searchengine.crawler('searchengine.db')
nnet = neuralnet.searchnet('nn.db')

@app.route("/", methods=['POST', 'GET'])
def search():
	if request.method == 'POST':
		queryText = request.form['q']
		(wordids, urlIdsList, urlsList) = e.query(queryText)
		listOfItems = []
		for i in range(0, len(urlIdsList)):
			listOfItems.append({'id': urlIdsList[i], 'url': urlsList[i]})
		return render_template('index.html', list=listOfItems, q=queryText)
	return render_template('index.html', list=None)

@app.route('/train', methods=['POST', 'GET'])
def train():
	if request.method == 'POST':
		queryPhrase = request.json['q']
		selectedURLId = int(request.json['clicked'])
		(wordids, urlIdsList, urlsList) = e.query(queryPhrase)
		nnet.trainquery(wordids, urlIdsList, selectedURLId)
		return 'done'

@app.route("/crawl")
def crawl():
	pagelist=['https://en.wikipedia.org/wiki/Python_(programming_language)']
	crawler.crawl(pagelist)
	return ('Crawling Complete')

@app.route("/rank")
def rank():
	crawler.calculatepagerank( )
	return ('Ranking Complete')

@app.route("/create")
def createDB():
	crawler.createindextables()
	nnet.maketables()
	return ('Created')

if __name__ == "__main__":
    app.run()