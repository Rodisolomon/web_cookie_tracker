import json
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

#https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path
#https://medium.com/dropout-analytics/selenium-and-geckodriver-on-mac-b411dbfe61bc




#duplicate code from file 3
def my_obj_pairs_hook(lst): #delete duplicate pair
    result={}
    count={}
    for key,val in lst:
        if key in count:count[key]=1+count[key]
        else:count[key]=1
        if key in result:
            if count[key] > 2:
                result[key].append(val)
            else:
                result[key]=[result[key], val]
        else:
            result[key]=val
    return result

def keys_exists(element, *keys): #helper determin if a key exist in a nested dic
    '''
    Check if *keys (nested) exists in `element` (dict).
    '''
    if not isinstance(element, dict):
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            if type(_element) is list:
                _element = _element[0]
            _element = _element[key]

        except KeyError:
            return False
    return True

def retransmission_helper(data): #if retransmission
    try:
        transmission = data["_source"]["layers"]["tcp"]["tcp.analysis"]["_ws.expert"]["tcp.analysis.retransmission"]
        return True
    except:
        return False  


import pyshark

# url grabber
import requests
from bs4 import BeautifulSoup
def url_grabber(origin):
    reqs = requests.get(origin)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    links = soup.find_all('a')
    for link in links:
        urls.append("https://computersecurityclass.com/" + str(link.get("href")))
    return urls


def Sum(file_name): #get data sum
    f = open(file_name)
    data = json.load(f)
    ret = 0
    for i in range(len(data)):
        try:
            ret += int(int(data[i]["_source"]["layers"]["tcp"]["tcp.seq"]))
        except:
            continue
    return ret


def sequence_web_run(origin_web): #run sequence of possible websites together
    urls = url_grabber(origin_web)
    for i in range(len(urls)):
        RUN(urls[i])

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
def RUN(url): #run one web
    """
    simple overview:
        1) set up webdriver
        2) load this article 
        3) close up shop 
    
    input:
        >> site_000
            > default: url of this article ('friend link')
    """
    #profile setting
    options= Options()
    profile = FirefoxProfile()
    profile.set_preference('browser.cache.disk.enable', False)
    profile.set_preference('browser.cache.memory.enable', False)
    profile.set_preference('browser.cache.offline.enable', False)
    profile.set_preference('network.cookie.cookieBehavior', 2)
    options.profile = profile
    # set the driver 
    # open geckodriver with that profile and get our class webpage

    browser = webdriver.Firefox(firefox_profile=profile)
    browser.get(url)

    # print out the page title, stored in the browser object:
    print("Downloaded the page entitled: " + browser.title)
    # and chill a bit
    sleep(10)
    # k, cool. let's bounce. 
    browser.close()
    browser.quit()

##I tried pyshark below to automate the whole process, but weird third IP address coming in so I give up this method
# import threading
# from threading import Thread
# class CustomThread(Thread):
#     # constructor
#     def __init__(self):
#         # execute the base constructor
#         Thread.__init__(self)
#         # set a default value
#         self.value = 0
 
#     # function executed in a new thread
#     def run(self):
#         import inspect
#         from pprint import pprint
#         import pyshark
#         fin_sum = 0
#         capture = pyshark.LiveRingCapture(interface='Wi-Fi')
#         for p in capture.sniff_continuously():
#             try:
#                 #p.tcp.pretty_print()
#                 #pprint(inspect.getmembers(p.tcp))
#                 if p.ip.src.get_default_value() == "128.135.11.239":
#                     print(p.tcp.flags.get_default_value())
#                 if p.tcp.flags.get_default_value() == "0x0011":
#                     print(p.ip.src.get_default_value())
#                 if p.ip.src.get_default_value() == "128.135.11.239" and (p.tcp.flags.get_default_value() == "0x0011"):
#                     pprint(inspect.getmembers(p.tcp))
#                     fin_sum +=  p.seq.int_value()
#             except:
#                 continue
#         self.value = fin_sum
# def pyshark_retransmission(p):
#     try:
#         a = p.tcp.analysis.retransmission
#         return True
#     except:
#         return False
# def dup_run(url):
#     import threading
#     global fin_sum
#     t1 = CustomThread()
#     t2 = threading.Thread(target=RUN, args = (url,)) 
#     t1.start()
#     t2.start()
#     t2.join()
#     t1.join()
#    return t1.value
    
def compare(num, candidate_dir, origin_web_file, origin_web): #Compare the generated page data size w/ the real one
    real_sum = Sum(origin_web_file)
    best_sum = 0
    min_dif = 3000000000
    urls = url_grabber(origin_web)
    real_i = 0
    for i in range(len(urls)):
        new_sum = Sum(candidate_dir + "/" + str(i+1)  + "_original.json")
        print(urls[i], new_sum)
        new_dif = abs(real_sum-new_sum)
        if new_dif <= min_dif:
            min_dif = new_dif
            best_sum =new_sum
            real_i = i
    print(f"for the automated webpage with size {real_sum}, the smallest difference comes from {real_i} : {urls[real_i]}, it is {best_sum}, got difference of {min_dif}")


# make runable 
if __name__ == '__main__':
#     # here we go
#     # gecko_test()
    ori_web = "https://computersecurityclass.com/8395429323325153639.html" #change manually
    # print(us)
    if 0:
        sequence_web_run(ori_web)
    else:
        candidate_dir = os.getcwd() + "/z" #change manually
        original_file = "20_original.json"
        compare(1, candidate_dir, original_file, ori_web)

#file list
# https://computersecurityclass.com/4645316182537493008.html
# https://computersecurityclass.com/2162649773462906129.html
# https://computersecurityclass.com/6515902067571552800.html
# https://computersecurityclass.com/3096362450007523403.html
# https://computersecurityclass.com/3543720717051768568.html
# https://computersecurityclass.com/4189735878785930371.html
# https://computersecurityclass.com/6951795341611099194.html
# https://computersecurityclass.com/4440420375552489898.html
# https://computersecurityclass.com/2220063448542616868.html
# https://computersecurityclass.com/4565717355070537488.html
# https://computersecurityclass.com/4828173522191520884.html
# https://computersecurityclass.com/8164980897159074435.html
# https://computersecurityclass.com/2841443097000131484.html
# https://computersecurityclass.com/2303956506707312172.html
# https://computersecurityclass.com/6650032294248895108.html
# https://computersecurityclass.com/5407145271694899850.html
# https://computersecurityclass.com/6278855606986685082.html
# https://computersecurityclass.com/2709630292946030487.html
# https://computersecurityclass.com/8395429323325153639.html
# https://computersecurityclass.com/3746638760973021784.html