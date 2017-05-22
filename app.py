from flask import Flask, render_template, request
import searchengine, neuralnet, crawler
searcher = searchengine.searcher('searchengine.db')
crawler=crawler.crawler('searchengine.db')
nnet = neuralnet.searchnet('nn.db')
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def search():
	if request.method == 'POST':
		queryText = request.form['q']
		(wordids, urlIdsList, urlsList) = searcher.query(queryText)
		listOfItems = [{'id': urlIdsList[i], 'url': urlsList[i]} for i in range(len(urlIdsList))]
		return render_template('index.html', list=listOfItems, q=queryText)
	return render_template('index.html', list=None)

@app.route('/train', methods=['POST'])
def train():
	if request.method == 'POST':
		queryPhrase = request.json['q']
		selectedURLId = int(request.json['clicked'])
		(wordids, urlIdsList, urlsList) = searcher.query(queryPhrase)
		nnet.trainquery(wordids, urlIdsList, selectedURLId)
		return 'done'

@app.route("/crawl")
def crawl():
	pagelist=['https://en.wikipedia.org/wiki/Python_(programming_language)']
	crawler.crawl(pagelist)
	return ('Crawling Completed')

@app.route("/rank")
def rank():
	crawler.calculatepagerank()
	return ('Ranking Completed')

@app.route("/create")
def createDB():
	crawler.createindextables()
	nnet.maketables()
	return ('Tables created.')

if __name__ == "__main__":
    app.run()