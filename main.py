import tweepy, os, emoji

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep
from generate_nazbol_name import generate_nazbol_name

from dotenv import load_dotenv
load_dotenv()


CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

# Chrome webdriver
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_argument("--headless")
options.add_experimental_option("mobileEmulation", { "deviceName": "Pixel 2" })

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


def get_last_mention_id():
    file = open('mentions_id.txt', 'r')
    lineList = file.readlines()
    file.close()

    if not lineList:
        return None

    id = int(lineList[-1])
    return id

def store_last_mention_id(id):
    with open('mentions_id.txt', 'a') as file:
        file.write(str(id) + '\n')
        file.close()

def document_initialised(driver):
    return driver.execute_script("console.log('cargao')")

def generate_image(tweet_url, name, driver):
    # Scrap web and modify HTML
    driver.get(tweet_url)
    sleep(5)

    try:
        element = driver.find_element_by_xpath("//span[contains(text(), '"+ name +"')]")
        element.send_keys("\ud83c\uddf9\ud83c\uddec \ud83c\uddfb\ud83c\uddf3")
        driver.execute_script("arguments[0].textContent='"+ generate_nazbol_name() +"'", element)
    except NoSuchElementException:
        pass

    # Make capture
    driver.get_screenshot_as_file("temp/capture.png")

if __name__ == '__main__':
    driver = webdriver.Chrome('/home/manel/nazbolizaBot/chromedriver', options=options)
    mentions = api.mentions_timeline(get_last_mention_id(), tweet_mode = 'extended')

    for mention in reversed(mentions):
        if not '@nazbolizaBot' in mention.__dict__['full_text']:
            store_last_mention_id(mention.id)
            continue

        tweet_url = 'https://twitter.com/{}/status/{}'.format(mention.__dict__['author'].screen_name, mention.__dict__['id'])
        generate_image(tweet_url, mention.__dict__['user'].screen_name, driver)

        api.update_with_media("temp/capture.png",
        status="",
        in_reply_to_status_id=mention.id_str,
        auto_populate_reply_metadata=True
        )
        store_last_mention_id(mention.id)
    driver.close()
