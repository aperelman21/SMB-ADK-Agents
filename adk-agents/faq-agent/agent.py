from google.adk.agents import Agent
from google.adk.tools import VertexAiSearchTool

YOUR_DATASTORE_ID = "projects/mx-summit-470817/locations/global/collections/default_collection/dataStores/mx-summit_1756863121472"
vertex_search_tool = VertexAiSearchTool(data_store_id=YOUR_DATASTORE_ID)

root_agent = Agent(
    name="panadero-asistant",
    model="gemini-2.0-flash",
    description=(
        "Agente que contesta cualquier pregunta acerca de cómo hacer pan."
    ),
    instruction=(
        "Eres un chef panadero que da clases acerca de cómo hacer pan y contestas cualquier duda acerca del proceso. Siempre contestale al usuario en el mismo idioma que ellos usen."
    ),
    tools=[vertex_search_tool],
)