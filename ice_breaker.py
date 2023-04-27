from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from third_parties.linkedin import scrape_linkedin_profile
from dotenv import load_dotenv
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as tweeter_lookup_agent
import os
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, AutoModelForSeq2SeqLM
from third_parties.twitter import scrape_user_tweets
from output_parsers import person_intel_parser,PersonIntel

load_dotenv()


def ice_breack(name: str) -> PersonIntel:
    summary_template = """
    given the linkedin information {linkedin_information} and twitter information {twitter_information} about a person i want you to create :
    1. a short summary
    2. two interesting facts
    3. A topic that may interest them
    4. 2 creative ice breakers to open a conversation with them
    \n{format_instructions}
    """
    openai_key = os.getenv("OPENAI_API_KEY")

    linkedin_profile_url = linkedin_lookup_agent(username=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_profile_url)

    tweeter_user_name = tweeter_lookup_agent(username=name)
    tweets = scrape_user_tweets(username=tweeter_user_name, num_tweets=5)

    # # model_id = "google/flan-t5-base"
    # # tokenizer = AutoTokenizer.from_pretrained(model_id)
    # # model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    # # pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=1000)
    # # local_llm = HuggingFacePipeline(pipeline=pipe)

    summary_prompt_template = PromptTemplate(input_variables=[
                                             "linkedin_information", "twitter_information"], template=summary_template,
                                             partial_variables={"format_instructions": person_intel_parser.get_format_instructions()})
    # pass local llm instead of openAI
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo",
                     client="Any", openai_api_key=openai_key)
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    result = chain.run(linkedin_information=linkedin_data,
                       twitter_information=tweets)
    return person_intel_parser.parse(result)


if __name__ == "__main__":
    print("Hello Langchain")
    name = "avinash kadkol amex"
    result = ice_breack(name=name)
    print(result)
