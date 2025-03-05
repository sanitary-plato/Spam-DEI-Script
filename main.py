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

def changer(input_string, x):

    # Convert the string to a list for easier manipulation
    chars = list(input_string)
    
    # If the string is too short to change two letters, return the original string
    if len(chars) < 2:
        return input_string
    
    # Select two unique random indices
    indices = random.sample(range(len(chars)), x)
    
    # For each selected index, replace the letter with a random different letter
    for index in indices:
        # Get a random letter that is different from the current letter
        current_letter = chars[index]
        if current_letter != '@':
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

def rand_zip_code():
    """
    Returns a randomly selected US school district zip code.
    
    Returns:
        str: A randomly chosen school district zip code.
    """
    school_district_zips = [
        # Major City School Districts
        '10001', '60601', '90210', '02108', '33101', '75201', '98101', 
        '02215', '85001', '94102', '77001', '30301', '20001', '80202', 
        '15201', '55401', '46201', '94105', '01601', '84101', '02116', 
        '50301',

        # California School Districts
        '90001', '90002', '90003', '90007', '90008', '90011', '90037', 
        '90044', '90059', '90061', '90220', '90240', '90241', '90242', 
        '90280', '90504', '90505', '90506', '90712', '90713', '90714',

        # New York School Districts
        '10002', '10003', '10004', '10005', '10006', '10007', 
        '10010', '10011', '10012', '10013', '10014', '10016', '10017', 
        '10018', '10019', '10020', '10022', '10023', '10024', '10025',

        # Texas School Districts
        '75001', '75006', '75007', '75010', '75019', '75022', '75023', 
        '75024', '75025', '75028', '75030', '75038', '75039', '75040', 
        '75041', '75042', '75043', '75044', '75048', '75078', '75080',

        # Florida School Districts
        '32801', '32803', '32804', '32806', '32807', '32808', '32809', 
        '32810', '32811', '32812', '32822', '32824', '32825', '32826', 
        '32827', '32828', '32829', '32830', '32835', '32837', '32839',

        # Illinois School Districts
        '60602', '60603', '60604', '60605', '60606', '60607', 
        '60608', '60609', '60610', '60611', '60612', '60613', '60614', 
        '60615', '60616', '60617', '60619', '60620', '60621', '60622',

        # Pennsylvania School Districts
        '15202', '15203', '15204', '15205', '15206', '15207', 
        '15208', '15210', '15211', '15212', '15213', '15214', '15215', 
        '15216', '15217', '15218', '15219', '15220', '15221', '15222',

        # Ohio School Districts
        '44101', '44102', '44103', '44104', '44105', '44106', '44107', 
        '44108', '44109', '44110', '44111', '44112', '44113', '44114', 
        '44115', '44116', '44117', '44118', '44119', '44120', '44121',

        # Georgia School Districts
        '30303', '30305', '30306', '30307', '30308', '30309', 
        '30310', '30311', '30312', '30313', '30314', '30315', '30316', 
        '30317', '30318', '30319', '30320', '30321', '30322',

        # Washington School Districts
        '98102', '98103', '98104', '98105', '98106', '98107', 
        '98108', '98109', '98112', '98115', '98116', '98117', '98118', 
        '98119', '98122', '98125', '98126', '98133', '98134', '98136'
    ]
    
    return random.choice(school_district_zips)

# Main infinite loop
def main():
    # Replace with your form's URL
    form_url = "https://enddei.ed.gov"
    
    # Your text strings for each field

    email_string = ["QueerRightsAreHumanRights@fagmail.net", "IsItGayToSuckCockAsLongAsYouHateIt@trustmeimstraight.com", "WhyDoesTrumpLookLikeDoritoDustCoveredNakedMoleRat@mail.com","IloveHRTandBottomSurgery@uwumail.kys", "TheGaysAreComingUwU@gmail.com", "DADDYSTOPTHRUSTINGITHURTS@PLEASE.com", "GawkOnMyGock@tgirls.com"]
    location_string = ["YourMother'sHouse", "Pornhub.com", "SayGex right now. Say it.", "I Love Taking 6 inch dog dildos", "Jizzrag County", "ProstitutesRus", "Elon sucking donald's left toe", "ILIKEYOURPP"]
    description_string = [" Can a girldick be trained to read braille? Just wondering, for SCIENCE!!!", "death to all trannies!!! disgusting misogynistic freaks ....wait why is abortion and bodily autonomy rights getting rolled back?!?!", "after putting all the trannies in concentration camps us real women will be in power!! ...wait why am i getting put into the same concentration camps too????", " I’m so happy that those “evil satan worshipping cannibalistic” trannys are all dead. 😈☺️🎀 What’s that? You’re going to force me to get pregnant, take off my shoes, go to the kitchen, and make you a sammich??? 😱 what? How? 🫠 ", "I hate trans people but they are allowed to live and I don't think we should kill them. I'm an ally."]


    counter = 1
    
    # Run with a limit to prevent infinite loop
    while True:  # Adjust number of attempts as needed
        print(f"\nSubmission attempt #{counter}")
        success = submit_form(form_url, changer(random.choice(email_string), 1), changer(random.choice(location_string), 2), str(rand_zip_code()), changer(random.choice(description_string), 4))
        
        if success:
            print(f"Submission #{counter} successful")
        else:
            print(f"Submission #{counter} failed")
        
        counter += 1
        
        # Small delay between submissions (can be adjusted)
        time.sleep(3)

if __name__ == "__main__":
    main()
