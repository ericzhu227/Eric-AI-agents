from pathlib import Path
from getpass import getpass

from openai import OpenAI

from agent import Agent
from tools import TOOL_DEFINITIONS, TaskTools



# Inside main(), after setting up client and model:
project_dir = Path(__file__).resolve().parent
task_tools = TaskTools()

client = OpenAI(api_key=getpass("Enter your OpenAI API key: ").strip())
model = "gpt-6-luna"

agent = Agent(
    client=client,
    model=model,
    skill_path=project_dir / "skills" / "task-list-manager" / "SKILL.md",
    tool_definitions=TOOL_DEFINITIONS,
    available_functions={
        "add_task": task_tools.add_task,
        "list_tasks": task_tools.list_tasks,
    },
)