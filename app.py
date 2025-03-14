from flask import Flask, request, jsonify
import requests
from classes import Article_snippet
import json


app = Flask(__name__)
with open("nyt_apikey.txt", "r") as f:
    nyt_apikey = f.read()
with open("news_apikey.txt", "r") as f:
    news_apikey = f.read()

def list_snippets(response):
    pass

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