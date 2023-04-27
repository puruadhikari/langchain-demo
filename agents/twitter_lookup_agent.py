from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from tools.tools import get_profile_url


def lookup(username: str) -> str:

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")  # type: ignore

    template = """Given the full name {name_of_person} I want you to find a link their twitter profile page, and extract from it their twitter username.
    In your final answer should contain person's username"""

    tools_for_agent = [
        Tool(
            name="Crawl Google for Twitter profile page",
            func=get_profile_url,
            description="usful for when you need to get the Twitter page URL",
        )
    ]
    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    twitter_username = agent.run(
        prompt_template.format_prompt(name_of_person=username))

    return twitter_username
