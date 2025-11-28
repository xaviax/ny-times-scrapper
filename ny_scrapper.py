import time

from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from datetime import datetime
from robocorp.tasks import task


class NewYorkTimesScrapper:
    def __init__(self, search_term,pages):
        self.search_term = search_term
        self.browser = Selenium()
        self.pages=pages


    def initiate_browser_and_search(self):
        self.browser.open_browser("https://www.nytimes.com/", 'chrome')
        self.browser.wait_and_click_button('xpath://button[@data-testid="search-button"]')
        print('Performing Search.....')


        self.browser.wait_until_element_is_visible('xpath://input[@name="query"]', timeout=10)
        self.browser.input_text('xpath://input[@name="query"]', self.search_term)
        self.browser.click_button('xpath://button[@data-testid="search-submit"]')
        print('Query Searched: ', self.search_term)




    def select_past_month(self):
        self.browser.wait_and_click_button('xpath://button[@data-testid="search-date-dropdown-a"]')
        print('Selecting Date Range....')

        self.browser.wait_and_click_button('xpath://button[@value="Past Month"]')
        print('Date Range Selected....')

    @task
    def perform_scrapping(self):
        time.sleep(5)
        total_pages=5 if self.pages=='all' else self.pages
        print("Total Pages to Scrap: ", total_pages)

        for i in range(total_pages):
            self.browser.wait_and_click_button('xpath://button[@data-testid="search-show-more-button"]')
            print("Show button Clicked: ", i+1)

        time.sleep(5)

        article_lists = self.browser.find_elements('xpath://li[@data-testid="search-bodega-result"]')
        print(f'Length of elements: {len(article_lists)}')

        articles_info = []

        for article in article_lists:
            article_dict = {}
            date = self.browser.find_element('xpath:.//span[@data-testid="todays-date"]', parent=article).text
            print("Date: ", date)
            article_dict['date'] = date

            title = self.browser.find_element('xpath:.//h4', parent=article).text
            print("Title: ", title)
            article_dict['title'] = title

            article_description = self.browser.find_element('xpath:.//p[@class="css-16nhkrn"]', parent=article).text
            print("Description: ", article_description)
            article_dict['description'] = article_description

            print('Do images load now!?')

            # not all articles have images so....
            try:
                img_element = self.browser.find_element('xpath:.//figure//img', parent=article)
                srcset = self.browser.get_element_attribute(img_element, 'srcset')
                if srcset:
                    high_quality_image = srcset.split(',')[-1].split()[0]
                    print('Image: ', high_quality_image)
                    article_dict['image'] = high_quality_image

                else:
                    src = self.browser.get_element_attribute(img_element, 'src')
                    article_dict['image'] = src
                    print('Image: ', src)

            except Exception as e:
                print("Article Does not have image!")
                article_dict['image'] = 'No image'

            print('-' * 80)
            articles_info.append(article_dict)

        print(articles_info)

        #save_to_excel(articles_info, self.search_term)

        print("Scraping Complete.....")

        return [articles_info,self.search_term]


    def save_to_excel(self, articles_info, search_term):
        excel_file = Files()

        excel_file.create_workbook()
        headers = ['Date', 'Title', 'Description', 'Image-URL']

        article_rows = []

        for article in articles_info:
            row = [
                article.get('date', ''),
                article.get('title', ''),
                article.get('description', ''),
                article.get('image', '')
            ]

            article_rows.append(row)

        print('-' * 80)
        print(article_rows)

        for column_index, header in enumerate(headers, start=1):
            excel_file.set_cell_value(1, column_index, header)

        for row_index, row_data in enumerate(article_rows, start=2):
            for column_index, value in enumerate(row_data, start=1):
                excel_file.set_cell_value(row_index, column_index, value)

        filename = f"nytimes_{search_term.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        excel_file.save_workbook(filename)
        excel_file.close_workbook()

        print('Written to Excel file...')









def main():
    scrapper = NewYorkTimesScrapper('amd',0)
    scrapper.initiate_browser_and_search()
    scrapper.select_past_month()
    data=scrapper.perform_scrapping()
    scrapper.save_to_excel(data[0],data[1])

    time.sleep(3)



if __name__ == "__main__":
    main()