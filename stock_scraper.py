import scrapy
from scrapy.crawler import CrawlerProcess
import argparse
import os

class StockscraperSpider(scrapy.Spider):

    name = "stockscraper"
    allowed_domains = ["www.moneycontrol.com"]
    start_urls = ["https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=7"]

    def __init__(self, stock_name):
        self.stock_name=stock_name
        
    def parse(self, response):
        flag=False
        stocks=response.css('div.MT10 table.tbldata14 tr')
        stocks.pop(0)

        for stock in stocks:
            stock_link="moneycontrol.com"+stock.css("td.brdrgtgry a")[0].attrib["href"]
            stock_link_data=stock_link.split("/")
            if self.stock_name in stock_link_data:
                flag=True
                break
        if not flag:
            yield None
        else:
            yield response.follow(stock_link, callback=self.ratio_link_find)

    def ratio_link_find(self,response):
        ratio_link=response.css('div.financials_container div.sub2menu_content div.right_block div.quick_links li a')[7].attrib['href']
        yield response.follow(ratio_link, callback=self.ratio_stat_find)

    def ratio_stat_find(self,response):
        ratios={}
        stock_name=response.css('h1.pcstname::text').get()
        stage1=response.css('table.mctable1  tr')
        stage2=stage1.css('tr')

        for ratio in stage2:
            
            un_class_name=ratio.css('tr').attrib['class']

            if un_class_name=='lightbg' or un_class_name=='darkbg':
                continue
            else:
                values=ratio.css('td::text').getall()[:-1]

                ratio_name=values[0]
                f_ratio_vals=values[1:len(values)]
                r_len=len(f_ratio_vals)
                b_len=5-r_len

                if r_len<5:
                    for b in range(b_len):
                        f_ratio_vals.append(0)
                
                ratios[ratio_name]=f_ratio_vals
                
        yield ratios

def process(stock_name):
    if os.path.exists("stock.json"):
        os.system("rm stock.json")

    process = CrawlerProcess(
        settings={
        "FEEDS": {
            "stock.json": {"format": "json"},
        },
    }
    )
    process.crawl(StockscraperSpider, stock_name=stock_name)
    process.start()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    stock_name=parser.add_argument('--stock_name',default='aavasfinanciers')
    args = parser.parse_args()
    stock_name=args.stock_name
    process(stock_name)


