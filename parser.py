from classes import Article_snippet
from datetime import datetime
import json

def list_snippets(r):
    snippets=[]
    for i in r['response']['docs']:
        title = i['headline']['main']
        headline = i['headline']['print_headline']
        pub_date = extract_date(i['pub_date'])
        keywords = []
        for j in i['keywords']:
            keywords.append(j['value'])
        image_url = i['multimedia']['default']['url']
        main_image_url = image_url
        web_url = i['web_url']

        snippets.append(Article_snippet(title=title, print_headline=headline, pub_date=pub_date, keywords=keywords, main_image_url=main_image_url, web_url=web_url))
    return snippets

def print_all(snippets):
    for snip in snippets:
        print(f"-------------{snip.title}------------")
        print(snip.pub_date)
        print(snip.keywords)
        print(snip.main_image_url)
        print(snip.print_headline)
        print(snip.web_url)
        print("--------------------------")

def extract_date(rawdate):
    dt = datetime.strptime(rawdate, "%Y-%m-%dT%H:%M:%S%z")
    return dt.strftime("%Y-%m-%d")

with open("json.json", "r") as f:
    js = json.load(f)

parsed = list_snippets(js)
print_all(parsed)
    