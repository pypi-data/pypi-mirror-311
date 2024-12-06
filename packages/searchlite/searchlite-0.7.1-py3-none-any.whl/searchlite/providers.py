from .searcher import RealTimeGoogleSearchProvider

import sys

def check_os_sys():
    if sys.platform.startswith('win'):
        return "Windows"
    elif sys.platform.startswith('linux'):
        return "Linux"
    else:
        return "Other OS"

def google(query,max_urls=5,animation=False,
           chromedriver_path=None):
    if chromedriver_path is None:
        cur_sys = check_os_sys()
        chromedriver_path = "/usr/local/bin/chromedriver" if cur_sys == 'Linux' else r"C:\Users\chromedriver-win64\chromedriver.exe"

    search = RealTimeGoogleSearchProvider(animation=animation,
                                          chromedriver_path=chromedriver_path)
    return search.search(query,max_urls=max_urls)

def bing(query,max_urls=5,animation=False,
         chromedriver_path=None):
    if chromedriver_path is None:
        cur_sys = check_os_sys()
        chromedriver_path = "/usr/local/bin/chromedriver" if cur_sys=='Linux' else r"C:\Users\chromedriver-win64\chromedriver.exe"
    search = RealTimeGoogleSearchProvider(search_provider="bing",
                                          animation=animation,
                                          chromedriver_path=chromedriver_path)
    return search.search(query, max_urls=max_urls)