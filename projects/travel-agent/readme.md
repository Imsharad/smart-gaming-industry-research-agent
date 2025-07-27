# AgentsVille Trip Planner

Welcome to the AgentsVille Trip Planner project! In this project, you'll build a sophisticated, multi-stage AI assistant that acts as an expert travel planner. Your AI will generate and refine a detailed travel itinerary for the fictional city of AgentsVille, taking into account user preferences, budget, weather, and available activities.

## Project Overview

The "AgentsVille Trip Planner" is a Jupyter Notebook-based application that interacts with a Large Language Model (LLM) to perform two main functions:

1.  **The Expert Planner (Initial Itinerary Generation)**
    - Based on user-defined travel preferences (destination, duration, interests, budget), your first agent will act as an expert travel planner.
    - It will generate a detailed, day-by-day travel itinerary as a structured JSON object that conforms to a predefined Pydantic model. This stage relies on crafting a system prompt that guides the LLM to produce complex, structured output.

2.  **The Resourceful Assistant (Itinerary Revision & Enhancement)**
    - Once an initial itinerary is generated, a second agent will revise it based on specific criteria and user feedback.
    - This agent will use a ReAct (Reasoning and Acting) loop, where it `THINK`s about a plan, `ACT`s by calling a tool (e.g., checking the weather, finding activities), and uses the `OBSERVATION` to refine the itinerary.
    - Your Python code will execute the tool calls and return the results to the agent, which will continue this cycle until the itinerary is finalized.

## Core Tasks & Project Specification

You will be provided with a starter Jupyter Notebook (`project_starter.ipynb`) and a Python library (`project_lib.py`). Your primary responsibility is to complete the `TODO` sections in the starter notebook, which involve:

1.  **Configuring your OpenAI API Key.**

2.  **Defining Vacation Details:**
    - Complete the `VacationInfo` Pydantic model to structure the traveler's vacation information.
    - Gather weather and activity data for AgentsVille based on the specified dates.

3.  **Crafting the `ITINERARY_AGENT_SYSTEM_PROMPT` for the ItineraryAgent:**
    - Instruct the LLM to act as an expert travel planner.
    - Define the task of generating a comprehensive travel itinerary.
    - Specify the output format as a JSON object conforming to the `TravelPlan` Pydantic model.
    - Provide necessary context (e.g., `VacationInfo`).
    - Encourage a Chain-of-Thought process for detailed daily plans.

4.  **Crafting the `ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT`:**
    - Create a prompt for an LLM-powered evaluation function that checks if suggested activities are suitable for the weather. The prompt must include a role, task, output format, and examples.

5.  **Defining the `get_activities_by_date_tool` docstring:**
    - The docstring must specify the tool's expected input parameter names and their data types.

6.  **Crafting the `ITINERARY_REVISION_AGENT_SYSTEM_PROMPT` for the ItineraryRevisionAgent:**
    - Assign a role to the LLM.
    - Define the task of refining the itinerary using feedback from tools.
    - Ensure the agent runs the `run_evals_tool` initially and again before finishing.
    - Dynamically include the list of `available_tools` in the prompt, describing each tool's name, purpose, and parameters.
    - Explain the `THINK-ACT-OBSERVE` cycle.
    - Specify the exact JSON format for tool calls: `{"tool_name": "[tool_name]", "arguments": {"arg1": "value1", ...}}`.
    - Ensure the agent calls the `final_answer_tool` to exit the ReAct loop.

## Provided Files

-   `project_starter.ipynb`: A starter Jupyter Notebook containing the project structure, helper functions, and `TODO` sections for you to complete.
-   `project_lib.py`: A Python library containing:
    -   Pydantic models (`VacationInfo`, `TravelPlan`, `Activity`, etc.) for data validation.
    -   Mock functions for simulated tools (e.g., `get_weather_forecast`, `search_activities_tool`).
    -   The `available_tools` dictionary, mapping tool names to their functions and JSON schemas.
    -   Utility functions like `print_in_box`.

## Environment Setup

You can work on this project in the Udacity workspace or on your local machine.

### Local Machine Setup

1.  **Install Python:** Ensure you have Python 3.8 or newer. You can download it from [python.org](https://www.python.org/downloads/).

2.  **Create a Virtual Environment:**
    ```bash
    # Navigate to your project directory
    cd path/to/agentsville_planner

    # Create a virtual environment
    python3 -m venv .venv

    # Activate the virtual environment
    # On macOS/Linux:
    source .venv/bin/activate
    # On Windows:
    # .venv\Scripts\activate
    ```

3.  **Install Required Libraries:**
    ```bash
    pip install json-repair==0.47.1 numexpr==2.11.0 openai==1.74.0 pandas==2.3.0 pydantic==2.11.7 python-dotenv==1.1.0
    ```

4.  **Obtain Project Files:** Download `project_starter.ipynb` and `project_lib.py` from the Udacity workspace into your project directory.

### Vocareum Workspace Setup

If you are using the Udacity workspace, you will be provided with a Vocareum OpenAI API key. These keys require special configuration to route requests through Vocareum's servers.

-   **Finding Your Key:** Your key is available under the "Cloud Resources" button in the lesson navigation. It will start with `voc-`.

-   **Code Configuration:** Use the following configuration in your code to use the key.

    **OpenAI Python Package v0.x:**
    ```python
    import openai
    openai.api_base = "https://openai.vocareum.com/v1"
    openai.api_key = "YOUR_VOC_API_KEY"
    ```

    **OpenAI Python Package v1.x:**
    ```python
    from openai import OpenAI
    client = OpenAI(
        base_url="https://openai.vocareum.com/v1",
        api_key="YOUR_VOC_API_KEY"
    )
    ```

## Success Criteria

You will have successfully completed the project when:

-   Your `ITINERARY_AGENT_SYSTEM_PROMPT` consistently guides the LLM to produce JSON output that validates against the `TravelPlan` Pydantic model and reflects user preferences.
-   Your `ITINERARY_REVISION_AGENT_SYSTEM_PROMPT` enables the LLM to:
    -   Always return a single message containing both a `THOUGHT` and an `ACTION`.
    -   Use reasoning in the `THOUGHT` section to choose the correct tool.
    -   Generate valid tool calls in the specified JSON format.
    -   Call the `final_answer_tool` after all evaluation criteria have passed.
-   The final itinerary returned by the LLM successfully passes all evaluation criteria and incorporates the initial traveler feedback.

## Project Assessment

Please review the project rubric on the following page. Check your work against the rubric requirements before submitting.

## Submission Instructions

To submit your project, zip up your code files (`project_starter.ipynb`, `project_lib.py`, etc.) and upload the zip file on the Project Submission Page.

