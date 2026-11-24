# Task List Agent

A Python terminal agent that adds and lists tasks using the OpenAI Responses API.

## Setup

Open a terminal in the project folder and install the dependency.

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Enter your OpenAI API key and a model ID available to your account that supports function calling.

Try these messages.

- Add a task to submit my lab report.
- Show my tasks.
- quit

Tasks are stored in memory for the current session and reset when the program exits.