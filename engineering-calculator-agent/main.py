from getpass import getpass
from pathlib import Path

from openai import OpenAI, RateLimitError

from agent import Agent
from tools import TOOL_DEFINITIONS, calculate_dc_power, convert_units


def main():
    try:
        api_key = getpass("Enter your OpenAI API key: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nAPI key entry cancelled.")
        return
    if not api_key:
        print("An OpenAI API key is required.")
        return

    project_dir = Path(__file__).resolve().parent
    skill_path = project_dir / "SKILL.md"

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
            try:
                answer = calculator.run(message)
            except RateLimitError as error:
                if error.code == "insufficient_quota" or "no credits remaining" in error.message.lower():
                    print("OpenAI API quota exhausted. Check your API organization's billing and usage limits, then restart the calculator.")
                else:
                    print("OpenAI API rate limit reached. Wait a moment before restarting the calculator.")
                return
            print("Calculator:", answer)


if __name__ == "__main__":
    main()
