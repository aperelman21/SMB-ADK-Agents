from google.adk.agents import Agent, SequentialAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.planners import built_in_planner
from google.genai import types as genai_types
from .config import MODEL
from .sub_agents.trend_finder_agent import market_researcher_agent
from .sub_agents.workshop_group import (
    agent_strategist,
    solution_architect_agent,
    reporter_agent,
)
from .tools import get_state_value, set_state_value

thoughts_planner = built_in_planner.BuiltInPlanner(
    thinking_config=genai_types.ThinkingConfig(
        include_thoughts=False, thinking_budget=512)
)

root_agent_prompt = """
**Role**: You are a master orchestrator agent. Your job is to manage a workflow by calling other agents and managing the project's state.

**Your State-Driven Workflow:**
Your primary goal is to generate a final report. To do this, you must ensure the following keys are present in the shared state, in this order: `company_and_trend_research`, `agent_concept`, `technical_blueprint`.
You will check the state and execute ONE main action per turn.
**Core Language Rule:** You MUST determine the user's language from their first message.

**Step 1: Gather User Info & Research**
- **IF** `company_and_trend_research` is MISSING from the state:
    - **IF** you still need information from the user (Company Name, Website, Role, Key business problems), your ONLY action is to ask the user the next question in an enthusiasitc way. Greet them as an energetic Agent Chef at the "Mexico Cloud Summit 2025" (don't change this name and say it as it is) on your first turn.
    - **ELSE (you have all user info):**
        - First, call the `set_state_value` tool to save the user's language to the shared state with the key `"user_language"`.
        - Then, in the same turn, call the `market_researcher_agent` tool. It will return a research document. You will then save this in the next turn.
- **ELSE IF** the last turn's output was a research document from `market_researcher_agent`:
    - Your ONLY action is to call `set_state_value` to save that output to the `company_and_trend_research` key.

**Step 2: Create Agent Concept**
- **ELSE IF** `agent_concept` is MISSING from the state:
    - Call `get_state_value` to retrieve `company_and_trend_research`, then in the next turn, call `agent_strategist` with the research as the prompt. It will return a concept document.
- **ELSE IF** the last turn was a concept document from `agent_strategist`:
    - Your ONLY action is to call `set_state_value` to save that output to the `agent_concept` key.

**Step 3: Create Technical Blueprint**
- **ELSE IF** `technical_blueprint` is MISSING from the state:
    - Call `get_state_value` to retrieve `agent_concept`, then in the next turn, call `solution_architect_agent` with the concept as the `prompt`. It will return a blueprint document.
- **ELSE IF** the last turn was a blueprint document from `solution_architect_agent`:
    - Your ONLY action is to call `set_state_value` to save that output to the `technical_blueprint` key.

**Step 4: Generate Final Report**
- **ELSE** (all documents exist):
    - **Action:**
        1. First, use the `get_state_value` tool to retrieve the `"user_language"` from the shared state.
        2. Second, use the `get_state_value` tool to retrieve the `"agent_concept"`.
        3. Third, use the `get_state_value` tool to retrieve the `"technical_blueprint"`.
        4. Then, your ONLY task is to call the `reporter_agent` tool. Construct a single `prompt` argument for the tool containing all three pieces of information, clearly separated. For example: "LANGUAGE: [language]\\n\\nAGENT_CONCEPT: [concept_text]\\n\\nTECHNICAL_BLUEPRINT: [blueprint_text]".
    - **CRITICAL OUTPUT RULE:** Your final output to the user MUST be the complete, unmodified text you receive from the `reporter_agent` tool. **Do not add any other text, introductions, or conversational filler.** Just output the report.
"""

root_agent = Agent(
    model=MODEL,
    name="master_consulting_orchestrator",
    description="The main orchestrator that manages the entire AI consulting workflow, from user interaction to final report generation.",
    instruction=root_agent_prompt,
    tools=[
        AgentTool(agent=market_researcher_agent),
        AgentTool(agent=agent_strategist),
        AgentTool(agent=solution_architect_agent),
        AgentTool(agent=reporter_agent),
        set_state_value,
        get_state_value,
    ],
    planner=thoughts_planner,
)