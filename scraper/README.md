This scraper utilises a Rightmove scraper previously built, available here: https://github.com/toby-p/rightmove_webscraper.py

This is used to get a basic list of rightmove properties, including their URL.

Then, we used the Python package scrapy to build a spider that will scrape all of the results on a given input URL (which we did by postcode as you can see in the swpostcode document in /postcodes): https://docs.scrapy.org/en/latest/intro/tutorial.html