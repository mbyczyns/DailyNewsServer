from flask import Flask, request, jsonify
import requests
from classes import Article_snippet, sections, desks
from datetime import datetime
import sqlite3


app = Flask(__name__)
with open("nyt_apikey.txt", "r") as f:
    nyt_apikey = f.read()
with open("news_apikey.txt", "r") as f:
    news_apikey = f.read()

def extract_date(rawdate):
    dt = datetime.strptime(rawdate, "%Y-%m-%dT%H:%M:%S%z")
    return dt.strftime("%Y-%m-%d")


def get_article(snippets, searched_url):
    for snpt in snippets:
        if hasattr(snpt, 'web_url'):
            if getattr(snpt, 'web_url') == searched_url:
                return snpt
    return None
    

def list_snippets(r):
    snippets = []
    for i in r['response']['docs']:
        title = i['headline']['main']
        headline = i['headline'].get('print_headline', "") 
        pub_date = extract_date(i['pub_date'])
        keywords = [j['value'] for j in i['keywords']]
        image_url = i['multimedia']['default']['url']
        main_image_url = image_url
        web_url = i['web_url']

        snippets.append(
            Article_snippet(
                title=title,
                print_headline=headline,
                pub_date=pub_date,
                keywords=keywords,
                main_image_url=main_image_url,
                web_url=web_url
            )
        )

    snippets.sort(key=lambda x: datetime.strptime(x.pub_date, "%Y-%m-%d"), reverse=True)
    return snippets


def print_snippets(list_snippets):
    for snippet in list_snippets:
        print("      "+snippet.title)
        print(snippet.print_headline)
        print(snippet.pub_date)
        print(snippet.keywords)
        print(snippet.main_image_url)
        print(snippet.web_url)
        print("- - - - - - - - -")


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
    article = get_article(global_snippets,searched_url)
    cursor.execute(f"INSERT into articles (title, action, web_url, pub_date, print_headline, main_image_url) values ('{article.title}', 'watched', '{article.web_url}', '{article.pub_date}', '{article.print_headline}', '{article.main_image_url}')")
    for keyword in article.keywords:
        cursor.execute(f"INSERT into keywords (keyword, article_title) values ('{keyword}','{article.title}')")
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    global_snippets = []
    conn = sqlite3.connect("./database/database_file.db")
    cursor = conn.cursor()