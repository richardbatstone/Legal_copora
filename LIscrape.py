import scrapy
import csv
import re
class LIsrape(scrapy.Spider):
    name = "LIscrape"

    def start_requests(self):

        URLlist = []

# I compiled a list of URLs to scrape (listed in TopDomains.txt) and added suffixes to URL before adding to the URLlist
# To run at command line: scrapy runspider LIscrape.py -s DOWNLOAD_DELAY=[x]

        with open('TopDomains.txt', 'r') as file:
            for line in file:
                link = line[:-1]
                for i in range(11):
                    j = str(i + 1)
                    link_ = link + j
                    URLlist.append(link_)

        for url in URLlist:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):

        # Select the first div tag with a data-clause-snippet attribute.
        # Extract and concatenate text from that tag into a single string.
        # The reference to 'class = "hlt-add"' is to parse the mark-up style text.
        # Remove \n breaks and strip leading/trailing white space.
        # Try searching on word characters. If present, start output from first character (i.e. remove punctuation
        # symbols etc. from start of string.)

        clause = response.xpath('//div[@data-clause-snippet]')[0:10]
        title = response.xpath('//title/text()').extract_first()
        for item in clause:
            text = "".join(item.xpath('./span[@class = "hlt-add"]/text()|./text()').extract())
            textout = re.sub('\\n','',text).strip()

            m = re.search('\w', textout)
            if m:
                textout = textout[m.start():]

            with open('LIdata_out.csv', 'a', newline='') as outfile:
                LIWriter = csv.writer(outfile, delimiter='|', quotechar='"',
                                      quoting=csv.QUOTE_MINIMAL)
                LIWriter.writerow([title, textout])
