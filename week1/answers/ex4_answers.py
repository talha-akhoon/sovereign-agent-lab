"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = [
    "search_venues",
    "get_venue_details"
]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "<think>\nOkay, the user is looking for a venue in Edinburgh that can hold 300 people and has vegan options. I first tried using the search_venues function with min_capacity set to 300 and requires_vegan as true, but there was a validation error. I realized the parameters needed to be inside the \"input\" object, so I adjusted the call. The response came back with zero matches. Hmm, that means there are no venues meeting both criteria. Maybe the capacity is too high, or there aren't enough vegan options. Let me check if there are any venues with vegan options even if the capacity is slightly lower. Alternatively, maybe the user can consider a higher capacity if needed. I should inform them that no venues fit both requirements and suggest adjusting the criteria.\n</think>\n\nIt seems there are no Edinburgh venues currently available that can accommodate 300 guests *and* offer vegan options. Would you like me to:\n\n1. Search for venues with vegan options but lower capacity (e.g., 250+ guests)?\n2. Look for venues with 300+ capacity but without vegan menus?\n3. Suggest alternative solutions (e.g., combining multiple venues)?\n\nLet me know how you'd like to proceed!"

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
After setting the status of The Albanach to full, the first query only returned
The Haymarket Vaults instead of two matches. The agent no longer needed a
follow-up `get_venue_details` call because the search result already left only
one valid venue. The second query did not materially change: it still found no
venue for 300 guests with vegan options. Only the MCP server data changed; the
client code and prompt logic did not need updating.
I only updated mcp_venue_server.py because that's the only file that the agent and Rasa action both use."""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 0   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 49   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP gives you a shared tool interface, not just cleaner file organization. The
agent does not need hardcoded knowledge of each tool, because it can discover
tool names and schemas from the server at runtime. That means multiple clients,
like LangGraph and Rasa, can reuse the same capabilities and data source. It
also makes maintenance easier, because changing the server updates behaviour for
every client without rewriting each agent separately.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- The Planner is a stronger reasoning model that turns a messy user request into ordered subgoals, and it lives in the autonomous-loop half upstream of the executor.
- The Executor grows out of `sovereign_agent/agents/research_agent.py`, carries out the planner's subgoals with tools, and lives in the autonomous-loop half.
- The Structured Agent grows out of `exercise3_rasa/` and handles the pub-manager conversation with explicit flows and deterministic business-rule checks.
- The Shared MCP Tool Server grows out of `sovereign_agent/tools/mcp_venue_server.py` and provides common capabilities like venue lookup, web search, and calendar access in the shared layer.
- The Handoff Bridge lives between the two halves and passes control from the loop to the structured agent for human conversations, then back when research or follow-up actions are needed.
- The Persistent Memory Store lives in the shared layer and keeps files, notes, and long-term state so PyNanoClaw can remember decisions across runs.
- The Vector Store lives alongside memory and supports RAG for the structured agent, so it can answer grounded questions that are not hardcoded in `flows.yml`.
- The Observability layer lives across the whole system and records traces, tool calls, costs, and failures so the hybrid agent can be debugged and audited.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
The LangGraph agent is the better choice for the research side because in
Exercise 2 it handled open-ended tasks by choosing its own tool sequence. In my
run, it checked venues, calculated catering, checked weather, and generated a
flyer without a fixed script. It also handled uncertainty reasonably well, such
as admitting that no 300-person venue fit the requirements. The Rasa CALM agent
is the better choice for the phone call side because in Exercise 3 it followed a
clear confirmation flow, collected the booking details in order, and escalated
when the deposit was too high. Swapping them feels wrong because the call needs
control and predictability, while the research task needs flexible tool use.
"""