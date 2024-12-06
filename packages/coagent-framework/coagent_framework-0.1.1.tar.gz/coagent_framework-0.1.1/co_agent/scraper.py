from co_agent import database

class BlogScraper:
    def __init__(self, name: str):
        self.name = name
        print("Enter Master URL of the Blog you want Co-Agent to make LinkedIn Posts of:")
        master_url = str(input())
        self.master_url = master_url
        print("----------------------------------------------------------------------")

    def scrape(self):
        database.scrape_blog(self.master_url)