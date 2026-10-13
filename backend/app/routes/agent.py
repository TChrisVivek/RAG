
import os
import json
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

from app.services.tools import (
    search_hr_policy,
    get_employee_info
)


# Load environment variables from the .env file.
load_dotenv()

# Create the OpenAI client.
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# Instructions that guide the agent's behavior.
AGENT_INSTRUCTIONS = """
You are an HR Assistant for the company.

You can help employees with:
1. Company HR policies using search_hr_policy.
2. Employee information using get_employee_info.

Use search_hr_policy for questions about company
rules, leave policies, benefits, and other policies.

Use get_employee_info for questions about an employee's
name, department, job title, or leave balance.

Employee identification rules:
- Valid demo IDs include EMP001, EMP002, and EMP003.
- An employee's name is not their employee ID.
- If a user asks about an employee by name but does not
  provide an ID, ask for that employee's ID.
- If the user provides the ID in a follow-up message,
  use the conversation history to understand the request.
- Do not ask for an ID again if it is already available
  in the conversation.

If both tools are needed, you may call both.

Tool result handling:
- Check the tool result before answering.
- If a tool returns success=false, explain that the
  information could not be retrieved.
- If a policy search returns found=false, explain that
  the requested information was not found.
- Answer policy questions using the retrieved policy text.
- Do not assume a policy does not exist just because
  the search did not find it.
- For employee information, use only the returned record.
- Never invent company policies or employee information.

For unrelated questions, politely explain that you
only assist with company HR-related questions.
"""


# Create the API router.
router = APIRouter()


# Temporary in-memory conversation storage.
# Each conversation ID has its own list of messages.
# This memory is cleared when the server restarts.
conversation_histories: dict[str, list[dict[str, Any]]] = {}


# Tell GPT-4.1 which tools it can use and their parameters.
tools = [
    {
        "type": "function",
        "name": "search_hr_policy",
        "description": (
            "Search company HR policies for information "
            "relevant to an employee's question."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The employee's HR policy question."
                }
            },
            "required": ["question"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "get_employee_info",
        "description": (
            "Retrieve an employee's name, department, "
            "job title, and leave balance using their ID."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "string",
                    "description": "Employee ID, such as EMP001."
                }
            },
            "required": ["employee_id"],
            "additionalProperties": False
        }
    }
]


# Define the request format accepted by the endpoint.
class AgentChatRequest(BaseModel):
    question: str
    conversation_id: str


# Execute a tool requested by GPT-4.1.
def execute_tool(tool_name: str, arguments: dict):
    try:
        # TOOL 1: Search company HR policies.
        if tool_name == "search_hr_policy":
            question = arguments.get("question")

            # Validate the policy question.
            if not isinstance(question, str) or not question.strip():
                return {
                    "success": False,
                    "error": "A valid policy question is required.",
                    "results": []
                }

            # Search only after validation succeeds.
            return search_hr_policy(question)

        # TOOL 2: Retrieve employee information.
        if tool_name == "get_employee_info":
            employee_id = arguments.get("employee_id")

            # Validate the employee ID.
            if not isinstance(employee_id, str) or not employee_id.strip():
                return {
                    "success": False,
                    "error": "A valid employee ID is required."
                }

            # Retrieve the employee record.
            return get_employee_info(employee_id)

        # Handle an unknown tool name.
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }

    except Exception:
        # Return a safe error if the tool fails.
        return {
            "success": False,
            "error": "The requested HR tool could not be completed."
        }


# Main agent endpoint.
@router.post("/agent-chat")
async def agent_chat(request: AgentChatRequest):

    question = request.question
    conversation_id = request.conversation_id

    # Get the existing history, or create a new conversation.
    history = conversation_histories.setdefault(
        conversation_id, []
    )

    # Add the new question to the input without modifying
    # the saved history until the turn is complete.
    conversation_input = history + [
        {
            "role": "user",
            "content": question
        }
    ]

    # Ask GPT-4.1 to answer or request one or more tools.
    response = client.responses.create(
        model="gpt-4.1",
        instructions=AGENT_INSTRUCTIONS,
        tools=tools,
        input=conversation_input
    )

    # Record which tools were executed during this turn.
    tools_used = []

    # Continue while GPT-4.1 requests tools.
    # This supports multiple tool calls in sequence.
    while True:

        # Find the function calls in the model response.
        function_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        # If there are no tool calls, the model has finished.
        if not function_calls:
            answer = response.output_text
            break

        # Execute every requested tool and prepare its result.
        tool_outputs = []

        for item in function_calls:

            # Convert the JSON arguments into a Python dictionary.
            arguments = json.loads(item.arguments)

            # Execute the matching Python function.
            tool_result = execute_tool(
                item.name,
                arguments
            )

            tools_used.append(item.name)

            # Send the tool result back using its call ID.
            tool_outputs.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(tool_result)
            })

        # Continue the same Responses API interaction by
        # sending the model's output and the tool results.
        # This preserves the required tool-call context.
        response = client.responses.create(
            model="gpt-4.1",
            instructions=AGENT_INSTRUCTIONS,
            tools=tools,
            input=[
                *response.output,
                *tool_outputs
            ]
        )

    # Save the completed user turn and final assistant answer.
    # The next request with the same conversation ID can
    # use these messages as context.
    history.extend([
        {
            "role": "user",
            "content": question
        },
        {
            "role": "assistant",
            "content": answer
        }
    ])

    # Return a consistent response format.
    return {
        "question": question,
        "answer": answer,
        "conversation_id": conversation_id,
        "tool_used": list(dict.fromkeys(tools_used))
    }
