import threading
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from AdvAssist.autoInput import getWebsite, sendKeys, finish
import time

stop_chat = threading.Event()  # Global event to signal the stopping of the chat loop
driver = None

def login(username: str, password: str, hidden=True):
    global driver
    url = "https://instagram.com"
    if hidden:
        driver = getWebsite(url, shadow=True)
    else:
        driver = getWebsite(url, shadow=False)

    print(f"Reached {url}")

    sendKeys(driver, username, log=False)  # Enter username
    sendKeys(driver, password, log=False)  # Enter password
    print("Successfully logged in")

    finish(log=False)  # Reset input state if needed
    time.sleep(3)

    try:
        not_now_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Not now')]")
        not_now_button.click()
        print("Clicked 'Not Now' button")
    except Exception as e:
        print("No 'Not Now' button found or already handled:", e)

def enterChat(targetUsername: str):
    global driver
    if driver is None:
        print("Please log in first.")
        return

    try:
        driver.get("https://www.instagram.com/direct/inbox/")
        print("Reached Direct Inbox")
    except Exception as e:
        print(f"Error with 'Messages' button: {e}")
        return

    time.sleep(2)

    try:
        sendMsgBtn = driver.find_element(By.XPATH, "//div[contains(text(), 'Send message')]")
        sendMsgBtn.click()
        sendKeys(driver, targetUsername)
        time.sleep(0.5)
        targetBtn = driver.find_element(By.XPATH, f"//span[contains(text(), '{targetUsername}')]")
        targetBtn.click()
        chatBtn = driver.find_element(By.XPATH, f"//div[contains(text(), 'Chat')]")
        chatBtn.click()
        print(f"Entered chat: {targetUsername} successfully!")
    except Exception as e:
        print(f"Error entering chat: {e}")

def sendMessage(message_text: str, log=True):
    try:
        time.sleep(2)
        msgBox = driver.find_element(By.CSS_SELECTOR, "p.xat24cr.xdj266r")
        msgBox.send_keys(message_text)
        msgBox.send_keys(Keys.ENTER)
        if log:
            print(f"Message sent: {message_text}")
    except Exception as e:
        print(f"Error sending message: {e}")

def receiveMessages(customNickname: str):
    global driver
    last_message = None
    while not stop_chat.is_set():
        try:
            messages = driver.find_elements(By.CSS_SELECTOR, "div.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1gslohp.x11i5rnm.x12nagc.x1mh8g0r.x1yc453h.x126k92a.x18lvrbx")
            if messages:
                last_msg = messages[-1].text
                if last_msg != last_message:
                    last_message = last_msg
                    print(f"{customNickname}: {last_message}")
        except Exception as e:
            print(f"Error fetching messages: {e}")
        time.sleep(1)  # Polling interval

def chat(targetUsername: str, customNickname: str):
    global driver
    if driver is None:
        print("Please log in first.")
        return

    enterChat(targetUsername)

    # Thread for receiving messages
    receive_thread = threading.Thread(target=receiveMessages, args=(customNickname,), daemon=True)
    receive_thread.start()

    print("Chat started. Type your messages below. Type 'exit' to quit.")
    time.sleep(1)

    try:
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Exiting chat...")
                stop_chat.set()
                break
            if user_input == "":
                continue

            sendMessage(user_input, log=False)
    except KeyboardInterrupt:
        print("\nChat interrupted by user. Exiting...")
        stop_chat.set()

    receive_thread.join()  # Ensure the receiving thread ends cleanly

def logout():
    global driver
    if driver is None:
        print("Please log in first.")
        return
    else:
        driver.quit()

if __name__ == "__main__":
    login("mr.mortal0", "111822*", False)  # Log in first
    enterChat("vincent_charles076")

    input()
    driver.quit()
