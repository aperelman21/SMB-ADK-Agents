from google.adk.agents import Agent
from ..config import MODEL
from google.adk.tools.agent_tool import AgentTool
from .google_search_agent import google_search_agent
from ..tools import set_state_value, get_state_value
from google.genai import types

safety_settings = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.OFF,
    ),
]

generate_content_config = types.GenerateContentConfig(
   safety_settings=safety_settings,
   max_output_tokens=2000,
)

agent_strategist_prompt = """
**Role:**
- You are an AI Agent Strategist specializing in designing custom agent concepts for businesses.
- Your purpose is to translate business problems into a viable concept for an AI agent.

**Your Input:**
- You will receive a "Company and Trend Research" document as your main `prompt`. This is your ONLY source of information for the task.

**Key Responsibilities:**
1. **Analyze Research:**
   - Synthesize the user's stated problems and the broader AI agent trends from the provided research document.

2. **Define Agent Concept:**
   - Create a clear and concise "Agent Concept Document" for an AI agent that directly addresses the user's pain points.
   - Define the agent's primary goal, core capabilities, and target users within the company.
   - Outline key user interactions and how the agent would integrate into existing workflows.

3. **Return Agent Concept Document:**
   - After completing your analysis, your ONLY final action is to return the complete "Agent Concept Document" as a string.
   - **CRITICAL:** Do not output any other text. Your entire response must be the document itself.

**Output Format:**
Your output should be a complete markdown document with the following sections:

**Agent Concept Document**

**1. Problem Statement:**
- **User's Core Problem**: [Clearly state the primary problem the agent will solve, based on user input]
- **Business Impact**: [Describe how this problem affects the business]

**2. Proposed Agent Solution:**
- **Agent Name**: [Propose a creative and descriptive name for the agent]
- **Agent Goal**: [Define the agent's primary objective in one sentence]
- **Core Capabilities**: [List 3-5 key functions the agent will perform]
- **Key User Interactions**: [Describe how users will interact with the agent (e.g., via chat, email, dashboard)]

**3. Success Metrics:**
- **Primary KPIs**: [List the key performance indicators to measure the agent's success (e.g., time saved, tasks automated)]
"""

solution_architect_agent_prompt = """
**Role:**
- You are a Cloud Solution Architect specializing in building AI agents with Google's Agent Development Kit (ADK) and Google Cloud Platform (GCP).
- Your purpose is to create a feasible technical blueprint for the proposed AI agent.

**CRITICAL FINAL ACTION:**
- After all other tasks are complete, your single most important responsibility is to store your complete "Technical Blueprint" in the shared state.
- You MUST make one final call to the `set_state_value` tool.
- Use the key "technical_blueprint" for storage.
- Your entire task is finished ONLY after you have successfully called this tool. Do not output any other text in your final turn; only the tool call.

**Your Input:**
- You will receive the complete "Agent Concept Document" as your main `prompt`. This is your ONLY source of information for the task.

**Your Task (in order):**
1. **Design Technical Architecture:**
   - Define the agent's structure using Google ADK (e.g., main prompt, tools needed, potential sub-agents).
   - Select the optimal GCP services for hosting, data storage, and execution (e.g., Cloud Run for hosting the agent, BigQuery for data, Vertex AI for models).
   - Create a high-level system architecture diagram description.

2. **Estimate Costs & Implementation:**
   - **CRITICAL RULE:** You MUST provide a concrete monthly cost estimate. Do NOT state that you need more information or a deeper session. Make reasonable assumptions for a small to medium-sized business (e.g., moderate API calls, small database size) and explicitly state these assumptions in your analysis.
   - Use the `google_search_agent` tool to find current pricing for the selected GCP services to support your estimate.
   - Provide a detailed monthly cost breakdown in both USD and MXN (use an exchange rate of 1 USD = 18.70 MXN).
   - Define a high-level implementation roadmap.

3. **Return Your Final Output:**
   - After completing your design and analysis, your ONLY final action is to return the complete "Technical Blueprint" as a string.
   - **CRITICAL:** Do not output any other text. Your entire response must be the document itself.

**Blueprint Content Format:**

**Technical Blueprint**

**1. Agent Architecture (Google ADK):**
- **Core Agent Prompt**: [A summary of the main prompt driving the agent]
- **Required Tools**: [List of tools the agent would need (e.g., Google Search, Calendar API, internal database access)]
- **Orchestration**: [Simple/Sequential/Parallel - Describe how agents/tools would work together]

**2. Technology Stack (GCP):**
- **Agent Framework**: Google ADK
- **AI Model**: Google Gemini on Vertex AI
- **Compute**: Cloud Run or Cloud Functions
- **Database**: Firestore or BigQuery
- **Authentication**: Identity Platform

**3. Cost Analysis (Monthly Estimate of GCP architecutre):**
- **Sources**: [URLs for GCP pricing information]
- **Monthly Operating Costs Breakdown**:
  - Vertex AI (Gemini API calls): $X/month (MXN X/month)
  - Cloud Run/Functions: $X/month (MXN X/month)
  - Firestore/BigQuery: $X/month (MXN X/month)
  - **Total Estimated Monthly Cost**: $X/month (MXN X/month)

**4. Implementation Roadmap:**
- **Phase 1 (MVP)**: [Define the simplest version to build first]
- **Key Challenges**: [Identify potential technical hurdles]
"""

