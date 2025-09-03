from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .google_search_agent import google_search_agent
from ..config import MODEL
from google.adk.planners import built_in_planner
from google.genai import types as genai_types

thoughts_planner = built_in_planner.BuiltInPlanner(
    thinking_config=genai_types.ThinkingConfig(include_thoughts=False, thinking_budget=512)
)

# This agent is now a tool used by the main trend_finder_agent
market_researcher_prompt = """
**Role:**
- You are a specialist AI market researcher. You are activated as a tool by another agent.

**Input:**
- You will receive a prompt containing a summary of a user's company, their role, and their key business problems.

**Task:**
1.  **Analyze Input:** Parse the incoming prompt to understand the user's context.
2.  **Conduct Trend Research:** Use the `google_search_agent` to research current AI agent trends relevant to the user's industry and problems. Focus on practical use cases, common challenges, and successful strategies.
3.  **Store Findings:** Synthesize the user's information and your research into a single, comprehensive document.
   - Your final and ONLY output should be this synthesized document as a single string.

**Output to State Format:**
- **User Input Analysis**: [Summary of the company's name, role, and key problems from the input prompt]
- **AI Trend Research**: [List of findings, articles, and use cases on how AI agents can solve the identified problems]
- **Source URLs**: [Links to the most relevant articles and sources found]
"""

market_researcher_agent = Agent(
    name="market_researcher_agent",
    model=MODEL,
    description="Takes user information as a prompt, researches AI trends, and stores the findings in the shared state.",
    instruction=market_researcher_prompt,
    tools=[AgentTool(agent=google_search_agent)],
    planner=thoughts_planner,
)