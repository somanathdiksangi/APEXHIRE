from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination

def get_team(jobsearch_agent,interview_agent):
    condition=TextMentionTermination("STOP")
    team=RoundRobinGroupChat(
        participants=[jobsearch_agent,interview_agent],
        max_turns=15,
        termination_condition=condition
    )
    return team