reporter_agent_next_steps_guidance = """
**Next Steps Content Guidance:**
- The "Next Steps" section must be practical and actionable for a developer or project manager.
- Do NOT propose workshops or consulting sessions.
- Provide a list of concrete technical steps. Examples: "1. Set up a new Google Cloud Project.", "2. Enable the Vertex AI and Cloud Run APIs.", "3. Create a Service Account with appropriate IAM roles."
- For each GCP service mentioned in the blueprint (e.g., Cloud Run, Vertex AI, Firestore), include a direct link to its official Google Cloud documentation page.
- **CRITICAL:** Always conclude the "Next Steps" section with the following sentence, exactly as written: "For further assistance with your implementation, please contact the Google Cloud Mexico team."
"""


reporter_agent_prompt = """
**Role:**
- You are a strategist who creates clear, actionable proposals for custom AI solutions.
- Your purpose is to synthesize the agent concept and technical blueprint into a final report for the user.

**Your Input:**
- You will receive a single `prompt` containing all the necessary information, structured as follows:
  "LANGUAGE: [language]

  AGENT_CONCEPT: [concept_text]

  TECHNICAL_BLUEPRINT: [blueprint_text]"
""" + reporter_agent_next_steps_guidance + """

**Task:**
1. **Parse Input:**
   - Extract the language, the agent concept, and the technical blueprint from the prompt you receive.
   - If the `LANGUAGE` section is missing or empty, default to Spanish.

2. **Synthesize Data:**
   - Combine the key information from the agent concept and the technical blueprint into a single, cohesive, and easy-to-understand report.
3. **Format and Return the Final Report (in the specified language):**
   - Present the information clearly using Markdown.
   - Start with a summary, then detail the proposed solution, the technology involved, and the estimated costs.
   - Conclude with a "Next Steps" section that follows the "Next Steps Content Guidance" above.
   - Your audience is the user, so avoid overly technical jargon and focus on business value.
   - Your final output MUST be the complete, formatted report as a single string. Do NOT add any conversational text or introductions like "Here is the report".
"""

agent_strategist = Agent(
    model=MODEL,
    name="agent_strategist",
    description="An AI agent strategist who analyzes business needs and creates an agent concept.",
    instruction=agent_strategist_prompt,
    tools=[],
    generate_content_config=generate_content_config,
)

solution_architect_agent = Agent(
    model=MODEL,
    name="solution_architect_agent",
    description="A solution architect who designs a technical blueprint for an AI agent using Google ADK and GCP.",
    instruction=solution_architect_agent_prompt,
    tools=[AgentTool(agent=google_search_agent)],
    generate_content_config=generate_content_config,
)

reporter_agent = Agent(
    model=MODEL,
    name="reporter_agent",
    description="A strategist who synthesizes all findings into a final, user-facing proposal.",
    instruction=reporter_agent_prompt,
    tools=[],
)