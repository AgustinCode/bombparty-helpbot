import time
import re
import os
import logging
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class JKLMBot:

    def __init__(self, room_code):
        self.room_code = room_code
        self.driver = None
        self.wordlist = []

        # Initialize wordlist from file
        self.load_wordlist()

        # Pre-compile the regular expression pattern for !helpbot command
        self.helpbot_pattern = re.compile(r'^!helpbot:([a-zA-Z]{2,3})$')


    ''' OLD INIT FUNCTION

    def __init__(self, room_code):
        self.room_code = room_code
        self.driver = None
        self.wordlist = []

        wordlist_file = "wordlist.txt"
        if os.path.exists(wordlist_file):
            with open(wordlist_file, "r") as file:
                self.wordlist = file.read().splitlines()
        else:
            logging.warning(f"Wordlist file '{wordlist_file}' not found.")
'''

#This function is new just to optimize the loading of the wordlist file
#It makes the process a bit easier to visualise and a bit more user-friendly
    def load_wordlist(self):
        wordlist_file = "wordlist.txt"
        if os.path.exists(wordlist_file):
            with open(wordlist_file, "r") as file:
                self.wordlist = file.read().splitlines()
        else:
            logging.warning(f"Wordlist file '{wordlist_file}' not found.")


    def setup_driver(self):
        service = Service(executable_path="chromedriver.exe")
        options = webdriver.ChromeOptions()
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        self.driver = webdriver.Chrome(service=service, options=options)
        link = f"https://jklm.fun/{self.room_code}"
        self.driver.get(link)
        print("Driver setup complete and navigated to the room.")

    def enter_room(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "styled.nickname"))
            )
            nickname_input = self.driver.find_element(By.CLASS_NAME, "styled.nickname")
            nickname_input.clear()
            nickname_input.send_keys("HelpBot by AgusCode", Keys.ENTER)
            print("Entered the room with nickname.")
            time.sleep(3)
        except Exception as e:
            print(f"ERROR entering room: {e}")

    def present(self):
        try:
            message = " ⛑️ Hey! I'm ready to help everyone in this room, command: !helpbot:(syllable) ⛑️ .\n Example: !helpbot:mis"
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-placeholder-text='typeHereToChat']"))
            )
            textarea = self.driver.find_element(By.CSS_SELECTOR, "textarea[data-placeholder-text='typeHereToChat']")
            textarea.send_keys(message, Keys.ENTER)
            print("Sent presentation message.")
            time.sleep(5)
        except Exception as e:
            print(f"ERROR presenting: {e}")

    
    def inject_mutation_observer(self):
        script = """
            var targetNode = document.querySelector('.log.darkScrollbar');
            if (!targetNode) {
                console.error("Target node not found. MutationObserver not injected.");
                return;
            }

            var config = { childList: true, subtree: true };

            var callback = function(mutationsList, observer) {
                mutationsList.forEach(function(mutation) {
                    if (mutation.type === 'childList') {
                        mutation.addedNodes.forEach(function(newNode) {
                            var textNode = newNode.querySelector('.text');
                            if (textNode) {
                                console.log('NEW_MESSAGE: ' + textNode.innerText);
                            }
                        });
                    }
                });
            };

            var observer = new MutationObserver(callback);
            observer.observe(targetNode, config);
            console.log("MutationObserver injected successfully.");
        """

    try:
        self.driver.execute_script(script)
        print("Injected MutationObserver script.")
    except Exception as e:
        print(f"Error injecting MutationObserver script: {e}")


    
    
    ''' OLD MUTATION INJECTION METHOD
    
    def inject_mutation_observer(self):
        script = """
            var targetNode = document.querySelector('.log.darkScrollbar');
            var config = { childList: true, subtree: true };

            var callback = function(mutationsList, observer) {
                for(var mutation of mutationsList) {
                    if (mutation.type === 'childList') {
                        var newNodes = mutation.addedNodes;
                        for (var i = 0; i < newNodes.length; i++) {
                            var newNode = newNodes[i];
                            // Check if the newNode has a class 'text'
                            var textNode = newNode.querySelector('.text');
                            if (textNode) {
                                console.log('NEW_MESSAGE: ' + textNode.innerText);
                            }
                        }
                    }
                }
            };

            var observer = new MutationObserver(callback);
            observer.observe(targetNode, config);
            console.log("MutationObserver injected successfully.");
        """
        self.driver.execute_script(script)
        print("Injected MutationObserver script.")
        '''



    def capture_messages(self):
        while True:
            logs = self.driver.get_log('browser')
            for log in logs:
                if 'NEW_MESSAGE:' in log['message']:
                    message = log['message'].split('NEW_MESSAGE:', 1)[1].strip()
                    message = message[:-1]
                    print("New message captured:", message)
                    self.process_message(message)
            time.sleep(1)  # Small pause to avoid an overly fast loop



    def process_message(self, message):
        if message == '!helpbot':
            self.send_message("Helpbot guide - Type '!helpbot:[syllable]' so I can help you find words!")

        match = self.helpbot_pattern.match(message.lower())
        if match:
            letters = match.group(1).lower()
            print("Let the magic happen...")
            self.help_user(letters)

    ''' [ORIGINAL PROCESS MESSAGE METHOD]
    def process_message(self, message):
        if message == '!helpbot':
            self.send_message("Helpbot guide - Type '!helpbot:[syllable]' so i can help you find words!")

        # Define a regex pattern to match '!helpbot:xx' or '!helpbot:xxx' where xx or xxx can be any letters
        pattern = r'^!helpbot:([a-zA-Z]{2,3})$'
        
        # Check if the message matches the pattern
        match = re.match(pattern, message.lower())
        if match:
            letters = match.group(1).lower()  # Extract the letters xx or xxx
            print("Ayudando...")
            self.help_user(letters)
    '''



    def help_user(self, letters, max_words=10):

        words_by_prefix = {}
        for word in self.wordlist:
            prefix = word[:len(letters)].lower()
            if prefix == letters:
                words_by_prefix.setdefault(word[0].lower(), []).append(word.capitalize())
            if len(words_by_prefix) >= max_words:
                break

        possible_words = [word for sublist in words_by_prefix.values() for word in sublist]
        if possible_words:
            word_list_message = "\n".join(possible_words[:max_words])  # Limit to max_words
            self.send_message(f"Don't worry! Here are some words that might help:\n{word_list_message}")
        else:
            self.send_message("Sorry, I couldn't find any words matching that criteria.")

    '''
    def help_user(self, letters):
        words_by_prefix = {}
        for word in self.wordlist:
            prefix = word[:len(letters)].lower()
            if prefix == letters:
                words_by_prefix.setdefault(word[0].lower(), []).append(word.capitalize())
            if len(words_by_prefix) >= 6:
                break

        possible_words = [word for sublist in words_by_prefix.values() for word in sublist]
        if possible_words:
            word_list_message = "\n".join(possible_words[:6])  # Limit to first 6 words
            self.send_message(f"Don't worry! Here are some words that might help:\n{word_list_message}")
        else:
            self.send_message("Sorry, I couldn't find any words matching that criteria.")
    '''



    def send_message(self, message):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-placeholder-text='typeHereToChat']"))
            )
            textarea = self.driver.find_element(By.CSS_SELECTOR, "textarea[data-placeholder-text='typeHereToChat']")
            textarea.send_keys(message, Keys.ENTER)
            print(f"Bot response sent: {message}")
        except Exception as e:
            print(f"ERROR sending message: {e}")

    def run(self):
        self.setup_driver()
        self.enter_room()
        self.present()
        self.inject_mutation_observer()
        self.capture_messages()

if __name__ == "__main__":
    bot = JKLMBot("your_room_code_here")
    bot.run()