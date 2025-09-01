from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools import VertexAiSearchTool

YOUR_DATASTORE_ID = "projects/my-custom-agents/locations/global/collections/default_collection/dataStores/jura-manual_1753826115104"
vertex_search_tool = VertexAiSearchTool(data_store_id=YOUR_DATASTORE_ID)

root_agent = Agent(
    name="jura_assistant_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about Jura E8 coffee machine."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the Jura E8 coffee machine."
    ),
    tools=[vertex_search_tool],
)