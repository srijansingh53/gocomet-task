import selenium
from selenium import webdriver
import json
import time



# fetch blogs based on tags
def get_blogs(tag,page):
    path = "F:/Downloads/Compressed/chromedriver"
    driver = webdriver.Chrome(executable_path=path)
    
    link = "https://medium.com/tag/" + tag
    driver.get(link)
    time.sleep(5)

    if driver.title=="Not Found – Medium":
        return None
    
    related_tags = driver.find_element_by_class_name("tags--postTags")
    related_tags_list = related_tags.find_elements_by_tag_name("a")

    tags = []
    for tag in related_tags_list:
        data = {
            'tag': tag.text,
            'tag_link': tag.get_attribute('href')
        }
        tags.append(data)

    # to scroll the page upto bottom of the page
    while(page > 0):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(8)
        page = page - 1
    
    blogs_list = driver.find_element_by_class_name("js-tagStream")
    blogs_list = blogs_list.find_elements_by_class_name("postArticle")

    blogs = []

    for blog in blogs_list:
        writerPublicationDate = blog.find_element_by_class_name("postMetaInline-authorLockup")
        writerPublicationDate = writerPublicationDate.find_elements_by_tag_name("a")

        # will currently deal only in writer and date
        title = blog.find_element_by_tag_name('h3')
        blogs.append({
            'writer': writerPublicationDate[0].text,
            'date': writerPublicationDate[-1].text,
            'link': writerPublicationDate[-1].get_attribute('href'),
            'title': title.text,
        })
    driver.close()
    return {'tags' : tags, 'blogs': blogs}