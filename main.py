from faker import Faker
from faker import Factory

from faker.providers import profile
from faker_education import SchoolProvider
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random
import os
from os import path
import tempfile

fake = Factory.create()
fake.add_provider(SchoolProvider)
fake.add_provider(profile)

def slow_type(element, text):
    """
    Type text slowly with a small delay between characters
    Adds realism and visibility to typing process
    """
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.09, 0.19))


def fake_image(image_path):
    size = random.randint(6000000, 9000000)
    with open(image_path,'wb') as f:
        f.write(random.randbytes(size))


def submit_form(url, email, location, zipcode, description):
    # Setup Firefox
    options = Options()
    options.add_argument("-profile")
    # Type about:profiles into firefox to get profile string 
    options.add_argument("<insert profile string (the one without .cache)>")
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
        description_field.send_keys(description)

        print("Adding fake image...")
        photo_id = random.randint(1000,9999)
        dir = tempfile.gettempdir()
        image_path = os.path.join(dir, f"IMG_{photo_id}.jpg")
        fake_image(image_path)
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(image_path)
        
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
        wait =  WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "page-confirmation")))
        os.unlink(image_path)
        
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
    counter = 1
    
    # Run with a limit to prevent infinite loop
    while True:  # Adjust number of attempts as needed
        email_string = fake.simple_profile().get('mail').replace('hotmail',random.choice(['hotmail','gmail','yahoo']))
        location_string = fake.school_object().get('school')
        zip_string = fake.postcode()
        description_string = fake.paragraph(nb_sentences=5)
        
        print(f"\nSubmission attempt #{counter}")
        success = submit_form(form_url, email_string, location_string, zip_string, description_string)
        
        if success:
            print(f"Submission #{counter} successful")
        else:
            print(f"Submission #{counter} failed")
        
        counter += 1
        
        # Small delay between submissions (can be adjusted)
        time.sleep(3)

if __name__ == "__main__":
    main()
