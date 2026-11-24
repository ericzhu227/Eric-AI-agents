import json
from pathlib import Path


MAX_MODEL_CALLS = 6


def load_skill_instructions(skill_path):
    """Read the Markdown body of a SKILL.md file."""
    path = Path(skill_path)
    lines = path.read_text(encoding="utf-8").splitlines()

    if not lines or lines[0] != "---":
        raise ValueError(f"Expected YAML front matter in {path}")

    try:
        end_of_front_matter = lines.index("---", 1)
    except ValueError as error:
        raise ValueError(f"Missing closing YAML delimiter in {path}") from error

    instructions = "\n".join(lines[end_of_front_matter + 1:]).strip()
    if not instructions:
        raise ValueError(f"Missing skill instructions in {path}")

    return instructions


class Agent:
    def __init__(
        self,
        client,
        model,
        *,
        skill_path,
        tool_definitions,
        available_functions,
    ):
        self.client = client
        self.model = model
        self.instructions = load_skill_instructions(skill_path)
        self.tool_definitions = tool_definitions
        self.available_functions = available_functions
        self.history = []

    def run(self, user_message):
        """Process one user message and return the agent's reply."""
        self.history.append({"role": "user", "content": user_message})

        for _ in range(MAX_MODEL_CALLS):
            response = self.client.responses.create(
                model=self.model,
                instructions=self.instructions,
                input=self.history,
                tools=self.tool_definitions,
                parallel_tool_calls=False,
            )
            self.history.extend(response.output)

            calls = [
                item for item in response.output
                if item.type == "function_call"
            ]

            if not calls:
                return response.output_text or "No text response was returned."

            for call in calls:
                result = self._execute_tool(call)
                self.history.append({
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(result),
                })

        return (
            "The agent reached its step limit before giving a final reply. "
            "A tool may already have completed an action. "
            "Check the current state before retrying."
        )

    def _execute_tool(self, call):
        """Execute a registered Python function using the model's arguments."""
        function = self.available_functions.get(call.name)
        if function is None:
            return {"error": f"Unknown tool: {call.name}"}

        try:
            arguments = json.loads(call.arguments)
            if not isinstance(arguments, dict):
                return {"error": "Tool arguments must be a JSON object."}

            return function(**arguments)
        except (TypeError, ValueError) as error:
            return {"error": str(error)}