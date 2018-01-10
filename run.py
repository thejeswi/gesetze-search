from flask import Flask, render_template, request
from simplesearch import search
app = Flask(__name__)

@app.route("/")
@app.route("/search")
def index():
    return render_template("index.html")

@app.route("/query", methods=['POST'])
def query():
    query = request.form['query']
    langauge = request.form['langauge']
    results = search(query, language = langauge)
    return render_template("search.html", results = results, query=query, language = langauge)
    
if __name__ == '__main__':
    app.run(debug=True)
