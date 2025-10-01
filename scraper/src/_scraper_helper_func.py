import time
import csv
from _config import ScraperConfig
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _let_sleep_for(seconds):
    time.sleep(seconds)


def _get_element(path, driver):
    try:
        return driver.find_element(By.XPATH, path)
    except:
        return None

def _get_elements(path, driver):
    try:
        many = driver.find_elements(By.XPATH, path)
        return many
    except:
        return None


def press_button(path, driver, timeout=5):
    try:
        button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, path))
        )
        driver.execute_script("arguments[0].click();", button)
        return True
    except:
        return False


def get_page_intution(sc, driver):
    if _get_element(sc.isCourse, driver) != None:
        isCourse = True
    else:
        isCourse = False
    
    if _get_element(sc.isMoreIns, driver) != None:
        isMoreIns = True
    else:
        isMoreIns = False

    if _get_element(sc.isReview, driver) != None:
        isReview = True
    else:
        isReview = False

    return isCourse, isMoreIns, isReview


def get_level(sc, driver):
    level = _get_element(sc.level_selector, driver)
    return level.text if level != None else None


def get_courses(sc, driver):
    title = []
    links = []
    try:
        cour_cont = _get_element(sc.cour_cont, driver)
        courses =  _get_elements(sc.cour_path, cour_cont)
        if courses:
            for course in courses: 
                try:
                    cont = _get_element(sc.cour_title, course)
                    if cont:
                        title.append(cont.text)
                        links.append(cont.get_attribute("href"))
                except:
                    break
    except:
        title.append(None)
        links.append(None)

    return title, links

def get_skills(sc, driver):
    press_button(sc.view_skills, driver)
    skills = _get_elements(sc.skills_selector, driver)
    if skills:
        skill = [s.text for s in skills][:-1:2]
        return skill
    else:
        return None

def get_instructor(isMoreIns, sc, driver):
    names = []
    links = []
    if isMoreIns:
        press_button(sc.ins_button, driver)
        ins = _get_elements(sc.ins, driver)
         
        if ins == None:
            return None, None

        for block in ins:
            try:
                name = _get_element(sc.more_ins_name, block)
                if name == None:
                    raise Exception(f'name is {name}')
                else:
                    name = name.text
                    if name == '':
                        raise Exception(f'name is {name}')
            except:
                name = None
            try:
                link = _get_element(sc.more_ins_link, block)
                if link:
                    link = link.get_attribute('href')
            except:
                link = None

            if name == None:
                pass

            names.append(name)
            links.append(link)
        
        _let_sleep_for(1)
        press_button(sc.close_ins, driver)
    else:
        try:
            ins = _get_element(sc.one_ins, driver)
            if ins == None:
                raise Exception()
            names.append(ins.text)
            l = _get_element(sc.one_ins_link, ins)
            if l == None:
                raise Exception()

            links.append(l.get_attribute("href"))
        except:
            names.append(None)
            links.append(None)

    return names, links


def who_offer(sc, driver):
    offer = _get_element(sc.offer_by, driver)
    if offer:
        return offer.get_attribute('href'), offer.text
    else:
        return None, None

def get_rating(sc, driver):
    rcount = _get_element(sc.rating_count, driver)
    rating = _get_element(sc.rating_selector, driver)

    if rcount and rating:
        return rating.text, rcount.text.split(' ')[0].strip('(')

    else:
        return None, None


def get_review_rating(sc, review_block):
    stars = review_block.find_elements(By.XPATH,  sc.rating_star)
    rating_ = 0
    for s in stars:
        if "Filled Star" in s.get_attribute("outerHTML"):
            rating_ += 1
    return  rating_

def get_reviews(sc, driver):
    press_button(sc.review_button, driver=driver)
    try:
        reviews = _get_elements(sc.rev_cont, driver)
        stars = []
        names = []
        if reviews:
            for r in reviews:
                star = get_review_rating(sc, r)
                name = _get_element(sc.review_name, r)
                if star and name:
                    stars.append(star)
                    names.append(name.text.strip('By '))
        return stars, names
    except:
        raise Exception("Something went wrong")

def csv_handler(file_path, data):
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False
        
    def safe_str(x):
        return "" if x is None else str(x)

    data_to_write = {
        k: ", ".join(safe_str(i) for i in v) if isinstance(v, list) else safe_str(v)
        for k, v in data.items()
    }

    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(data_to_write.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(data_to_write)
