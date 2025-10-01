import random
from tqdm import tqdm
import threading
from _crawler_helper_func import read_cfile
from _scraper_helper_func import  *
from selenium import webdriver
from _config import ScraperConfig
from _crawler_helper_func import rest_for_min
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class CoursesPage:
    def __init__(self, isMoreIns, sc: ScraperConfig, driver, ltype=None):
        self.ltype = ltype
        self.sc = sc
        self.driver = driver
        self.isMoreIns = isMoreIns
        self.data = None

    def scrape(self):
        title = self.driver.title
        level = get_level(self.sc, self.driver)
        rating, rcount = get_rating(self.sc, self.driver)
        olink, offer =  who_offer(self.sc, self.driver)
        sub_courses, subc_links = get_courses(self.sc, self.driver)
        skills = get_skills(self.sc, self.driver)
        time.sleep(2)
        names, links = get_instructor(self.isMoreIns, self.sc, self.driver)
        
        self.data = {
            'Title' :title,
            'Level': level,
            'Organization': offer,
            'Organization_Link': olink,
            'Rating': rating,
            'Rating count': rcount,
            'Course type': self.ltype,
            'Skills': skills,
            'Courses': sub_courses,
            'Courses_Link': subc_links,
            'Instructors': names,
            'links': links
        }

        csv_handler(f'{self.sc.path_}/courses.csv', self.data)


class CoursePage:
    def __init__(self, isMoreIns, sc, driver, ltype=None):
        self.ltype = ltype
        self.sc = sc
        self.driver = driver
        self.isMoreIns = isMoreIns
        self.data = None
        self.user_data = None

    def scrape(self):
        title = self.driver.title
        level = get_level(self.sc, self.driver)
        rating, rcount = get_rating(self.sc, self.driver)
        olink, offer =  who_offer(self.sc, self.driver)
        names, links = get_instructor(self.isMoreIns, self.sc, self.driver)
        skills = get_skills(self.sc, self.driver)
        time.sleep(2)
        reviews, user = get_reviews(self.sc, self.driver)
       
        self.data = {
            'Title' :title,
            'Level': level,
            'Organization': offer,
            'Organization_Link': olink,
            'Rating': rating,
            'Rating count': rcount,
            'Course type': self.ltype,
            'Skills': skills,
            'Instructors': names,
            'links': links,
        }

        self.user_data = {
            'Title' :title,
            'User': user,
            'Reviews': [str(r) for r in reviews]
        }

        csv_handler(f'{self.sc.path_}/course.csv', self.data)
        csv_handler(f'{self.sc.path_}/user_rating.csv', self.user_data)

def link_type(link):
    if '/professional-certificates' in link:
        return 'professional-certificates'

    elif '/specialization' in link:
        return 'specialization'

    return 'course'

def scrape_links(links, sc, driver, stop_after_min=5, res_min=1):
    pbar = tqdm(links, total=len(links), desc='\nStarting Scraping....', colour="yellow")
    
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

    for l in pbar:
        sl = random.uniform(3, 5)
        pbar.set_description(f'Waiting for {sl:.2f} sec......') 
        time.sleep(sl)
        driver.get(l)

        pbar.set_description('Getting page intution....')
        
        isCourse, isMoreIns, isReview = get_page_intution(sc, driver)

        pbar.set_description(f'Scraping {l[:40]}')

        if not (isCourse or isReview):
            pass

        ltype = link_type(l)
        
        try:
            if isCourse and not isReview:
                CoursesPage(isMoreIns, sc, driver, ltype=ltype).scrape()

            elif isReview:
                CoursePage(isMoreIns, sc, driver, ltype=ltype).scrape()

            if isRest:
                isRest = False
                try:
                    stop = True
                    rest_for_min(driver, minu=res_min)
                    stop = False
                except Exception as e:
                    print(f'Error: {type(e).__name__}')
        except Exception as e:
            pbar.set_description(f'Error: {type(e).__name__}')

    print('Scraping Completed')


def scraper_handler(sc, stop_after_min=5, res_min=1, scount=None):
    state, links = read_cfile(f'{sc.path_}/cleaned.txt')

    if not state or links == None:
        raise Exception('"cleaned.txt" wasn\'t found')
     
    if scount:
        links = links[:scount]

    print('\nStaring Scraping...\n')
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver  = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=options
    )
    try:
        scrape_links(links, sc, driver, stop_after_min, res_min)
    except:
        print('Exiting')
        driver.quit()
