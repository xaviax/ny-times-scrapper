from RPA.Browser.Selenium import Selenium
from typing import Optional
import threading

class BrowserManager:
    '''Thread-sage browser session manager'''

    def __init__(self):
        self._browsers={} #this is session_id for browser instance
        self._lock = threading.Lock()


    def create_session(self,session_id: str)->Selenium:
        '''Create a new browser session'''

        with self._lock:
            if session_id in self._browsers:
                # Reuse the existing session
                return self._browsers[session_id]

            browser=Selenium()
            browser.open_browser("https://www.nytimes.com/", 'chrome')
            self._browsers[session_id]=browser
            return browser


    def get_session(self,session_id: str) -> Optional[Selenium]:
        '''Get a browser session by id'''
        with self._lock:
            return self._browsers.get(session_id)

    def close_session(self,session_id: str):
        '''Close a browser session'''
        with self._lock:
            if session_id in self._browsers:
                try:
                    self._browsers[session_id].close_browser()

                except Exception as e:
                    print(f"Error closing browser session: {e}")

                finally:
                    del self._browsers[session_id]
                    print(f"Closed browser session: {session_id}")




    def cleanup_all(self):
        '''Close all browser sessions'''
        with self._lock:
            for session_id in list(self._browsers.keys()):
                self.close_session(session_id)







browser_manager = BrowserManager()