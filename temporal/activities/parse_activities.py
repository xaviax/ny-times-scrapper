import time
from temporalio import activity


from temporal.services.browser_manager import browser_manager

@activity.defn
async def scrape_articles(params):


    print(f'params inside the scrape_articles function:{params}')
    
    session_id = params[1]
    pages=params[0]['pages']
    search_term=params[0]['search_term']

    browser=browser_manager.get_session(session_id)

    if not browser:
        raise RuntimeError(f"Session id {session_id} not found (Scrape-Activity)!")

    time.sleep(5)
    #pages = 5 if pages == 'all' else pages
    print("Total Pages to Scrap: ", pages)

    for i in range(pages):
        browser.wait_and_click_button('xpath://button[@data-testid="search-show-more-button"]')
        print("Show button Clicked: ", i + 1)

    time.sleep(5)

    article_lists = browser.find_elements('xpath://li[@data-testid="search-bodega-result"]')
    print(f'Length of elements: {len(article_lists)}')

    articles_info = []

    for article in article_lists:
        article_dict = {}
        date = browser.find_element('xpath:.//span[@data-testid="todays-date"]', parent=article).text
        print("Date: ", date)
        article_dict['date'] = date

        title = browser.find_element('xpath:.//h4', parent=article).text
        print("Title: ", title)
        article_dict['title'] = title

        article_description = browser.find_element('xpath:.//p[@class="css-16nhkrn"]', parent=article).text
        print("Description: ", article_description)
        article_dict['description'] = article_description

        print('Do images load now!?')

        # not all articles have images so....
        try:
            img_element = browser.find_element('xpath:.//figure//img', parent=article)
            srcset = browser.get_element_attribute(img_element, 'srcset')
            if srcset:
                high_quality_image = srcset.split(',')[-1].split()[0]
                print('Image: ', high_quality_image)
                article_dict['image'] = high_quality_image

            else:
                src = browser.get_element_attribute(img_element, 'src')
                article_dict['image'] = src
                print('Image: ', src)

        except Exception as e:
            print("Article Does not have image!")
            article_dict['image'] = 'No image'

        print('-' * 80)
        articles_info.append(article_dict)

    print(articles_info)

    # save_to_excel(articles_info, search_term)

    print("Scraping Complete.....")

    print('ONLY PRINTING ARTICLES')
    print('-' * 80)
    print(articles_info)
    print('-' * 80)

    print("Closing browser before saving to excel...")
    browser.close_browser()

    return [articles_info,search_term]