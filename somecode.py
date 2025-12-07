image = driver.find_element(By.ID, "post-image")
image_url = image.get_attribute("src")

r = requests.get(image_url)
filename = os.path.join(SAVE_FOLDER, f"{post_id}.webp")
with open(filename, "wb") as f:
    f.write(r.content)

iframes = driver.find_elements(By.TAG_NAME, "iframe")
print("Found iframes:", len(iframes))

video = driver.find_element(By.CSS_SELECTOR, "video:nth-child(1)")
video = driver.find_element(By.TAG_NAME, "video")
video = driver.find_element(By.XPATH, "//video[1]")

video:nth-child(1)

image = driver.find_element(By.ID, "post-image")
image_url = image.get_attribute("src")

r = requests.get(image_url)
filename = os.path.join(SAVE_FOLDER, f"{post_id}.webp")
with open(filename, "wb") as f:
    f.write(r.content)
