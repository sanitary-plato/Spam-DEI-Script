from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random
import string

def changer(input_string):

    # Convert the string to a list for easier manipulation
    chars = list(input_string)
    
    # If the string is too short to change two letters, return the original string
    if len(chars) < 2:
        return input_string
    
    # Select two unique random indices
    indices = random.sample(range(len(chars)), 2)
    
    # For each selected index, replace the letter with a random different letter
    for index in indices:
        # Get a random letter that is different from the current letter
        current_letter = chars[index]
        possible_letters = [letter for letter in string.ascii_letters if letter != current_letter]
        chars[index] = random.choice(possible_letters)
    
    # Convert back to a string and return
    return ''.join(chars)

def slow_type(element, text):
    """
    Type text slowly with a small delay between characters
    Adds realism and visibility to typing process
    """
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.09, 0.19))

def submit_form(url, email, location, zipcode, description):
    # Setup Firefox
    options = Options()
    options.add_argument("-profile")
    options.add_argument("CHANGE IT HERE")
    driver = webdriver.Firefox(options=options)
    
    try:
        # Navigate to the page
        driver.get(url)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
        
        # Find and fill the text fields by name with slow typing
        print("Typing email...")
        email_field = driver.find_element(By.NAME, "email")
        slow_type(email_field, email)
        
        print("Typing location...")
        location_field = driver.find_element(By.NAME, "location")
        slow_type(location_field, location)
        
        print("Typing zipcode...")
        zipcode_field = driver.find_element(By.NAME, "zipcode")
        slow_type(zipcode_field, zipcode)
        
        print("Typing description...")
        description_field = driver.find_element(By.NAME, "description")
        slow_type(description_field, description)
        
        # Find submit button
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
        
        # Scroll to submit button using JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        
        # Wait a moment after scrolling
        time.sleep(1)
        
        # Try multiple methods to click the submit button
        try:
            # Method 1: ActionChains click
            ActionChains(driver).move_to_element(submit_button).click().perform()
        except Exception:
            try:
                # Method 2: JavaScript click
                driver.execute_script("arguments[0].click();", submit_button)
            except Exception:
                # Method 3: Direct Selenium click
                submit_button.click()
        
        # Wait for submission to complete
        time.sleep(2)
        
        return True
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    
    finally:
        # Close the browser
        driver.quit()

# Main infinite loop
def main():
    # Replace with your form's URL
    form_url = "https://enddei.ed.gov"
    
    # Your text strings for each field

    email_string = ["QueerRightsAreHumanRights@fagmail.net", "IloveHRTandBottomSurgery@uwumail.kys", "TheGaysAreComingUwU@gmail.com", "DADDYSTOPTHRUSTINGITHURTS@PLEASE.com", "GawkOnMyGock@tgirls.com"]
    location_string = ["YourMother'sHouse", "Pornhub.com", "Jizzrag County", "ProstitutesRus", "Elon sucking donald's left toe", "ILIKEYOURPP"]
    description_string = [" Can a girldick be trained to read braille? Just wondering, for SCIENCE!!!", "death to all trannies!!! disgusting misogynistic freaks ....wait why is abortion and bodily autonomy rights getting rolled back?!?!", "after putting all the trannies in concentration camps us real women will be in power!! ...wait why am i getting put into the same concentration camps too????", " I’m so happy that those “evil satan worshipping cannibalistic” trannys are all dead. 😈☺️🎀 What’s that? You’re going to force me to get pregnant, take off my shoes, go to the kitchen, and make you a sammich??? 😱 what? How? 🫠 ", "I hate trans people but they are allowed to live and I don't think we should kill them. I'm an ally."]


    counter = 1
    
    # Run with a limit to prevent infinite loop
    while True:  # Adjust number of attempts as needed
        print(f"\nSubmission attempt #{counter}")
        success = submit_form(form_url, changer(random.choice(email_string)), changer(random.choice(location_string)), str(random.randint(10000, 99999)), changer(random.choice(description_string)))
        
        if success:
            print(f"Submission #{counter} successful")
        else:
            print(f"Submission #{counter} failed")
        
        counter += 1
        
        # Small delay between submissions (can be adjusted)
        time.sleep(3)

if __name__ == "__main__":
    main()
