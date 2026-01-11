<rubric>
Use this project rubric as a guide for evaluating project criteria.

1. <general_prompt_design>
Design a system prompt that effectively guides the LLM to produce a comprehensive, structured itinerary.

<requirements_to_pass>
The prompt in ITINERARY_AGENT_SYSTEM_PROMPT satisfies the following:

Clearly instructs LLM to assume a role as a travel planner, travel agent, or something similar
Encourages detailed daily plans through Chain-of-Thought guidance or examples.
Specifies JSON output format matching the TravelPlan Pydantic model structure.
Provides necessary context, including VacationInfo object, weather data, and activities data
</requirements_to_pass>

<reviewer_tip>
PASS if

the system prompt includes clear role instruction, JSON output expectations tied to the Pydantic model, and necessary context, AND
the JSON output validates against the TravelPlan model.
Review for examples or implicit cues that elicit step-by-step planning (e.g., "for each day…").

Recommend including a model schema in the prompt if results are inconsistent.
</reviewer_tip>

2. Design a system prompt that determines whether an event should be avoided due to weather conditions

<requirements_to_pass>
The prompt in ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT satisfies the following:

Clearly defines the LLM role and task
Specifies exact output format
Includes relevant examples illustrating expected evaluations
</requirements_to_pass>

<reviewer_tip>
PASS if
the role, task, and output format are present in the prompt, AND
the prompt mentions considering backup options for activities,
the examples show at least one example of IS_COMPATIBLE and one of IS_INCOMPATIBLE
This prompt is less involved than the others. The emphasis here is on the examples.
</reviewer_tip>
</general_prompt_design>

3. <agent_reasoning_and_tool_use>
Design a tool description that guides the LLM to call it when needed

<requirements_to_pass>
The docstring for the get_activities_by_date_tool function should:

provide sufficient description for understanding tool's purpose and use and
define expected input parameters and their data types and formats.
</requirements_to_pass>

<reviewer_tip>
Check that the docstring for get_activities_by_date_tool includes:

A short description on the first line

A list of parameters/arguments including date (str) and city (str)

The date format is given as YYYY-MM-DD or %Y-%m-%d or something equivalent.

Check that the tool is used properly the ReAct agent

If the tool parameter date is not being written properly by the LLM, recommend adding the date format to the description
</reviewer_tip>

<agent_reasoning_and_tool_use>

4. Design a prompt that guides an LLM to use reasoning and tools in the ReAct cycle

<requirements_to_pass>
The prompt ITINERARY_REVISION_AGENT_SYSTEM_PROMPT should satisfy the following:

Clearly states LLM role and itinerary revision task.
Details the THINK-ACT-OBSERVE cycle explicitly.

Lists all available tools, their purposes, and parameter requirements (adding this dynamically is nice, but not required).

Specifies exact ACTION format for tool invocation: {"tool_name": "[tool_name]", "arguments": {"arg1": "value1", ...}}

Includes explicit exit instruction via final_answer_tool invocation.

States that the run_evals_tool must be run before the final_answer_tool
</requirements_to_pass>

<reviewer_tip>
PASS if:

the prompt guides the LLM step-by-step, clearly delineating the reasoning (THOUGHT) and the tool call (ACTION) portions of the response (e.g. in the output format section)

the tool descriptions and argument schemas are included in the prompt (dynamic insertion is nice but not needed)

the agent calls run_evals_tool at least once

the agent terminates the loop by calling final_answer_tool

If the model is not requesting tool calls or the right tool calls, recommend having the LLM use a step-by-step process within the THOUGHT section to plan, do reasoning, and then to decide on a tool to use.

Note: This prompt doesn't need examples to work well.
</reviewer_tip>
</agent_reasoning_and_tool_use>

5. <structured_output_validation>
Pydantic models are created and used properly

<requirements_to_pass>
The VacationInfo Pydantic model is:

created properly given the JSON structure representing the travelers and their vacation details
is read properly (start and end dates) when pulling the weather and activity data
The TravelPlan Pydantic model's schema is:

included in AT LEAST ONE system prompt that needs to output a TravelPlan data structure (there are two such prompts, so it is best, but not required, to include this schema in both of them)
</requirements_to_pass>

<reviewer_tip>
PASS if:
The VacationInfo Pydantic object is created and used successfully at the beginning of the notebook
The TravelPlan Pydantic object is successfully generated and viewed at the end of the notebook
</reviewer_tip>
</structured_output_validation>
</rubric>