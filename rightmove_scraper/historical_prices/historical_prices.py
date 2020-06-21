import scrapy
import json
import os
import subprocess
import time
import pandas as pd
import hashlib
import re
from rightmove_webscraper import RightmoveData

urls = pd.DataFrame()


class rightmoveSpider(scrapy.Spider):

    base_url = "https://www.rightmove.co.uk/"

    name = "rightmove"
    input_json_file = "./postcodes/swpostcodes.json"
    file_address = './'+input_json_file
    scrapy_proj_dir = './rightmove_scraper/spiders/'
    description = ''
    # Change dir to scrapy Jumpon Crawler
    os.chdir(scrapy_proj_dir)

    # Open json file and read all URLs
    with open(file_address, 'r') as links_file:
        # Load json stream
        urls = json.load(links_file)

    start_urls = []
    print("Started")
    # Loop every item
    for value in urls:
        start_urls.append(value['url'])

    def start_requests(self):

        propertyurl = ''
        for url in self.start_urls:
            rm = RightmoveData(url)
            apidata = rm.get_results
            apidata.drop(["search_date"], axis=1, inplace=True)
            apidata.drop(["postcode"], axis=1, inplace=True)
            apidata['Full Description'] = ''
            apidata['Agent Name'] = ''
            apidata['Agent Address'] = ''
            apidata['postcode'] = ''
            apidata['longitude'] = ''
            apidata['latitude'] = ''
            apidata['viewType'] = ''
            apidata['propertyType'] = ''
            apidata['propertySubType'] = ''
            apidata['added'] = ''
            apidata['maxSizeFt'] = ''
            apidata['retirement'] = ''
            apidata['preOwned'] = ''

            filename = 'out/' + hashlib.md5(url.encode('utf-8')
                                            ).hexdigest() + '.json'
            apidata.to_json(filename, orient='split')
            for index, row in apidata.iterrows():
                propertyurl = row["url"]
                yield scrapy.Request(propertyurl, self.parse, meta={'index': index, 'filename': filename})

    def parse(self, response):
        dfrow = response.meta.get('index')
        filename = response.meta.get('filename')

        df = pd.read_json(filename, orient='split')

        selling_agent = response.css('div.overflow-hidden')
        selling_agent_name = selling_agent.css('strong::text').get()
        selling_agent_address = selling_agent.css('address::text').get()
        
        items = response.xpath("//script[contains(., 'longitude')]/text()")
        txt = items.extract_first()
        start = txt.find('property') + 10
        end = txt.find('));')
        json_string = txt[start:end]
        
        data = json.loads(json_string)
        
        locationdata = data['location']
        postcode = locationdata.get('postcode')
        longitude = locationdata.get('longitude')
        latitude = locationdata.get('latitude')
        
        propertyinfo = data['propertyInfo']
        viewType = propertyinfo.get('viewType')
        propertyType = propertyinfo.get('propertyType')
        propertySubType = propertyinfo.get('propertySubType')
        added = propertyinfo.get('added')
        maxSizeFt = propertyinfo.get('maxSizeFt')
        retirement = propertyinfo.get('retirement')
        preOwned = propertyinfo.get('preOwned')
        
        propertyfilename = 'out/properties/' + \
            str(data['propertyId']) + '.html'
        with open(propertyfilename, 'w') as html_file:
            html_file.write(response.text)

        description = response.xpath(
            'string(//p[@itemprop="description"])').extract_first()
        df.at[dfrow, 'Full Description'] = description
        df.at[dfrow, 'Agent Address'] = selling_agent_address
        df.at[dfrow, 'Agent Name'] = selling_agent_name
        df.at[dfrow, 'postcode'] = postcode
        df.at[dfrow, 'longitude'] = longitude
        df.at[dfrow, 'latitude'] = latitude
        df.at[dfrow, 'viewType'] = viewType
        df.at[dfrow, 'propertyType'] = propertyType
        df.at[dfrow, 'propertySubType'] = propertySubType
        df.at[dfrow, 'added'] = added
        df.at[dfrow, 'maxSizeFt'] = maxSizeFt
        df.at[dfrow, 'retirement'] = retirement
        df.at[dfrow, 'preOwned'] = preOwned

        df.to_json(filename, orient='split')
