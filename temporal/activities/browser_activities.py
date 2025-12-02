import time
from temporalio import activity
from temporal.services.browser_manager import browser_manager

@activity.defn 
async def open_and_search(req):

    """
    here open browser, search, and also return session id to identify browser instance
    :param req:
    :return:
    """

    print("printing the entire Req", req)
    print("Search term in activity: ", req['search_term'])
    print("Pages in activity: ", req['pages'])

    # Create unique session id for workflow
    # will be using workflow id and run id for uniqueness

    info=activity.info()
    print(f"Browser session: {info.workflow_id}_{info.workflow_run_id}")
    session_id = f"{info.workflow_id}_{info.workflow_run_id}"


    #Now we will create a browser instance with the generated session

    browser=browser_manager.create_session(session_id)




    #browser = Selenium()
    #browser.open_browser("https://www.nytimes.com/", 'chrome')
    time.sleep(5)
    browser.wait_and_click_button('xpath://button[@data-testid="search-button"]')
    print('Performing Search.....')

    browser.wait_until_element_is_visible('xpath://input[@name="query"]', timeout=10)
    browser.input_text('xpath://input[@name="query"]', req['search_term'])
    browser.click_button('xpath://button[@data-testid="search-submit"]')
    print('Query Searched: ', req['search_term'])
    time.sleep(2)

    return {"status":"searched", "term": req['search_term'], "session_id": session_id}



@activity.defn 
async def select_past_month(session_id:str):

    browser=browser_manager.get_session(session_id)

    if not browser:
        raise RuntimeError(f"Browser session not found: {session_id}")



    browser.wait_and_click_button('xpath://button[@data-testid="search-date-dropdown-a"]')
    print('Selecting Date Range....')

    browser.wait_and_click_button('xpath://button[@value="Past Month"]')
    print('Date Range Selected....')


    return {"status":"date_selected", "session_id": session_id}
    
