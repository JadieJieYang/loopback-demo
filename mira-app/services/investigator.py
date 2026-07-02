"""
Agentic Tier 2 investigation via Claude tool use.

Claude receives the question and a set of tools, then autonomously decides
what to search and which files to read — running multiple tool calls until
it has enough context to summarise its findings.

This is the MCP pattern: the AI drives the investigation, not scripted Python.
Claude decides the strategy; we execute whatever it asks for.

Tools available to Claude:
  search_github(query)        — searches loopback-analytics codebase
  read_file(path)             — reads a specific file from the analytics repo
  search_slack_history(query) — searches Slack workspace history (RTS API)
  read_known_issues()         — reads docs/known_issues.md directly
"""

import logging
from typing import Any

import anthropic

from config import ANTHROPIC_API_KEY
from services.mcp_github import search_codebase, _read_file, read_known_issues
from services.slack_search import search_slack_history as _search_slack

logger = logging.getLogger(__name__)

_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
_MODEL = "claude-sonnet-4-6"
_MAX_ITERATIONS = 5

_TOOLS = [
    {
        "name": "search_github",
        "description": (
            "Search the analytics codebase (SQL schema, metric definitions, documentation) "
            "for information relevant to the question."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query to find relevant code or documentation"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "read_file",
        "description": "Read the full content of a specific file from the analytics repository.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "File path relative to repo root, e.g. 'schema/raw_applications.sql'"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "search_slack_history",
        "description": "Search Slack workspace message history for conversations relevant to the question.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for Slack messages"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "read_known_issues",
        "description": "Read the known data quality issues document from the analytics repository.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

_SYSTEM = """You are Mira, an AI analyst embedded in a Slack workspace.
A team member has asked a question. Your job is to investigate using the available tools
and surface the most relevant information to help answer it.

Strategy:
1. Start with a GitHub search to find relevant schema or metric definitions
2. If you find a promising file, read it fully
3. Check the known issues doc — it often contains root causes
4. Search Slack history if codebase search wasn't enough

When you have enough information, stop calling tools and summarise your findings
in 3-5 concise bullet points. Be specific: cite file names, field names, issue numbers,
or concrete facts you found. Do not make up anything you did not find through the tools."""


def _execute_tool(tool_name: str, tool_input: dict) -> str:
    """Execute one tool call and return the result as a string."""
    try:
        if tool_name == "search_github":
            results = search_codebase(tool_input["query"])
            if not results:
                return "No matching files found in the codebase."
            return "\n\n".join(
                f"**{r['filename']}** ({r['path']}):\n{r['excerpt']}"
                for r in results
            )

        elif tool_name == "read_file":
            content = _read_file(tool_input["path"])
            if not content:
                return f"File not found: {tool_input['path']}"
            return content[:2500]

        elif tool_name == "search_slack_history":
            results = _search_slack(tool_input["query"])
            if not results:
                return "No relevant messages found in Slack history."
            return "\n\n".join(
                f"@{r.get('username', 'unknown')} in #{r.get('channel_name', '?')}:\n{r['text'][:300]}"
                for r in results[:3]
            )

        elif tool_name == "read_known_issues":
            content = read_known_issues()
            if not content:
                return "Known issues document not found."
            return content[:3000]

        else:
            return f"Unknown tool: {tool_name}"

    except Exception as e:
        logger.warning(f"Tool {tool_name} failed: {e}", exc_info=True)
        return f"Tool execution failed: {str(e)}"


def investigate(question: str) -> str:
    """
    Run an agentic investigation loop.

    Claude calls tools autonomously until it has enough context, then
    returns a concise bullet-point summary of its findings.
    Returns empty string if nothing useful was found.
    """
    if not question:
        return ""

    messages = [{"role": "user", "content": question}]

    for iteration in range(_MAX_ITERATIONS):
        try:
            response = _client.messages.create(
                model=_MODEL,
                max_tokens=800,
                system=_SYSTEM,
                tools=_TOOLS,
                messages=messages,
            )
        except Exception:
            logger.exception("Claude tool use call failed in investigator")
            return ""

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text") and block.text.strip():
                    return block.text.strip()
            return ""

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    logger.info(f"Mira calling tool: {block.name}({list(block.input.keys())})")
                    result = _execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            messages.append({"role": "user", "content": tool_results})
        else:
            break

    logger.warning("Investigator hit max iterations without a final answer")
    return ""
