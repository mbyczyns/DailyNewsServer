import datetime
from classes import Article_snippet


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