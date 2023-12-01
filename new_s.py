#!/usr/bin/env python
 
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# create a profile that disables caching
profile = FirefoxProfile()
profile.set_preference('browser.cache.disk.enable', False)
profile.set_preference('browser.cache.memory.enable', False)
profile.set_preference('browser.cache.offline.enable', False)
profile.set_preference('network.cookie.cookieBehavior', 2)

# open geckodriver with that profile and get our class webpage
browser = webdriver.Firefox(firefox_profile=profile)
browser.get('https://classes.cs.uchicago.edu/archive/2023/winter/23200-1/')

# print out the page title, stored in the browser object:
print("Downloaded the page entitled: " + browser.title)

# close the page and quit the browser fully
browser.close()
browser.quit()