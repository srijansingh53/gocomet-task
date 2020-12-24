import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import json
import time
from selenium.common.exceptions import NoSuchElementException


# fetch blogs based on tags
def get_blogs(tag,page):
    path = "F:/Downloads/Compressed/chromedriver"
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(executable_path=path, options=options)
    
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
        temp = blog.find_element_by_class_name("postMetaInline-authorLockup")
        temp = temp.find_elements_by_tag_name("a")

        # will currently deal only in writer and date
        title = blog.find_element_by_tag_name('h3')
        blogs.append({
            'writer': temp[0].text,
            'date': temp[-1].text,
            'link': temp[-1].get_attribute('href'),
            'title': title.text,
        })
    driver.close()
    return {'tags' : tags, 'blogs': blogs}


def get_details(link):

    start = time.time()

    path = "F:/Downloads/Compressed/chromedriver"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(executable_path=path, options=options)
    
    driver.get(link)
    time.sleep(5)

    article_title = driver.find_elements_by_tag_name("article")[0]

    # fetching date+time together
    while True:
        try:
            all_spans = article_title.find_elements_by_tag_name("span")
            for dt in all_spans: 
                if "read" in dt.text:
                    date_time = dt.text  
                    print('date time fetched')
                    break
            break
        except:
            time.sleep(5)
    # print(date_time)

    #fetching all tags inside blog
    related_tags_list = []
    all_links = driver.find_elements_by_tag_name("a")

    for link in all_links:
        url = link.get_attribute('href')
        flag = url.find("/tag/")
        # print(flag)
        if flag != -1:
            related_tags_list.append(link.text)
        flag = url.find("/tagged/")
        if flag != -1:
            related_tags_list.append(link.text)
    # print(related_tags_list)

    #fetching claps and response

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    num_claps = "NA"
    num_responses = "NA"
    response_button = None
    
    
    for i in range(2,7):
        print(i)
        try:
            svg_clap = driver.find_element_by_xpath("//*[@id='root']/div/div[3]/div[5]/div/div[1]/div/div["+str(i)+"]/div/div[1]/div[1]/span[2]/div/div[2]/div/h4/button")
            # //*[@id="root"]/div/div[3]/div[5]/div/div[1]/div/div[5]/div[1]/div[1]/span[2]/div/div[2]/div/h4/button
            # //*[@id="root"]/div/div[3]/div[5]/div/div[1]/div/div[4]/div/div[1]/div[1]/span[2]/div/div[2]/div/h4/button
            num_claps = svg_clap.text
            if num_claps is not 'NA':
                break

        except NoSuchElementException:
            try:
                svg_clap = driver.find_element_by_xpath("//*[@id='root']/div/div[3]/div[5]/div/div[1]/div/div["+str(i)+"]/div[1]/div[1]/span[2]/div/div[2]/div/h4/button")
                num_claps = svg_clap.text
                if num_claps is not 'NA':
                    break
            except:
                num_claps = 'NA'
        

    for i in range(2,7):
        try:
            svg_resp = driver.find_element_by_xpath("//*[@id='root']/div/div[3]/div[5]/div/div[1]/div/div["+str(i)+"]/div/div[1]/button/div/div[2]/h4")
            # //*[@id="root"]/div/div[3]/div[5]/div/div[1]/div/div[5]/div[1]/button/div/div/h4
            # //*[@id="root"]/div/div[3]/div[5]/div/div[1]/div/div[4]/div/div[1]/button/div/div[2]/h4
            num_responses = svg_resp.text
            if num_responses is not 'NA':
                break
            # //*[@id="root"]/div/div[3]/div[5]/div/div[1]/div/div[5]/div[1]/button/div/div/h4
        except NoSuchElementException:
            try:
                svg_resp = driver.find_element_by_xpath("//*[@id='root']/div/div[3]/div[5]/div/div[1]/div/div["+str(i)+"]/div[1]/button/div/div/h4")
                num_responses = svg_resp.text
                if num_responses is not 'NA':
                    break
            except:
                num_responses = 'NA'
    num_claps = num_claps.split(' ')[0]
    num_responses = num_responses.split(' ')[0]
    print(num_claps, num_responses)

    # fetching comments
    for i in range(2,7):
        try:
            response_button = driver.find_element_by_xpath("//*[@id='root']/div/div[3]/div[5]/div/div[1]/div/div["+str(i)+"]/div[1]/button")
            if response_button is not None:    
                break
        except NoSuchElementException:
            try:
                response_button = driver.find_element_by_xpath("//*[@id='root']/div/div[3]/div[5]/div/div[1]/div/div["+str(i)+"]/div/div[1]/button")
                if response_button is not None:    
                    break
            except:
                response_button = None

    comments_list = []
    if response_button and num_responses!='NA':
        response_button.click()
        time.sleep(3)
        n = int(num_responses)
        n = min(5,n)
        if n==1:
            try:
                responder = driver.find_element_by_xpath("//*[@id='root']/div/div[3]/div[2]/div[2]/div[3]/div/div/div/div[1]/div/div[2]/div/a/h4")
                # //*[@id="root"]/div/div[3]/div[2]/div[2]/div[3]/div[1]/div/div/div[1]/div/div[2]/div/a/h4
                # //*[@id="root"]/div/div[3]/div[2]/div[2]/div[3]/div[1]/div/div/div[1]/div/div[2]/div/a/h4
                comment_text = driver.find_element_by_xpath("//*[@id='root']/div/div[3]/div[2]/div[2]/div[3]/div/div/div/div[2]/pre/div/h4/div")
                # //*[@id="root"]/div/div[3]/div[2]/div[2]/div[3]/div[1]/div/div/div[3]/pre/div/h4/div
                # //*[@id="root"]/div/div[3]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/pre/div/h4/div
            except:
                comments_list = []
        else:

            for i in range(1,n+1):
                try:
                    responder = driver.find_element_by_xpath("//*[@id='root']/div/div[3]/div[2]/div[2]/div[3]/div["+str(i)+"]/div/div/div[1]/div/div[2]/div/a/h4")
                    # //*[@id="root"]/div/div[3]/div[2]/div[2]/div[3]/div[1]/div/div/div[1]/div/div[2]/div/a/h4
                    comment_text = driver.find_element_by_xpath("//*[@id='root']/div/div[3]/div[2]/div[2]/div[3]/div["+str(i)+"]/div/div/div[2]/pre/div/h4/div")
                    # //*[@id="root"]/div/div[3]/div[2]/div[2]/div[3]/div[1]/div/div/div[1]/div/div[2]/div/a/h4
                    # //*[@id="root"]/div/div[3]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/pre/div/h4/div
                except:
                    break
                comments_list.append({
                    'responder': responder.text,
                    'comment': comment_text.text,
                })

    print(comments_list)
    driver.close()
    return {
        'date_time' : date_time,
        'num_claps': num_claps,
        'num_responses': num_responses,
        'comments_list': comments_list,
        'related_tags': related_tags_list,
        'burst_time': int(time.time()-start),
    }


# data = get_details("https://towardsdatascience.com/is-python-really-a-bottleneck-786d063e2921")





