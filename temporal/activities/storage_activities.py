import time
from temporalio import activity
from temporal.services.browser_manager import browser_manager
from RPA.Excel.Files import Files
from datetime import datetime
@activity.defn
async def save_to_excel(article_and_search_term):

    print('*' * 80)
    print(f"PARAMS[0]: \n {article_and_search_term[0]}")
    print('*' * 80)

    print(f"PARAMS[0]: \n {article_and_search_term[1]}")
    print('*' * 80)






    excel_file = Files()
    articles_info=article_and_search_term[0]
    search_term=article_and_search_term[1]

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

