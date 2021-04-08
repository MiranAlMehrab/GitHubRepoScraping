import json
import scrapy


class CommitsSpider(scrapy.Spider):
    name = "commits"
    start_urls = ["https://api.github.com/repos/facebook/react-native/commits?page=170&per_page=100"]


    def parse(self, response):
        page = response.url
        fp = open("commits.csv", "a+")
        
        for item in json.loads(response.body):

            row = {}
            row['url'] = item['commit']['url']
            row['message'] = item['commit']['message'] 
            row['author_url'] = item['author']['url'] if item['author'] else None 
            row['committer_url'] = item['committer']['url'] if item['committer'] else None 
            row['author_commit_date'] = item['commit']['author']['date'] if item['author'] else None 
            row['committer_commit_date'] = item['commit']['committer']['date'] if item['committer'] else None 
            
            fp.write(json.dumps(row))
            fp.write("\n")

        curr_page_number = page.split("?")[1]
        curr_page_number = curr_page_number.split("&")[0]
        curr_page_number = curr_page_number.split("=")[1]
        next_page_number = int(curr_page_number) + 1

        yield scrapy.Request("https://api.github.com/repos/facebook/react-native/commits?page="+str(next_page_number)+"&per_page=100", callback = self.parse)