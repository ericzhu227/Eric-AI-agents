class TaskTools:
    def __init__(self):
        self.tasks = []

    def add_task(self, description):
        description = description.strip()

        if not description:
            return {"error": "The task description cannot be empty."}

        task = {
            "id": len(self.tasks) + 1,
            "description": description,
        }
        self.tasks.append(task)
        return {"added": task}

    def list_tasks(self):
        return {"tasks": self.tasks}


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "name": "add_task",
        "description": "Add a task to the user's task list.",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "The task to add.",
                },
            },
            "required": ["description"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "list_tasks",
        "description": "Retrieve all tasks currently in the task list.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    },
]