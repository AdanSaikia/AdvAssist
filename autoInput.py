import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


def getWebsite(url: str, incognito=True, shadow=False) -> webdriver.Chrome:
    chrome_options = Options()

    # Optimization settings for speed
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--disable-popup-blocking")  # Disable popup blocking
    chrome_options.add_argument("--disable-notifications")  # Disable browser notifications
    if shadow:
        chrome_options.add_argument("--headless")  # Optional: Run headless for testing
    if incognito:
        chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-dev-shm-usage")  # Optimize shared memory
    chrome_options.add_argument("--no-sandbox")  # Bypass OS-level sandboxing
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless
    chrome_options.add_argument("--enable-automation")  # Indicate automated testing
    chrome_options.add_argument("--start-maximized")  # Maximize for speed and fewer errors
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.page_load_strategy = 'eager'  # Load only essential resources

    # Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(5)  # Use shorter implicit wait for speed
    return driver


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Global count variable
current_input_index = 0


def sendKeys(driver: WebDriver, value: str, log=True):
    """
    Finds the next input box or text area on the page based on a global count,
    enters the given value, and presses Enter.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        value (str): The value to input into the text field.
    """
    global current_input_index

    try:
        # Get all input boxes and text areas
        input_elements = driver.find_elements(By.CSS_SELECTOR, "input, textarea")

        # Ensure the current index is within bounds
        if current_input_index < len(input_elements):
            # Target the current input box
            input_element = input_elements[current_input_index]
            # Clear the field, enter the value, and press Enter
            input_element.clear()
            input_element.send_keys(value)
            time.sleep(1)
            input_element.send_keys(Keys.RETURN)
            if log:
                print(f"Entered '{value}' into input box #{current_input_index + 1} and pressed Enter.")

            # Increment the global counter
            current_input_index += 1
        else:
            if log:
                print("Error: No more input boxes available on the page.")
    except Exception as e:
        print(f"Error: Unable to send keys. Details: {e}")


def finish(log=True):
    """
    Resets the global counter to start targeting the first input box again.
    """
    global current_input_index
    current_input_index = 0
    if log:
        print("Input box counter has been reset.")


if __name__ == "__main__":
    # Usage example
    url = "https://myntra.com"  # Replace with your URL
    driver = getWebsite(url)

    # Enter values into multiple input fields
    sendKeys(driver, "kurtas for men under 1000")

    # Reset the counter
    finish()


    # Clean up
    input()
    driver.quit()


