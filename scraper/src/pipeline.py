from crawler import crawl_handler
import argparse
from _config import ScraperConfig
from scrape import scraper_handler
import os

print('This is the Coursera Scraper pipeline')


print('\nTo change something, look into the scraper/_config.py....[You might find something interesting]')

sc = ScraperConfig()

parser = argparse.ArgumentParser(
        prog='Coursera Scraper',
        description='Program run the scraper with the crwaler')

# crawler
parser.add_argument('-co', '-overwrite', type=bool, default=False, help='overwite the crawler.txt')
parser.add_argument('-cinterval', '-crawl_interval', type=float, default=5, help='The time interval in which the crawler works and afterwards takes a rest')
parser.add_argument('-crest', '-crawl_rest', type=float, default=1.5, help='The rest time of crawler after interval')

# scraper
parser.add_argument('-sinterval', '-scraper_interval', type=float, default=5, help='The time interval in which the scraper works and afterwards takes a rest')
parser.add_argument('-srest', '-scraper_rest', type=float, default=1.5, help='The rest time of scrape after interval')
parser.add_argument('-scount', '-scraper_link_count', type=int, default=None, help='This argument help u scrape the "x" amount of links')

args = parser.parse_args()



# crwaler
try:
    if os.path.exists('crawler.txt') and not args.co:
        crawl_handler(sc, args.crest, args.cinterval, overwrite=args.co)
    else:
        crawl_handler(sc, args.crest, args.cinterval, overwrite=args.co)
except Exception as e:
    print(f'Sometihng went wrong: {type(e).__name__}')

# scraper
try:
   scraper_handler(sc, args.sinterval, args.srest, args.scount)
except Exception as e:
    print(f'Something went wrong: {type(e).__name__}')


print('Exiting..')
print('Bye from "cmd-HMN"')
