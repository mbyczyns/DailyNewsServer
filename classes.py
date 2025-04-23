class Article_snippet:
    def __init__(self, title, pub_date, main_image_url, print_headline, web_url, keywords):
        self.title = title
        self.pub_date = pub_date
        self.main_image_url = main_image_url
        self.print_headline = print_headline
        self.web_url = web_url
        self.keywords = keywords

    def to_dict(self):
        return {
            "title": self.title,
            "print_headline": self.print_headline,
            "pub_date": self.pub_date,
            "keywords": self.keywords,
            "main_image_url": self.main_image_url,
            "web_url": self.web_url
        }
    
    
sections =["Health", "Sports", "Books", "Arts", "Fashion"]
desks =["Business","Science", "Politics", "Weather", "Travel"]
