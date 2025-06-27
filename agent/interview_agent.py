from autogen_agentchat.agents import AssistantAgent
from agent.prompt.prompt2 import prompt2


def get_jobinterview_agent(model_clind):

    jobinterview_agent=AssistantAgent(
        name="job_interview_agent",
        model_client=model_clind,
        system_message=prompt2

    )