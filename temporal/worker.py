import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from temporal.workflow.nytimes_workflow import NYTimesWorkflow
from temporal.activities import browser_activities as browser_acts
from temporal.activities import parse_activities as parse_acts
from temporal.activities import storage_activities as storage_acts

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="nytimes-tasks",
        workflows=[NYTimesWorkflow],
        activities=[browser_acts.open_and_search,browser_acts.select_past_month,parse_acts.scrape_articles,storage_acts.save_to_excel]
    )

    print("Worker started")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())