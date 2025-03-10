from datetime import datetime
import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import random
import re

def login_to_twitter(driver, username, password, phone=None):
    driver.get("https://x.com/i/flow/login")
    wait = WebDriverWait(driver, 10)

    # Step 1: Enter username/email
    username_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
    username_input.send_keys(username)
    time.sleep(random.uniform(1.5, 3))

    # Click 'Next' button
    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Next"]')))
    next_button.click()
    time.sleep(random.uniform(2, 4))

    try:
        # Step 2: Enter password
        password_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
        password_input.send_keys(password)
        time.sleep(random.uniform(1.5, 3))
    except Exception as e:
        print("Ins the error: ",e)
        print("Trying with phone number...")
        # If password field is not found, try entering phone number
        phone_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
        if phone:
            phone_input.send_keys(phone)
            time.sleep(random.uniform(1.5, 3))
            # Click 'Next' button again
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Next"]')))
            next_button.click()
            time.sleep(random.uniform(2, 4))
            # Try entering password again
            password_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
            password_input.send_keys(password)
            time.sleep(random.uniform(1.5, 3))

    # Click 'Log in' button
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Log in"]')))
    login_button.click()
    time.sleep(random.uniform(5, 7))




def clear_terminal():
    """Clears the terminal output dynamically to prevent scrolling."""
    os.system('cls' if os.name == 'nt' else 'clear')

def post_tweet(driver, tweet_text, browser_close=False, range_time=[1, 2]):
    """
    Automates posting tweets using robust XPaths (updated for March 2025)
    """
    first_time, second_time = range_time

    try:
        driver.get("https://twitter.com/home")
        wait = WebDriverWait(driver, 15)


        # Tweet input box (3 reliable options)
        tweet_box = wait.until(EC.presence_of_element_located((
            By.XPATH, '//div[@data-testid="tweetTextarea"]'  # Primary selector
            ' | //div[@aria-label="Post text"]'  # Fallback 1
            ' | //div[@role="textbox"]'  # Fallback 2

        )))

        tweet_box.click()
        time.sleep(random.uniform(2, second_time))
        tweet_box.send_keys(tweet_text)
        
        # Tweet button (with multiple fallbacks)
        tweet_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, '//div[@data-testid="tweetButton"]'  # Primary selector
            ' | //button//span[text()="Post"]'  # Text-based fallback
            ' | //div[@role="button"][.//span[text()="Post"]]'  # Role-based
        )))
        
        tweet_button.click()
        print("✅ Tweet posted successfully!")

    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
        # Implement emergency browser reset here
    finally:
        if browser_close:
            driver.quit()



def links_rollout(driver,tweet_text,range_time,repeat = 20,repeat_time = 2):
        # print("Repeat : ",repeat)
        # print("Repeat time: ",repeat_time)
        # Bypass webdriver detection by modifying navigator.webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Optionally, you can integrate selenium-stealth for further masking:
        from selenium_stealth import stealth
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
        )

        USERNAME =  os.getenv('EMAIL')
        PASSWORD = os.getenv("PASSWORD")
        PHONE_NUMBER = os.getenv("PHONE_NUMBER") # Add phone number if needed

        login_to_twitter(driver, USERNAME, PASSWORD, PHONE_NUMBER)
        print("Logged In Successfully...................")
    

        post_tweet(driver,tweet_text,browser_close=True,range_time=range_time)
        print("Last link is left open. Browser remains active.")

def main(tweet_text,count = 0,BASE_CONDITION = 5,range_time = [1,2],repeat = 10,repeat_time =  5):
    if(count == BASE_CONDITION):
        return "Max Retries Finished Please re run the Bot.."
    
    print("Tweet Text: ",tweet_text)
    # Get a single rotating 
    options = Options()
   

    # Additional options to help bypass detection:
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless=new")  # Enable  headless mode
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-web-security")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # # Randomize the user agent
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
    ]
    user_agent = random.choice(user_agent_list)
    options.add_argument(f'user-agent={user_agent}')

    # Initialize the driver with the above options
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(6.5)
    try:
        # Links roll out.
        links_rollout(driver,tweet_text,range_time,repeat=repeat,repeat_time=repeat_time)            
    except Exception as e:
        print("Exception Occured due to : ",e)
        print(f"Retrying........ {count+1}")
        main(tweet_text,count=count+1,repeat=repeat,repeat_time=repeat_time,BASE_CONDITION = BASE_CONDITION)


class Tweet:
    def __init__(self, title, content, hashtags):
        self.title = title
        self.content = content
        self.hashtags = hashtags
        self.timestamp = datetime.now()

    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content,
            'hashtags': self.hashtags,
            'timestamp': self.timestamp.isoformat()
        }

    def remove_hashtags(self,text):
        return re.sub(r'#\w+', '', text).strip()

    def remove_non_bmp(self,text):
        return ''.join(c for c in text if ord(c) <= 0xFFFF)

    def to_string(self):
        tweet = f"{self.remove_hashtags(self.title)}\n\n{self.remove_hashtags(self.content)}"
        tweet = self.remove_non_bmp(tweet)
        return tweet

    
    def tweet_post(self,tweet_data:str):
        try:
            main(tweet_data,range_time=[1,4],repeat=200,repeat_time=1,BASE_CONDITION  = 30)
        except Exception as e:
            raise e
