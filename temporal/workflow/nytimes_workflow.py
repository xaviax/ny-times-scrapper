from datetime import timedelta
from temporalio import workflow



with workflow.unsafe.imports_passed_through():

    from temporal.activities.browser_activities import open_and_search
    from temporal.activities.browser_activities import select_past_month
    from temporal.services.models import ScrapeRequest
    from temporal.activities.parse_activities import scrape_articles
    from temporal.activities.storage_activities import save_to_excel


@workflow.defn
class NYTimesWorkflow:
    @workflow.run
    async def run(self,req: ScrapeRequest):

        # calling the activity to open browser and search
        res_browser= await workflow.execute_activity("open_and_search", req, start_to_close_timeout=timedelta(seconds=120))

        res_browser_two = await workflow.execute_activity(
            "select_past_month",
            res_browser['session_id'],
            start_to_close_timeout=timedelta(seconds=60),
        )




        article_data_and_search_term = await workflow.execute_activity(
            "scrape_articles",
            (req,res_browser_two['session_id']),
            start_to_close_timeout=timedelta(seconds=60)
        )


        res_browser_four = await workflow.execute_activity(
            "save_to_excel",
            article_data_and_search_term,
            start_to_close_timeout=timedelta(seconds=60),
        )


        print("Workflow completed")
        return [res_browser,res_browser_two,article_data_and_search_term]



