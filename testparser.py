from classes import Article_snippet
import json

def list_snippets(r):
    snippets=[]
    for i in r['response']['docs']:
        title = i['headline']['main']
        headline = i['headline']['print_headline']
        pub_date = i['pub_date']
        keywords = []
        for j in i['keywords']:
            keywords.append(j['value'])
        images=[]
        for j in i['multimedia']:
            # print(j['url'])
            images.append(j['url'])
        if len(images)>0:
            main_image_url = images[0]
        else: main_image_url=''
        print(f'------- length:{len(images)}----------')
        web_url = i['web_url']

        print("----------------------------")
        print(f"title: {title}, type: {type(title)}")
        print(f"headline: {headline}, type: {type(headline)}")
        print(f"pub_date: {pub_date}, type: {type(pub_date)}")
        print(f"keywords: {keywords}, type: {type(keywords)}")
        print(f"main_image_url: {main_image_url}, type: {type(main_image_url)}")
        print(f"web_url: {web_url}, type: {type(web_url)}")
        print("----------------------------")

        snippets.append(Article_snippet(title=title, print_headline=headline, pub_date=pub_date, keywords=keywords, main_image_url=main_image_url, web_url=web_url))
    return snippets

with open("json.json", "r") as f:
    js = json.load(f)

parsed = list_snippets(js)
for i in parsed:
    print(type(i.title))