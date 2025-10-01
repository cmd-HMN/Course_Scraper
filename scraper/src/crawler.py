import random
import time
import threading
from tqdm import tqdm
from _config import ScraperConfig
from _cleaner import cleaner
from _crawler_helper_func import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def crawl(links, sc: ScraperConfig, crawler, return_=False, stop_after_min=5, res_min=1.5):
    print('Starting crawling....')
    pbar = tqdm(range(sc.iterations), total=sc.iterations, desc='Starting crawling....', position=0, colour='blue', leave=True)
    links = set(links)
    start = 0
    isRest = False
    stop = False

    def check_min(stop):
        nonlocal start, isRest
        while not stop:
            time.sleep(1)
            start += 1
            if start >= int(stop_after_min * 60):
                isRest = True
                start = 0

    t = threading.Thread(target=check_min, args=(stop,), daemon=True)
    t.start()
    
    for _ in pbar:
        link = links.pop()
        if not link or len(link) <= 10:
            pass

        try:
            sl = random.uniform(5, 10)
            pbar.set_description(f'Sleeping for {sl:.1f}')
            time.sleep(sl)
        except Exception as e:
            print('Passing sleep', type(e).__name__)
            pbar.set_description(f'Passing Sleep: {type(e).__name__}')
      
        try:
            pbar.set_description(f'Calling crawler: {link[:40]}...')
            crawler.get(link)
            
            clinks = crawler.find_elements(By.XPATH, '//a[@href]')
            new_links = set()
            for l in clinks:
                try:
                    href = l.get_attribute('href')
                    if href and all(x not in href for x in ['/articles', '?authMode', '//chat', '/support']):
                        new_links.add(href)
                except Exception as e:
                    pbar.set_description(f'Error: {type(e).__name__}')
            
            links |= new_links
            write_cfile(list([*links, link]), filename=f'{sc.path_}/crawler.txt')

            print('Successfully crawled:', link, 'New links found:', len(new_links), 'Total links:', len(links))

        except Exception as e:
            print('Error occurred while crawling:', link)
            pbar.set_description(f'Error: {type(e).__name__}')

        if isRest:
            isRest = False
            try:
                stop = True
                rest_for_min(crawler, pos=0, minu=res_min)
                stop = False
                
            except Exception as e:
                crawler.quit()
                print('Error during rest:', type(e).__name__)

    crawler.quit()
    print('Crawling finished.')
    if return_:
        return links


def crawl_handler(sc:ScraperConfig, res_min, stop_after_min, overwrite):
    state, links = read_cfile(filename=f'{sc.path_}/crawler.txt')

    if links and state and not overwrite and len(links) != 0:
        print('The file "crawler.txt" was found')
        return
    else:
        print('Overwriting "crawler.txt"' if overwrite else 'Using Default link from "_config.py"')
        links = set([sc.default_link])


    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    crawler  = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=options
    )
    try:
        crawl(links, sc=sc, crawler=crawler, res_min=res_min, stop_after_min=stop_after_min)
        cleaner(sc=sc)
        
    except KeyboardInterrupt:
        crawler.quit()
        print('Crawling interrupted.')

