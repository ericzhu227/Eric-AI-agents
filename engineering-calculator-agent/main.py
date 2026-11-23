from getpass import getpass
from pathlib import Path

from openai import OpenAI

from agent import Agent
from tools import TOOL_DEFINITIONS, calculate_dc_power, convert_units


def main():
    api_key = getpass("Enter your OpenAI API key: ").strip()
    if not api_key:
        print("An OpenAI API key is required.")
        return

    project_dir = Path(__file__).resolve().parent
    skill_path = project_dir / "engineering-calculator-agent" / "SKILL.md"

    calculator = Agent(
        client=OpenAI(api_key=api_key),
        model="gpt-5-mini",
        skill_path=skill_path,
        tool_definitions=TOOL_DEFINITIONS,
        available_functions={
            "convert_units": convert_units,
            "calculate_dc_power": calculate_dc_power,
        },
    )

    print("Engineering calculator ready. Type 'quit' to exit.")

    while True:
        message = input("\nYou: ").strip()

        if message.lower() == "quit":
            break

        if message:
            print("Calculator:", calculator.run(message))


if __name__ == "__main__":
    main()