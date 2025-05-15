import os
from dotenv import load_dotenv
from langchain_core.tools import Tool
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langchain_google_community import GoogleSearchAPIWrapper

load_dotenv()
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
os.environ['GOOGLE_CSE_ID'] = os.getenv('GOOGLE_CSE_ID')
os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')


@tool
def custom_disease_info_search_google(query: str) -> str:
    """This function will search about the symptom,
    cause, cure and prevention of the disease"""

    search = GoogleSearchAPIWrapper()

    search_tool = Tool(
        name="google_search",
        description="Search Google for recent results.",
        func=search.run,
    )
    custom_prompt = f"""
        Find reliable information about the symptoms, causes, 
        and treatments of the disease: {query}
    """
    return search_tool.run(custom_prompt)


@tool
def custom_disease_info_search_tavily(query: str) -> str:
    """This function will search reliable information
    about the disease"""

    search_tool = TavilySearch(
        max_results=5,
        topic="general",
        # include_answer=False,
        # include_raw_content=False,
        # include_images=False,
        # include_image_descriptions=False,
        # search_depth="basic",
        # time_range="day",
        # include_domains=None,
        # exclude_domains=None
    )
    custom_prompt = f"""
        Find reliable Interesting Fact about {query}
    """
    return search_tool.invoke({"query": custom_prompt})