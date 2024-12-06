# AI Stepper

A lightweight, flexible Python framework for creating step-by-step AI workflows with full LLM prompt control.

## Overview

AI Stepper is a basic sequential AI agent system designed for developers who need:
- Full control over LLM prompts and interactions
- Step-by-step workflow execution
- Strong output validation
- Simple retry mechanisms
- Clear and predictable agent behavior

If you're looking for a straightforward way to create sequential AI workflows without the complexity of full-scale agent frameworks, AI Stepper is the right choice.

## Key Features

- **LLM Agnostic**: Works with any LLM through litellm annotations (OpenAI, Anthropic, local models, etc.)
- **Full Prompt Control**: Define exactly how your LLM should behave at each step
- **Sequential Execution**: Each step's output is automatically available as input for subsequent steps
- **YAML-Driven Workflows**: Define your entire workflow in a simple YAML file
- **Schema Compatibility**: Supports both JSON Schema and YAML annotations for input/output validation
- **Strong Validation**: Validate LLM outputs against predefined schemas
- **Rich Logging**: Built-in Markdown-formatted logging with step context
- **Flexible Callbacks**: Custom callback system for monitoring and debugging

## Installation

```bash
pip install -U ai-stepper
```

## Usage

### 1. Environment Setup
Create a `.env` file with your LLM configuration:

```env
OPENAI_API_BASE=your_llm_api_base
OPENAI_API_KEY=your_llm_api_key
OPENAI_MODEL_NAME=your_model_name
```

### 2. Create a Workflow
Define your workflow steps in a YAML file (e.g., `dynamic_team_task_management.yaml`):

```yaml
generate_team_members:
  task: >
    Generate {team_size} team members with realistic names and roles.
    Each team member should have:
    - id (integer)
    - name (string)
    - role (string: developer, designer, manager, etc.)
    - skills (array of strings)
  inputs:
    team_size:
      type: integer
  outputs:
    team_members:
      type: array
      items:
        type: object
        properties:
          id:
            type: integer
          name:
            type: string
          role:
            type: string
          skills:
            type: array
            items:
              type: string

generate_tasks:
  task: >
    Generate {task_count} tasks that need to be assigned to the team members {team_members}.
    Each task should have:
    - id (integer)
    - title (string)
    - description (string)
    - required_skills (array of strings)
    - estimated_hours (integer between 4-40)
  inputs:
    task_count:
      type: integer
    team_members:
      type: array
  outputs:
    tasks:
      type: array
      items:
        type: object
        properties:
          id:
            type: integer
          title:
            type: string
          description:
            type: string
          required_skills:
            type: array
            items:
              type: string
          estimated_hours:
            type: integer
```

### 3. Implement the Runner
Create a Python script to run your workflow:

```python
from ai_stepper import AI_Stepper
import os
from dotenv import load_dotenv
from rich import print
from typing import Optional
from datetime import datetime

# Load environment variables
load_dotenv(override=True)

def agent_logger(message: str, step_name: Optional[str] = None):
    """Log agent actions and responses."""
    if step_name:
        print(f"\n### {step_name.upper()}\n{message}\n")
    else:
        print(f"\n{message}\n")

def run_workflow(stepper: AI_Stepper, name: str, yaml_file: str, inputs: dict) -> None:
    """Run a single workflow and handle any errors."""
    try:
        print(f"\n[bold blue]Running {name} workflow...[/bold blue]")
        result = stepper.run(
            steps_file=yaml_file,
            initial_inputs=inputs,
            callback=agent_logger
        )
        print(f"[green]Result:[/green]", result)
    except Exception as e:
        print(f"[bold red]Error in {name} workflow:[/bold red] {str(e)}")

def main():
    """Main execution function."""
    try:
        # Initialize the AI_Stepper
        stepper = AI_Stepper(
            llm_base_url=os.getenv("OPENAI_API_BASE"),
            llm_api_key=os.getenv("OPENAI_API_KEY"),
            llm_model_name=os.getenv("OPENAI_MODEL_NAME")
        )

        # Define and run workflows
        workflows = [
            ("dynamic team task management", "yaml/dynamic_team_task_management.yaml", {
                "team_size": 12,
                "task_count": 10
            }),
        ]
    
        for name, yaml_file, inputs in workflows:
            run_workflow(stepper, name, yaml_file, inputs)

    except Exception as e:
        print(f"[bold red]Critical error:[/bold red] {str(e)}")

if __name__ == "__main__":
    main()
```

This example demonstrates a workflow that:
1. Generates a team of members with different roles and skills
2. Creates tasks with specific requirements
3. Uses structured validation to ensure the LLM outputs match the expected format

The framework handles:
- Environment configuration
- YAML workflow loading
- Step execution
- Error handling
- Logging
- Output validation

For more examples, check the `yaml/` directory in the repository.

## Logging and Output

### Markdown Logger

AI Stepper includes a built-in markdown logger utility that creates well-formatted logs of your workflow execution. The logger supports:

- Timestamped entries with timezone support
- Structured message formatting
- Code block formatting with syntax highlighting
- Token usage tracking
- JSON pretty-printing
- File output capabilities

Example usage:

```python
from ai_stepper.utils.logger import markdown_logger
from ai_stepper.schema.callback import CallBack

# Create a callback
callback = CallBack(
    sender="LLM",
    step_name="analyze_sentiment",
    object="output",
    message="Response for sentiment analysis",
    created=int(datetime.utcnow().timestamp()),
    code=CodeItem(
        language="json",
        content={"sentiment_analysis": {"product_sentiments": [...]}}
    )
)

# Log to file
markdown_logger(callback, "log.md")
```

### Schema Validation

AI Stepper enforces strict schema validation for LLM outputs. Each step's output must conform to the schema defined in your YAML workflow:

```yaml
analyze_sentiment:
  task: >
    Perform sentiment analysis on the feedback {feedback}.
    Determine whether each theme has a positive, negative, or neutral sentiment.
  inputs:
    feedback:
      type: array
  outputs:
    sentiment_analysis:
      type: object
      properties:
        product_sentiments:
          type: array
          items:
            type: object
            properties:
              product:
                type: string
              theme_sentiments:
                type: array
                items:
                  type: object
                  properties:
                    theme:
                      type: string
                    sentiment:
                      type: string
```

The framework will:
1. Validate all outputs against their schemas
2. Provide clear error messages for validation failures
3. Support retry mechanisms for failed validations
4. Log validation results in markdown format

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
