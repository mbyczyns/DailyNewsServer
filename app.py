from flask import Flask, request, jsonify
import requests
from classes import Article_snippet
import json


app = Flask(__name__)
with open("nyt_apikey.txt", "r") as f:
    nyt_apikey = f.read()
with open("news_apikey.txt", "r") as f:
    news_apikey = f.read()

def list_snippets(r):
    snippets=[]
    for i in r['response']['docs']:
        title = i['headline']['main']
        headline = i['headline']['print_headline']
        pub_date = i['pub_date']
        keywords = []
        for j in i['keywords']:
            keywords.append(j['value'])
        main_image_url = "https://static01.nyt.com/" + str(i['multimedia'][0]['url'])
        web_url = i['web_url']
        snippets.append(Article_snippet(title=title, headline=headline, pub_date=pub_date, keywords=keywords, main_image_url=main_image_url, web_url=web_url))
    return snippets

@app.route("/text")
def proxy_text():
    query = request.args.get("q", "")
    r = requests.get(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?fq={query}&api-key={nyt_apikey}")
    return r.text

@app.route("/json")
def proxy_json():
    query = request.args.get("q", "")
    r = requests.get(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?fq={query}&api-key={nyt_apikey}")
    return r.json()

@app.route("/parse")
def proxy_parser():
    query = request.args.get("q", "")
    r = requests.get(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?fq={query}&api-key={nyt_apikey}")
    r=r.json()
    title1 = str(r['response']['docs'][0]['headline']['main'])
    return title1


if __name__ == "__main__":
    app.run(debug=True)