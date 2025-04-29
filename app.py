from flask import Flask, request, jsonify
import requests
from classes import Article_snippet, sections, desks
from datetime import datetime


app = Flask(__name__)
with open("nyt_apikey.txt", "r") as f:
    nyt_apikey = f.read()
with open("news_apikey.txt", "r") as f:
    news_apikey = f.read()

def extract_date(rawdate):
    dt = datetime.strptime(rawdate, "%Y-%m-%dT%H:%M:%S%z")
    return dt.strftime("%Y-%m-%d")

def list_snippets(r):
    snippets = []
    for i in r['response']['docs']:
        title = i['headline']['main']
        headline = i['headline'].get('print_headline', "")  # dodaj `get()` na wypadek braku klucza
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

    # Sortuj po dacie od najnowszej do najstarszej
    snippets.sort(key=lambda x: datetime.strptime(x.pub_date, "%Y-%m-%d"), reverse=True)

    return snippets

@app.route("/categories")
def categories_endpoint():
    query = request.args.get("fq", "")
    if query in sections:
        r = requests.get(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=section.name:(\"{query}\")&api-key={nyt_apikey}")
    elif query in desks:
        r = requests.get(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=desk:(\"{query}\")&api-key={nyt_apikey}")
    else:
           r = requests.get(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key={nyt_apikey}") 
    r=r.json()
    snippets = list_snippets(r)
    return jsonify([article.to_dict() for article in snippets])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)