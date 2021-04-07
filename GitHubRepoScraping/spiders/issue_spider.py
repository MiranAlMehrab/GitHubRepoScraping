import json
import scrapy


class IssuesSpider(scrapy.Spider):
    name = "issues"
    start_urls = ["https://api.github.com/repos/facebook/react-native/issues?page=1&per_page=100"]


    def parse(self, response):
        page = response.url
        fp = open("commits.csv", "a+")
        
        for item in json.loads(response.body):

            row = {}

            row['url'] = item['url']
            row['number'] = item['number']
            row['title'] = item['title']
            row['body'] = item['body']
            row['comments'] =  item['comments']
            row['assignee'] = item['assignee']['url'] if item['assignee'] else None
            row['assignees'] = [] 
            
            for assignee in item['assignees']: 
                row['assignees'].append(assignee['url'])
                 
            row['created_at'] = item['created_at']
            row['closed_at'] = item['closed_at']
            
            fp.write(json.dumps(row))
            fp.write("\n")
            
        curr_page_number = page.split("?")[1]
        curr_page_number = curr_page_number.split("&")[0]
        curr_page_number = curr_page_number.split("=")[1]
        next_page_number = int(curr_page_number) + 1

        yield scrapy.Request("https://api.github.com/repos/facebook/react-native/issues?page="+str(next_page_number)+"&per_page=100", callback = self.parse)