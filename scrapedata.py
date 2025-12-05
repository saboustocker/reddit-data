from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By

# folder for images
SAVE_FOLDER = "images"

# set up selenium
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Firefox(
    service=Service(GeckoDriverManager().install()),
    options=options
)

url = "https://www.reddit.com/r/RealOrAI/top/?t=month"
driver.get(url)

wait = WebDriverWait(driver, 15)

# Wait for ANY articles to appear
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.w-full")))

# Scroll down on page
def scroll_to_load_all(driver, pause_time=2, max_scrolls=50):
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_count = 0

    while scroll_count < max_scrolls:
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scroll_count += 1

        # Wait for new content to load
        time.sleep(pause_time)

        # Check new height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # No new content loaded
            break
        last_height = new_height

    print(f"Finished scrolling after {scroll_count} scrolls")

def scroll_to_load_next(driver, pause_time=2, max_scrolls=3):
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_count = 0

    while scroll_count < max_scrolls:
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scroll_count += 1

        # Wait for new content to load
        time.sleep(pause_time)

        # Check new height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # No new content loaded
            break
        last_height = new_height

    print(f"Finished scrolling after {scroll_count} scrolls")

# initialize results as an empty array
results = []
# keep count of seen IDs to avoid duplicates
seen_ids = set(result["id"] for result in results)

# Loop until no new IDs are added
while True: 
    before_count = len(seen_ids)

    # scroll three times
    scroll_to_load_next(driver)

    time.sleep(2)

    # find all posts that are currently loaded
    posts = driver.find_elements(By.CSS_SELECTOR, "article.w-full.m-0")


    # extract relevant info from post
    for post in posts:
        try:
            shreddit = post.find_element(By.TAG_NAME,"shreddit-post")

            # ID
            post_id = shreddit.get_attribute("id")
            
            # check if ID already exists
            if post_id in seen_ids:
                continue
            
            comment_count = shreddit.get_attribute("comment-count")
            post_title = shreddit.get_attribute("post-title")
            
            # Username
            username_el = post.find_element(By.CSS_SELECTOR, "a[aria-label^='Author:']")
            username = username_el.get_attribute("aria-label").replace("Author: ", "")

            # Date posted ("faceplate-timeago time")
            date_el = post.find_element(By.CSS_SELECTOR, "faceplate-timeago time")
            date_posted = date_el.get_attribute("datetime")

            # Upvotes ("score" attribute on shreddit-post)
            shreddit_post = post.find_element(By.CSS_SELECTOR, "shreddit-post")
            upvotes = shreddit_post.get_attribute("score")

            # Permalink
            permalink_el = shreddit_post.find_element(By.CSS_SELECTOR, "a[slot='full-post-link']")
            permalink = permalink_el.get_attribute("href")

            # Flair (inside shreddit-post-flair)
            try:
                flair_el = post.find_element(By.CSS_SELECTOR, "shreddit-post-flair span")
                flair = flair_el.text.strip()
            except:
                flair = None

            results.append({
                "id": post_id,
                "title": post_title,
                "username": username,
                "date_posted": date_posted,
                "upvotes": upvotes,
                "comments": comment_count,
                "permalink": permalink,
                "flair": flair
            })
            seen_ids.add(post_id)

        except Exception as e:
            print("Error on item:", e)
            continue
    
    after_count = len(seen_ids)

    if after_count == before_count:
        print("No new posts loaded, stopping scroll.")
        break


## Go through all the Links and Download stuff from individual pages
detailed_results = []

for post in results:
    post_id = post['id']
    url = post['permalink']
    print(url)
    driver.get(url)

    time.sleep(3)

    # get the comment by the realOrAIbot
    comment_divs = driver.find_elements(By.CSS_SELECTOR, "div[slot='comment']")

    comments_text = []

    for div in comment_divs[:10]:
        # get all visible text inside the div (works regardless of tags like p, h1, etc.)
        text = div.text.strip()
        if text: 
            comments_text.append(text)
    
    # append the id and all comments to detailed_results
    detailed_results.append({
        "id": post_id,
        "AI_score": comments_text[0],  # first comment
        "comment_2": comments_text[1],
        "comment_3": comments_text[2],
        "comment_4": comments_text[3],
        "comment_5": comments_text[4],
        "comment_6": comments_text[5],
        "comment_7": comments_text[6],
        "comment_8": comments_text[7],
        "comment_9": comments_text[8],
        "comment_10": comments_text[9]
    })

    print(comments_text[0])

    time.sleep(3)

    # Download Image / Video 
    

