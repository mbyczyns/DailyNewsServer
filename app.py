from flask import Flask, request, jsonify, g
import requests
from classes import sections, desks
from manage_articles import list_snippets, print_snippets, get_article
from datetime import datetime
import sqlite3

DATABASE = "./database/database_file.db"

app = Flask(__name__)
with open("nyt_apikey.txt", "r") as f:
    nyt_apikey = f.read()
with open("news_apikey.txt", "r") as f:
    news_apikey = f.read()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # opcjonalnie: zwracaj jako dict
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route("/search")
def categories_endpoint():
    global global_snippets
    query = request.args.get("fq", "")
    if query in sections:
        r = requests.get(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=section.name:(\"{query}\")&api-key={nyt_apikey}")
    elif query in desks:
        r = requests.get(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=desk:(\"{query}\")&api-key={nyt_apikey}")
    else:
        r = requests.get(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key={nyt_apikey}") 
    r=r.json()
    snippets = list_snippets(r)
    global_snippets = snippets
    print_snippets(snippets)
    return jsonify([article.to_dict() for article in snippets])


@app.route("/readarticle")
def readarticle(): # zapisuje artykuł do bazy danych jako przeczytany (watched)
    searched_url = request.args.get("fq", "")
    db= get_db()
    cursor = db.cursor()
    article = get_article(global_snippets,searched_url)
    cursor.execute(f"INSERT into articles (title, action, web_url, pub_date, print_headline, main_image_url) values ('{article.title}', 'watched', '{article.web_url}', '{article.pub_date}', '{article.print_headline}', '{article.main_image_url}')")
    for keyword in article.keywords:
        cursor.execute(f"INSERT into keywords (keyword, article_title) values ('{keyword}','{article.title}')")
    

@app.route("/likearticle")
def likearticle(): # zapisuje artykuł do bazy danych jako przeczytany (watched)
    searched_url = request.args.get("fq", "")
    db= get_db()
    cursor = db.cursor()
    article = get_article(global_snippets,searched_url)
    cursor.execute(f"INSERT into articles (title, action, web_url, pub_date, print_headline, main_image_url) values ('{article.title}', 'liked', '{article.web_url}', '{article.pub_date}', '{article.print_headline}', '{article.main_image_url}')")
    for keyword in article.keywords:
        cursor.execute(f"INSERT into keywords (keyword, article_title) values ('{keyword}','{article.title}')")
    


@app.route("/database")
def test_database():
    db= get_db()
    cursor = db.cursor()
    cursor.execute("select * from articles")
    rows = cursor.fetchall()
    return jsonify([dict(row) for row in rows]) 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555)
    global_snippets = []
    