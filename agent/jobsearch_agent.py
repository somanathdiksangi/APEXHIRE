from autogen_agentchat.agents import AssistantAgent
from agent.prompt.prompt import prompt

def get_job_search_agent(model_clind,tool):

    job_search_agent=AssistantAgent(
        name="job_search_agent",
        model_client=model_clind,
        description="you are a job search agent find the job",
        system_message=prompt,
        tools=[tool]
    )
    return job_search_agent