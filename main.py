import tweepy, os

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
options = webdriver.FirefoxOptions()
options.add_argument('--disable-extensions')
options.add_argument("--headless")

user_agent = 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36'
profile = webdriver.FirefoxProfile()
profile.set_preference('general.useragent.override', user_agent)


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
    driver.set_window_position(0,0)
    driver.set_window_size(366, 1300)
    driver.get(tweet_url)
    sleep(10)
    try:
        nazbol_name = generate_nazbol_name()
        elements = driver.find_elements_by_xpath("//span[contains(text(), '"+ name +"')]")
        print(elements)
        JS_ADD_TEXT_TO_INPUT = """
        arguments[0].textContent="{}"
        var elm = arguments[0];
        elm.dispatchEvent(new Event('change'));
        """.format(nazbol_name)

        for element in elements:
            driver.execute_script(JS_ADD_TEXT_TO_INPUT, element)
    except NoSuchElementException:
        pass

    # Make capture
    sleep(5)
    driver.get_screenshot_as_file("temp/capture.png")

if __name__ == '__main__':
    filename = os.path.join(os.path.dirname(__file__), 'drivers/geckodriver.exe')
    driver = webdriver.Firefox(executable_path=filename, options=options, firefox_profile=profile)

    mentions = api.mentions_timeline(get_last_mention_id(), tweet_mode = 'extended')

    for mention in reversed(mentions):
        if 'nazbolizaBot' in mention.__dict__['author'].screen_name:
            store_last_mention_id(mention.id)
            continue

        tweet_url = 'https://twitter.com/{}/status/{}'.format(mention.__dict__['author'].screen_name, mention.__dict__['id'])
        generate_image(tweet_url, mention.__dict__['user'].name, driver)

        api.update_with_media("temp/capture.png",
        status="",
        in_reply_to_status_id=mention.id_str,
        auto_populate_reply_metadata=True
        )
        store_last_mention_id(mention.id)
    driver.close()
