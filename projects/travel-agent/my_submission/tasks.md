# AgentsVille Trip Planner - Task Completion Guide

## Project Overview
This document outlines the step-by-step tasks required to complete the AgentsVille Trip Planner project, a multi-stage AI assistant that generates and refines travel itineraries using LLM-based agents.

## Task List

### Phase 1: Environment Setup and API Configuration

#### Task 1.1: Configure OpenAI API Key
- **Location**: `project_starter.ipynb` - Cell 4
- **Action**: Fill in the missing API key configuration
- **Details**: 
  - Uncomment and fill in the `api_key` parameter
  - Choose between direct API key or environment variable approach
  - Ensure proper base_url configuration for Vocareum if using workspace

#### Task 1.2: Test API Connection
- **Action**: Run the API configuration cell and verify connection
- **Validation**: Ensure no errors when creating the OpenAI client

### Phase 2: Data Structure Definition

#### Task 2.1: Complete VacationInfo Pydantic Model
- **Location**: `project_starter.ipynb` - Cell 8
- **Action**: Fill in the missing fields marked with `**********`
- **Required Fields**:
  - `travelers: List[Traveler]`
  - `destination: str`
  - `date_of_arrival: datetime.date`
  - `date_of_departure: datetime.date` 
  - `budget: int`
- **Validation**: Ensure all assertions pass and model validates correctly

#### Task 2.2: Fix Weather and Activity Data Retrieval
- **Location**: `project_starter.ipynb` - Cells 10 & 11
- **Action**: Fill in missing start/end dates from vacation_info
- **Details**:
  - Cell 10: Set `start=vacation_info.date_of_arrival` and `end=vacation_info.date_of_departure`
  - Cell 11: Set same date range for activities retrieval
- **Validation**: DataFrames should display weather and activity data correctly

### Phase 3: Itinerary Agent Development

#### Task 3.1: Create ITINERARY_AGENT_SYSTEM_PROMPT
- **Location**: `project_starter.ipynb` - Cell 14
- **Action**: Fill in all sections marked with `**********`
- **Required Components**:
  - **Role**: Define the LLM as an expert travel planner/agent
  - **Task**: Specify step-by-step itinerary creation process
    - Must consider outdoor activities during rain avoidance
    - Must choose events based on traveler interests
    - Must stay within budget constraints
    - Must include at least one activity per day
  - **Output Format**: 
    - ANALYSIS section format specification
    - FINAL OUTPUT section with TravelPlan JSON schema
  - **Context**: Include weather and activities data
- **Validation**: Ensure system prompt contains required sections (assertions will check)

#### Task 3.2: Test Itinerary Generation
- **Location**: `project_starter.ipynb` - Cell 15
- **Action**: Run the itinerary generation
- **Validation**: Confirm initial itinerary is generated successfully

### Phase 4: Evaluation System Implementation

#### Task 4.1: Create Weather Compatibility System Prompt
- **Location**: `project_starter.ipynb` - Cell 22
- **Action**: Fill in `ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT`
- **Required Components**:
  - **Role**: Define LLM role for weather-activity compatibility evaluation
  - **Task**: Specify evaluation criteria
    - Note: Assume compatibility when information is insufficient
    - Look for backup options in activity descriptions
  - **Output Format**: 
    - REASONING section format
    - FINAL ANSWER format: [IS_COMPATIBLE, IS_INCOMPATIBLE]
  - **Examples**: At least one example each of compatible and incompatible scenarios
- **Validation**: Test with evaluation function to ensure proper responses

#### Task 4.2: Define Activity Tool Docstring
- **Location**: `project_starter.ipynb` - Cell 27
- **Action**: Fill in `get_activities_by_date_tool` docstring
- **Required Elements**:
  - Clear description of tool's purpose and functionality
  - Input parameter specifications with data types
  - Parameter format requirements
- **Validation**: Tool should work correctly with defined parameters

### Phase 5: ReAct Agent Implementation

#### Task 5.1: Create ITINERARY_REVISION_AGENT_SYSTEM_PROMPT
- **Location**: `project_starter.ipynb` - Cell 34
- **Action**: Fill in all sections marked with `**********`
- **Required Components**:
  - **Role**: Define LLM role for itinerary revision
  - **Task**: Specify revision process
    - Must consider traveler feedback
    - Must use evaluation tools for validation
    - Must run evaluation tools before final output
  - **Available Tools**: Dynamic tool descriptions and parameters
  - **Output Format**: 
    - THOUGHT section format
    - ACTION section with JSON tool call format: `{"tool_name": "[tool_name]", "arguments": {"arg1": "value1", ...}}`
  - **Context**: Additional information for task execution
- **Validation**: Test single THOUGHT/ACTION response format

#### Task 5.2: Test ReAct Cycle
- **Location**: `project_starter.ipynb` - Cell 35
- **Action**: Run the ReAct cycle to generate revised itinerary
- **Validation**: Confirm revised itinerary is generated successfully

### Phase 6: Final Validation and Testing

#### Task 6.1: Run Complete Evaluation Suite
- **Location**: `project_starter.ipynb` - Cell 36
- **Action**: Validate revised travel plan against all evaluation functions
- **Validation Criteria**:
  - Start/end dates match vacation info
  - Total cost is accurate and within budget
  - All activities exist and match reference data
  - Activities satisfy traveler interests
  - Activities are weather-compatible
  - Traveler feedback is incorporated (at least 2 activities per day)
- **Validation**: All evaluation functions must pass

#### Task 6.2: Display Final Itinerary
- **Location**: `project_starter.ipynb` - Cell 37
- **Action**: Review final travel plan output
- **Validation**: Itinerary should be properly formatted and complete

#### Task 6.3: Generate Trip Narration (Optional)
- **Location**: `project_starter.ipynb` - Cell 39
- **Action**: Run the trip narration function
- **Validation**: Audio file should be generated successfully

## Success Criteria Verification

### General Prompt Design
- [ ] ITINERARY_AGENT_SYSTEM_PROMPT includes role definition
- [ ] Encourages detailed daily plans through Chain-of-Thought
- [ ] Specifies JSON output format matching TravelPlan model
- [ ] Provides necessary context (VacationInfo, weather, activities)
- [ ] ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT includes role, task, output format, and examples

### Agent Reasoning and Tool Use
- [ ] get_activities_by_date_tool has sufficient description and parameter definitions
- [ ] ITINERARY_REVISION_AGENT_SYSTEM_PROMPT includes role, task, THINK-ACT-OBSERVE cycle
- [ ] Lists available tools with purposes and parameters
- [ ] Specifies exact ACTION format for tool invocation
- [ ] Includes exit instruction via final_answer_tool
- [ ] States run_evals_tool must be run before final_answer_tool

### Structured Output Validation
- [ ] VacationInfo Pydantic model created properly
- [ ] VacationInfo model reads dates correctly for weather/activity data
- [ ] TravelPlan schema included in relevant system prompts

## Notes
- All TODO sections must be completed for project submission
- Test each component thoroughly before moving to the next phase
- Pay attention to JSON schema requirements for structured outputs
- Ensure proper error handling and validation throughout
- Consider edge cases and model limitations when crafting prompts