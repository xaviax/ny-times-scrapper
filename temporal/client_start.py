import asyncio
import time
from temporalio.activity import client
from temporalio.client import Client
from temporal.workflow.nytimes_workflow import NYTimesWorkflow
from temporal.services.models import ScrapeRequest


async def main():
    client = await Client.connect("localhost:7233")
    #req = ScrapeRequest(search_term="amd", pages=0)
    handle = await client.start_workflow(
        NYTimesWorkflow.run,
        ScrapeRequest(search_term="amd", pages=2),
        id="nytimes-amd-" + str(int(time.time())),
        task_queue="nytimes-tasks"
    )



    print("workflow id: ", handle.id)
    print("Started workflow, run id: ", handle.run_id)


    result = await handle.result()
    print("workflow result: ", result)


if __name__ == "__main__":
    asyncio.run(main())