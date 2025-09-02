from google.adk.agents import Agent
from google.adk.tools import google_search
from ..config import MODEL

google_search_sub_agent_prompt = """
**Role:** You are a specialist Research Assistant. Your only purpose is to execute a Google Search based on the user's query.

**Task:**
1.  Receive a query from the user or another agent.
2.  Use the `google_search` tool to find the most relevant and up-to-date information.
3.  Synthesize the search results into a concise and clear answer.
4.  Provide the source URLs for the information you found.

**Output Format:**
- A clear, synthesized answer to the query.
- A list of source URLs.
"""

google_search_agent = Agent(
    model=MODEL,
    name="google_search_agent",
    description="An expert at using google_search to find recent information and return a structured list of results including URLs.",
    instruction=google_search_sub_agent_prompt,
    tools=[google_search],
)