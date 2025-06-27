from config.model_clind import get_model_client
from agent.interview_agent import get_jobinterview_agent
from agent.jobsearch_agent import get_job_search_agent
from team.teams import get_team
from tool.search_job_tool import search_google_jobs_via_serper
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from autogen_core.tools import Tool
import asyncio
import asyncio



model_clind=get_model_client()
# job_title = "data scientist"  # This could be dynamic input from another agent
# tool = search_google_jobs_via_serper(keywords=job_title)
# or from autogen_agentchat.tools if you're using that version

# search_tool =register_function{
#     "name": "search_google_jobs_via_serper",
#     "description": "Searches for jobs using the Serper API based on provided keywords",
#     "func": search_google_jobs_via_serper
# }


async def main():
    job_search_agent= get_job_search_agent(model_clind, tools=[search_google_jobs_via_serper])

    jobinterview_agent=get_jobinterview_agent(model_clind)

    team=get_team(job_search_agent,jobinterview_agent)

    try:
        task = 'take resume from working directory for example resume.docx and search job'
        async for message in team.run_stream(task=task):
            print('='*40)
            if isinstance(message, TextMessage):
                msg = f"{message.source}: {message.content}"
                print(msg)
            elif isinstance(message, TaskResult):
                # Handle TaskResult differently - check available attributes
                msg = f"Task Result: {message}"
                if hasattr(message, 'summary'):
                    msg = f"Task Result Summary: {message.summary}"
                print(msg)
            print('='*40)

    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == '__main__':
    asyncio.run(main())