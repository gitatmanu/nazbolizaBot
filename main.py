import os, json, tweepy
from time import sleep
from dotenv import load_dotenv
load_dotenv()
from tweepy import Stream
from tweepy.streaming import StreamListener

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from generate_nazbol_name import generate_nazbol_name

# Firefox webdriver
options = webdriver.FirefoxOptions()
options.add_argument('--disable-extensions')
options.add_argument("--headless")
executable_path = os.path.join(os.path.dirname(__file__), 'drivers/geckodriver')
user_agent = 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36'
profile = webdriver.FirefoxProfile()
profile.set_preference('general.useragent.override', user_agent)


class Listener(StreamListener):
    def on_data(self, tweet):
        tweet = json.loads(tweet)
        bot_name = 'nazbolizabot'
        if tweet['user']['screen_name'].lower() == bot_name: # If it is a bot interaction
            return

        if hasattr(tweet,'retweeted_status'): # If it is a retweet
            return

        if '@' + bot_name not in tweet['text'].lower(): # Has not mentioned
            return


        if tweet['in_reply_to_status_id'] and tweet['text'].lower().count('@' + bot_name) == 1: # If it is a reply
            return

        print('Procesando tuit de: '+ tweet['user']['screen_name'])
        respond_tweet(tweet)


def respond_tweet(tweet):
    api, auth = set_up_auth()

    tweet_url = 'https://twitter.com/{}/status/{}'.format(
        tweet['user']['screen_name'], tweet['id'])
    
    generate_image(tweet_url, tweet['user']['name'])

    api.update_with_media("./capture.png",
                            status="",
                            in_reply_to_status_id=tweet['id_str'],
                            auto_populate_reply_metadata=True
                            )


def set_up_auth():
    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_KEY'), os.getenv('ACCESS_SECRET'))
    api = tweepy.API(auth)
    return api, auth


def follow_stream():
    api, auth = set_up_auth()
    listener = Listener(StreamListener)
    stream = Stream(auth, listener)
    stream.filter(track=[os.getenv('ACCOUNT_NAME')])


def generate_image(tweet_url, name):
    # Init driver
    driver = webdriver.Firefox(executable_path=executable_path, options=options, firefox_profile=profile, service_log_path=os.devnull)
    driver.set_window_position(0, 0)
    driver.set_window_size(500, 700)

    # Modify HTML
    driver.get(tweet_url)
    sleep(8)
    try:
        nazbol_name = generate_nazbol_name()
        elements = driver.find_elements_by_xpath(
            "//span[contains(text(), '" + name + "')]")
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
    sleep(1)
    driver.get_screenshot_as_file("capture.png")
    print('Procesado.')
    driver.close()



if __name__ == '__main__':
    follow_stream()