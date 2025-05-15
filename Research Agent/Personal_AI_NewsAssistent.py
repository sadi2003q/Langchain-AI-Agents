from langchain_tavily import TavilySearch
from langchain.tools import tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from langchain import hub
import requests
from dotenv import load_dotenv
import os

load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
os.environ['GOOGLE_CSE_ID'] = os.getenv('GOOGLE_CSE_ID')
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

google_search = GoogleSearchAPIWrapper()

google_search_tool = Tool(
    name="google_search",
    description="Search Google for recent results using Google's Programmable Search Engine.",
    func=google_search.run,
)


duckduckgo_search = DuckDuckGoSearchRun()

duckduckgo_search_tool = Tool(
    name="duckduckgo_search",
    description="Search the web using DuckDuckGo Search for general-purpose results.",
    func=duckduckgo_search.run,
)

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())


@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia and return a summary for a given query."""
    return wikipedia.run(query)


def openserp_search(query: str) -> str:
    url = "http://localhost:5000/search"
    params = {"q": query}
    response = requests.get(url, params=params)
    return response.json()


openserp_search_tool = Tool(
    name="openserp_search",
    description="Search the web using OpenSERP.",
    func=openserp_search,
)

tavily_search = TavilySearch(
    max_results=5,
    topic="general",
)

tavily_search_tool = Tool(
    name="tavily_search",
    description="Use Tavily to search for recent, high-quality information from the web.",
    func=lambda query: tavily_search.invoke({"query": query}),
)

prompt = hub.pull("hwchase17/react")

tools = [
    google_search_tool,
    openserp_search_tool,
    wikipedia_search,
    tavily_search_tool,
]

agent = create_react_agent(
    # llm=ChatOpenAI(model="gpt-4", temperature=0),
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temparature=0),
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, verbose=True)
response = agent_executor.invoke({
    "input": """how to be happy as a student"""})
print(response)
