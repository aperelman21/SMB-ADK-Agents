from google.genai import Client

from google.adk import Agent
from google.adk.tools import google_search

# Only Vertex AI supports image generation for now.
client = Client()

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description="""an agent whose job it is to perform Google search queries and answer questions about the results.""",
    instruction="""You are an agent whose job is to perform Google search queries and answer questions about the results.
""",
    tools=[google_search],
)

