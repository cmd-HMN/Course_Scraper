class ScraperConfig:
    # should be in the form of xpath
    rating_selector = '//div[contains(@aria-label,"stars")]'
    rating_count = '//p[contains(text(),"reviews")]'
    level_selector = '//div[contains(text(),"level")]'

    # if the course is consists on courses
    cours_ovw = '//div[contains(text(), "months")]'
    
    # courses container
    cour_cont = '//span[text()="Course 1"]/ancestor::div[contains(@class, "css-")][last()]'
    cour_path = './/h3/ancestor::div[1]'
    cour_title = './/h3/a'
    isCourse = '//a[text()="Courses"]'

    # instructor
    ins_button = '//button[.//span[contains(text(),"+")]]'
    ins = '//div[@role="dialog"]//div[contains(@class,"cds-grid-item")]'
    close_ins = '//button[@aria-label="Close"]'
    isMoreIns = '//span[contains(text(),"+")]'

    one_ins = '//span[contains(normalize-space(.), "Instructor:")]'
    one_ins_link = './/a' 

    more_ins_name = './/a/span'
    more_ins_link = './/a'

    # offered by
    offer_by = '//h3[contains(text(), "Offered by")]/following::a[1]'

    # review 
    rev_cont = '//div[contains(@class, "review review-text review-page-review")]'
    rating_star = './/div[@role="img"]//span'
    review_button = '//a[.//span[contains(normalize-space(.), "View more reviews")]]'
    isReview = '//span[contains(normalize-space(.), "View more reviews")]'
    review_name = './/p[contains(@class,"reviewerName")]'
    
    #-----------------------
    # error in the path will see later
    skills_selector = '//h2[contains(.,"Skills")]/following::ul[1]//span'
    #-----------------------
    view_skills = '//button[.//span[text()="View all skills"]]'

    # crawler
    default_link = 'https://www.coursera.org/'
    # crawler iterations
    iterations = 1000

    path_ = '../../assets/raw_data'

    # cleaning
    clean_format = ['/learn', '/professional-certificates', '/specializations']
