from flask import Flask, render_template, request, redirect
import searchengine, neuralnet, crawler
searcher = searchengine.searcher('searchengine.db')
crawler = crawler.crawler('searchengine.db')
nnet = neuralnet.searchnet('nn.db')


app = Flask(__name__)


@app.route("/")
def search():
	if request.args:
		queryText = request.args.get('q')
		(wordids, scores, urlIdsList, urlsList) = searcher.query(queryText)
		if len(urlIdsList) != 0:
			listOfItems = [{'id': urlIdsList[i], 'url': urlsList[i], 'score': scores[i]} for i in range(len(urlIdsList))]
		else:
			listOfItems = []
		return render_template('index.html', list=listOfItems, q=queryText)
	return render_template('index.html', list=None)


@app.route('/train', methods=['POST', 'GET'])
def train():		
	if request.method == 'POST':
		queryPhrase = request.json['q']
		selectedURLId = int(request.json['clicked'])
		app.logger.debug('queryPhrase: %s => selectedURLId: %s' %(queryPhrase, selectedURLId))
		(wordids, scores, urlIdsList, urlsList) = searcher.query(queryPhrase)
		nnet.trainquery(wordids, urlIdsList, selectedURLId)
		return 'done'
	return redirect('/')


@app.cli.command('crawl')
def crawl():
	pagelist=['https://en.m.wikipedia.org/wiki/Wikipedia:Former_featured_articles','https://en.wikipedia.org/wiki/Python_(programming_language)']
	crawler.crawl(pagelist)
	print ('Crawling Completed')


@app.cli.command('rankdocuments')
def rank():
	crawler.calculatepagerank()
	print ('Ranking Completed')


@app.cli.command('initdb')
def createDB():
	crawler.createindextables()
	nnet.maketables()
	print ('Tables created.')


if __name__ == "__main__":
	# 'threaded=True' argument enables support concurrent requests to flask app
    app.run(threaded=True)