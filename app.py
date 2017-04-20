from flask import Flask, render_template, request
import searchengine
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def search():
	if request.method == 'POST':
		queryText = request.form['q']
		e = searchengine.searcher('searchengine.db')
		list = e.query(queryText)
		return render_template('index.html', list=list)
	return render_template('index.html', list=None)

@app.route("/crawl")
def crawl():
	pagelist=['https://en.wikipedia.org/wiki/Python_(programming_language)']
	crawler=searchengine.crawler('searchengine.db')
	crawler.crawl(pagelist)
	return ('Hi')

@app.route("/create")
def createDB():
	crawler=searchengine.crawler('searchengine.db')
	crawler.createindextables()
	return ('Created')

if __name__ == "__main__":
    app.run()