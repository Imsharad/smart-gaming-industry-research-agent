#!/usr/bin/env python3
"""
AgentsVille Trip Planner - Optimized Development Implementation
Uses existing components from project_lib.py instead of recreating them
"""

import os
import sys
import json
import datetime
from typing import List, Optional
from pprint import pprint
from enum import Enum

# Add workspace to path if exists
WORKSPACE_DIRECTORY = "/workspace"
if os.path.exists(WORKSPACE_DIRECTORY) and WORKSPACE_DIRECTORY not in sys.path:
    sys.path.append(WORKSPACE_DIRECTORY)

# Import required packages
try:
    from openai import OpenAI
    from pydantic import BaseModel
    import pandas as pd
    import numexpr as ne
    from json_repair import repair_json
    print("✅ All required packages imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Import from project_lib instead of recreating
try:
    from project_lib import (
        Interest, ChatAgent, print_in_box, do_chat_completion,
        call_weather_api_mocked, call_activities_api_mocked, call_activity_by_id_api_mocked,
        ACTIVITY_CALENDAR, WEATHER_FORECAST, INCLIMATE_WEATHER_CONDITIONS
    )
    print("✅ Project library components imported successfully")
except ImportError as e:
    print(f"❌ Project library import error: {e}")
    sys.exit(1)

# =============================================================================
# CONFIGURATION AND SETUP
# =============================================================================

class OpenAIModel(str, Enum):
    GPT_41 = "gpt-4.1"
    GPT_41_MINI = "gpt-4.1-mini"
    GPT_41_NANO = "gpt-4.1-nano"

MODEL = OpenAIModel.GPT_41_MINI

def setup_openai_client():
    """Setup OpenAI client with proper configuration"""
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("VOCAREUM_API_KEY")
    
    if not api_key:
        raise ValueError("No API key found. Please set OPENAI_API_KEY or VOCAREUM_API_KEY in .env file")
    
    if api_key.startswith("voc-"):
        base_url = "https://openai.vocareum.com/v1"
        print("Using Vocareum API endpoint")
    else:
        base_url = None
        print("Using OpenAI API endpoint")
    
    return OpenAI(base_url=base_url, api_key=api_key)

# =============================================================================
# DATA STRUCTURES (Using Pydantic models that match notebook requirements)
# =============================================================================

# Vacation Info Data (from notebook)
VACATION_INFO_DICT = {
    "travelers": [
        {"name": "Yuri", "age": 30, "interests": ["tennis", "cooking", "comedy", "technology"]},
        {"name": "Hiro", "age": 25, "interests": ["reading", "music", "theatre", "art"]},
    ],
    "destination": "AgentsVille",
    "date_of_arrival": "2025-06-10",
    "date_of_departure": "2025-06-12",
    "budget": 130,
}

class Traveler(BaseModel):
    name: str
    age: int
    interests: List[Interest]

class VacationInfo(BaseModel):
    """Complete VacationInfo model as required by notebook TODO"""
    travelers: List[Traveler]
    destination: str
    date_of_arrival: datetime.date
    date_of_departure: datetime.date
    budget: int

# Travel Plan structures (these need to be defined as they're not in project_lib)
class Weather(BaseModel):
    temperature: float
    temperature_unit: str
    condition: str

class Activity(BaseModel):
    activity_id: str
    name: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    location: str
    description: str
    price: int
    related_interests: List[Interest]

class ActivityRecommendation(BaseModel):
    activity: Activity
    reasons_for_recommendation: List[str]

class ItineraryDay(BaseModel):
    date: datetime.date
    weather: Weather
    activity_recommendations: List[ActivityRecommendation]

class TravelPlan(BaseModel):
    city: str
    start_date: datetime.date
    end_date: datetime.date
    total_cost: int
    itinerary_days: List[ItineraryDay]

# =============================================================================
# PHASE 1: SETUP AND VALIDATION FUNCTIONS
# =============================================================================

def test_vacation_info():
    """Test VacationInfo model validation"""
    print("\n" + "="*50)
    print("TESTING VACATION INFO MODEL")
    print("="*50)
    
    try:
        vacation_info = VacationInfo.model_validate(VACATION_INFO_DICT)
        print("✅ VacationInfo validation successful")
        pprint(vacation_info.model_dump())
        
        # All the required assertions from notebook
        assert "travelers" in vacation_info.model_dump().keys()
        assert "destination" in vacation_info.model_dump().keys()
        assert "date_of_arrival" in vacation_info.model_dump().keys()
        assert "date_of_departure" in vacation_info.model_dump().keys()
        assert "budget" in vacation_info.model_dump().keys()
        assert isinstance(vacation_info.travelers, list)
        assert all(isinstance(traveler, Traveler) for traveler in vacation_info.travelers)
        assert isinstance(vacation_info.date_of_arrival, datetime.date)
        assert isinstance(vacation_info.date_of_departure, datetime.date)
        assert isinstance(vacation_info.budget, int)
        
        print("✅ All VacationInfo assertions passed")
        return vacation_info
    except Exception as e:
        print(f"❌ VacationInfo validation failed: {e}")
        return None

def get_weather_and_activities(vacation_info: VacationInfo):
    """Retrieve weather and activity data using existing project_lib functions"""
    print("\n" + "="*50)
    print("RETRIEVING WEATHER AND ACTIVITY DATA")
    print("="*50)
    
    pd.set_option("display.max_colwidth", None)
    
    # Use existing mock API functions from project_lib
    weather_for_dates = [
        call_weather_api_mocked(
            date=ts.strftime("%Y-%m-%d"), 
            city=vacation_info.destination
        )
        for ts in pd.date_range(
            start=vacation_info.date_of_arrival,
            end=vacation_info.date_of_departure,
            freq="D",
        )
    ]
    
    activities_for_dates = [
        activity
        for ts in pd.date_range(
            start=vacation_info.date_of_arrival,
            end=vacation_info.date_of_departure,
            freq="D",
        )
        for activity in call_activities_api_mocked(
            date=ts.strftime("%Y-%m-%d"), 
            city=vacation_info.destination
        )
    ]
    
    print(f"Weather Data: {len(weather_for_dates)} days")
    print(f"Activity Data: {len(activities_for_dates)} activities")
    
    return weather_for_dates, activities_for_dates

# =============================================================================
# PHASE 2: ITINERARY AGENT
# =============================================================================

def create_itinerary_agent_prompt(weather_data, activity_data):
    """Create the ITINERARY_AGENT_SYSTEM_PROMPT as required by notebook"""
    
    weather_context = "Weather Data:\n"
    for weather in weather_data:
        weather_context += f"- {weather['date']}: {weather['condition']}, {weather['temperature']}°{weather['temperature_unit']}\n"
    
    activity_context = f"Available Activities ({len(activity_data)} total):\n"
    for activity in activity_data[:5]:
        activity_context += f"- {activity['name']} ({activity['start_time']}) - ${activity['price']} - Interests: {activity['related_interests']}\n"
    activity_context += f"... and {len(activity_data) - 5} more activities\n"
    
    travel_plan_schema = TravelPlan.model_json_schema()
    
    # This matches the exact requirements from the notebook TODO
    ITINERARY_AGENT_SYSTEM_PROMPT = f"""You are an expert travel planner and itinerary specialist with extensive experience creating personalized travel experiences.

## Task

Create a comprehensive day-by-day travel itinerary based on the provided vacation information, weather conditions, and available activities. Follow these requirements:

1. **Weather Considerations**: Avoid scheduling outdoor-only activities during rain or thunderstorms
2. **Interest Matching**: Select activities that match the travelers' interests and preferences  
3. **Budget Compliance**: Ensure the total cost does not exceed the specified budget
4. **Activity Requirements**: Include at least one activity per day
5. **Realistic Planning**: Consider travel time, activity duration, and logical flow

Use a step-by-step approach to analyze the requirements and create an optimal itinerary.

## Output Format

Respond using two sections (ANALYSIS AND FINAL OUTPUT) in the following format:

    ANALYSIS:
    1. Weather Analysis: Review weather conditions for each day
    2. Interest Mapping: Identify activities matching each traveler's interests
    3. Budget Planning: Calculate costs and ensure budget compliance
    4. Day-by-Day Planning: Create logical flow for each day
    5. Validation: Verify all requirements are met

    FINAL OUTPUT:

    ```json
    {travel_plan_schema}
    ```

## Context

{weather_context}

{activity_context}

Full activity details will be provided in the user message along with vacation information.
"""
    
    return ITINERARY_AGENT_SYSTEM_PROMPT

class ItineraryAgent(ChatAgent):
    """Extends existing ChatAgent from project_lib"""
    
    def __init__(self, system_prompt, client, model):
        super().__init__(system_prompt=system_prompt, client=client, model=model)
    
    def get_itinerary(self, vacation_info: VacationInfo, model: Optional[OpenAIModel] = None) -> TravelPlan:
        """Generate itinerary using existing ChatAgent functionality"""
        response = (self.chat(
            user_message=vacation_info.model_dump_json(indent=2),
            add_to_messages=False,
            model=model or self.model,
        ) or "").strip()

        print_in_box(response, "Raw Response")

        json_text = response.strip()
        if "```json" in json_text:
            json_text = json_text.split("```json")[1].split("```")[0].strip()

        try:
            travel_plan = TravelPlan.model_validate_json(json_text)
            return travel_plan
        except Exception as e:
            print("Error validating the following text as TravelPlan JSON:")
            print(json_text)
            raise

# =============================================================================
# PHASE 3: EVALUATION SYSTEM
# =============================================================================

class AgentError(Exception):
    pass

class EvaluationResults(BaseModel):
    success: bool
    failures: List[str]
    eval_functions: List[str]

def get_eval_results(vacation_info, final_output, eval_functions) -> EvaluationResults:
    """Evaluation framework using existing print_in_box from project_lib"""
    eval_results = []
    for eval_fn in eval_functions:
        try:
            eval_fn(vacation_info, final_output)
        except AgentError as e:
            error_msg = str(e)
            print_in_box(error_msg, title="Evaluation Error")
            eval_results.append(error_msg)
    
    return EvaluationResults(
        success=len(eval_results) == 0,
        failures=eval_results,
        eval_functions=[fn.__name__ for fn in eval_functions],
    )

# All evaluation functions (unchanged from original implementation)
def eval_start_end_dates_match(vacation_info: VacationInfo, final_output: TravelPlan):
    """Verifies that dates match between vacation_info and final_output"""
    if (vacation_info.date_of_arrival != final_output.start_date or 
        vacation_info.date_of_departure != final_output.end_date):
        raise AgentError(f"Dates do not match: {vacation_info.date_of_arrival} != {final_output.start_date}")
    if final_output.start_date > final_output.end_date:
        raise AgentError(f"Start date is after end date: {final_output.start_date} > {final_output.end_date}")

def eval_total_cost_is_accurate(vacation_info: VacationInfo, final_output: TravelPlan):
    """Verifies cost calculation accuracy"""
    actual_total_cost = sum(
        activity_rec.activity.price 
        for day in final_output.itinerary_days 
        for activity_rec in day.activity_recommendations
    )
    if actual_total_cost != final_output.total_cost:
        raise AgentError(f"Cost mismatch: {actual_total_cost} != {final_output.total_cost}")

def eval_total_cost_is_within_budget(vacation_info: VacationInfo, final_output: TravelPlan):
    """Verifies budget compliance"""
    if final_output.total_cost > vacation_info.budget:
        raise AgentError(f"Over budget: {final_output.total_cost} > {vacation_info.budget}")

def eval_itinerary_events_match_actual_events(vacation_info: VacationInfo, final_output: TravelPlan):
    """Verifies activities exist using project_lib function"""
    event_ids_missing = []
    for day in final_output.itinerary_days:
        for activity_rec in day.activity_recommendations:
            event_id = activity_rec.activity.activity_id
            reference_event = call_activity_by_id_api_mocked(event_id)  # Using project_lib function
            if reference_event is None:
                event_ids_missing.append(event_id)
    
    if event_ids_missing:
        raise AgentError(f"Missing event IDs: {event_ids_missing}")

def eval_itinerary_satisfies_interests(vacation_info: VacationInfo, final_output: TravelPlan):
    """Verifies interest matching"""
    traveler_matches = {t.name: 0 for t in vacation_info.travelers}
    
    for traveler in vacation_info.travelers:
        for day in final_output.itinerary_days:
            for activity_rec in day.activity_recommendations:
                matching_interests = set(traveler.interests) & set(activity_rec.activity.related_interests)
                if matching_interests:
                    traveler_matches[traveler.name] += 1
    
    no_matches = [name for name, count in traveler_matches.items() if count == 0]
    if no_matches:
        raise AgentError(f"No interest matches for: {no_matches}")

def create_weather_compatibility_prompt():
    """ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT as required by notebook"""
    return """You are an expert event coordinator and weather analyst responsible for determining whether outdoor activities should proceed given specific weather conditions.

## Task
Evaluate whether the given activity is compatible with the specified weather condition. Consider the activity description, location (indoor/outdoor), and any backup options mentioned. When there is not enough information, assume the activity IS_COMPATIBLE with the weather. Also, look out for backup options mentioned in the activity description.

## Output format

    REASONING:
    [Provide step-by-step analysis of the activity description, weather condition, and compatibility factors]

    FINAL ANSWER:
    [IS_COMPATIBLE, IS_INCOMPATIBLE]

## Examples

Activity: Tennis Tournament
Description: Outdoor tennis competition at the city courts
Weather Condition: thunderstorm
REASONING: Tennis is an outdoor sport requiring safe conditions. Thunderstorms pose lightning risks and make courts unplayable.
FINAL ANSWER: IS_INCOMPATIBLE

Activity: Art Gallery Exhibition  
Description: Indoor art exhibition featuring local artists at the community center
Weather Condition: rainy
REASONING: Art gallery is an indoor activity held at a community center. Rain does not affect indoor venues.
FINAL ANSWER: IS_COMPATIBLE

Activity: Hiking Adventure with Indoor Backup
Description: Nature hike through forest trails. In case of rain, activities move to the visitor center for indoor nature education.
Weather Condition: rainy
REASONING: While hiking is typically outdoor, the description mentions indoor backup activities at visitor center during rain.
FINAL ANSWER: IS_COMPATIBLE"""

def eval_activities_and_weather_are_compatible(vacation_info: VacationInfo, final_output: TravelPlan, client=None):
    """Weather compatibility evaluation using existing do_chat_completion"""
    if client is None:
        print("⚠️ Skipping weather compatibility evaluation - no OpenAI client provided")
        return
    
    weather_prompt = create_weather_compatibility_prompt()
    incompatible_activities = []
    
    for day in final_output.itinerary_days:
        for activity_rec in day.activity_recommendations:
            resp = do_chat_completion(  # Using existing project_lib function
                messages=[
                    {"role": "system", "content": weather_prompt},
                    {"role": "user", "content": 
                     f"Activity: {activity_rec.activity.name}\n"
                     f"Description: {activity_rec.activity.description}\n"
                     f"Weather Condition: {day.weather.condition}"},
                ],
                client=client,
                model=OpenAIModel.GPT_41_NANO,
            )
            
            if "IS_INCOMPATIBLE" in (resp or ""):
                incompatible_activities.append(activity_rec.activity.name)
    
    if incompatible_activities:
        raise AgentError(f"Weather incompatible activities: {incompatible_activities}")

# =============================================================================
# PHASE 4: REACT AGENT TOOLS
# =============================================================================

def calculator_tool(input_expression) -> float:
    """Evaluates mathematical expressions as required by notebook"""
    return float(ne.evaluate(input_expression))

def get_activities_by_date_tool(date: str, city: str) -> List[dict]:
    """Retrieves available activities for a specific date and city from the activity database.
    
    This tool searches the activity calendar and returns all activities scheduled for the given date 
    in the specified city. Each activity includes details like name, time, location, price, and related interests.
    
    Args:
        date (str): The date to search for activities in YYYY-MM-DD format (e.g., "2025-06-10")
        city (str): The name of the city to search in (e.g., "AgentsVille")
    
    Returns:
        List[dict]: A list of activity dictionaries containing activity details, or empty list if none found
    """
    resp = call_activities_api_mocked(date=date, city=city)  # Using project_lib function
    return [Activity.model_validate(activity).model_dump() for activity in resp]

def run_evals_tool(travel_plan: TravelPlan, vacation_info: VacationInfo, client=None) -> dict:
    """Runs comprehensive evaluation suite"""
    if isinstance(travel_plan, dict):
        travel_plan = TravelPlan.model_validate(travel_plan)
    
    eval_functions = [
        eval_start_end_dates_match,
        eval_total_cost_is_accurate,
        eval_itinerary_events_match_actual_events,
        eval_itinerary_satisfies_interests,
        eval_total_cost_is_within_budget,
    ]
    
    resp = get_eval_results(vacation_info, travel_plan, eval_functions)
    
    if client:
        try:
            eval_activities_and_weather_are_compatible(vacation_info, travel_plan, client)
        except AgentError as e:
            resp.failures.append(str(e))
            resp.success = False
    
    return {"success": resp.success, "failures": resp.failures}

def final_answer_tool(final_output: TravelPlan) -> TravelPlan:
    """Returns the final travel plan"""
    return final_output

ALL_TOOLS = [calculator_tool, get_activities_by_date_tool, run_evals_tool, final_answer_tool]

def get_tool_descriptions_string(fns):
    """Generate tool descriptions from docstrings"""
    resp = ""
    for fn in fns:
        function_name = fn.__name__
        function_doc = fn.__doc__ or "No description provided."
        resp += f"* `{function_name}`: {function_doc}\n"
    return resp

# =============================================================================
# PHASE 4: REACT AGENT IMPLEMENTATION
# =============================================================================

TRAVELER_FEEDBACK = "I want to have at least two activities per day."

def create_itinerary_revision_agent_prompt(vacation_info, traveler_feedback):
    """Create ITINERARY_REVISION_AGENT_SYSTEM_PROMPT as required by notebook"""
    
    tool_descriptions = get_tool_descriptions_string(ALL_TOOLS)
    
    return f"""You are an expert travel itinerary revision specialist with extensive experience in refining travel plans based on feedback and evaluation criteria.

## Task

Your task is to revise and improve the provided travel itinerary based on traveler feedback and evaluation results. You must:

1. **Consider Traveler Feedback**: Incorporate the specific feedback provided by travelers
2. **Use Evaluation Tools**: Run evaluation tools to identify any issues with the current itinerary
3. **Make Iterative Improvements**: Use available tools to gather information and make improvements
4. **Ensure Quality**: Before providing the final output, run the evaluation tools again to verify all criteria are met
5. **Mandatory Evaluation**: You MUST run the `run_evals_tool` initially and again before using `final_answer_tool`

## Available Tools

{tool_descriptions}

## Output Format

You must respond with BOTH a THOUGHT and a single ACTION in the following format:

    THOUGHT:
    [Your reasoning about what to do next, analysis of the current situation, and justification for the chosen action]

    ACTION:
    {{"tool_name": "[tool_name]", "arguments": {{"arg1": "value1", "arg2": "value2"}}}}

## Context

**Traveler Feedback**: {traveler_feedback}

**Vacation Information**: 
- Travelers: {[t.name + " (interests: " + str(t.interests) + ")" for t in vacation_info.travelers]}
- Destination: {vacation_info.destination}
- Dates: {vacation_info.date_of_arrival} to {vacation_info.date_of_departure}
- Budget: ${vacation_info.budget}

## THINK-ACT-OBSERVE Cycle

1. **THINK**: Analyze the current situation, consider what needs to be done next
2. **ACT**: Choose and execute a tool with proper JSON format
3. **OBSERVE**: Review the tool results and plan next steps

## Important Instructions

- Always start by running `run_evals_tool` to assess the current itinerary
- Use `get_activities_by_date_tool` to find additional or alternative activities
- Use `calculator_tool` for accurate cost calculations
- Before finishing, run `run_evals_tool` again to verify all criteria are met
- End by calling `final_answer_tool` with the improved itinerary
- Each response must contain exactly one THOUGHT and one ACTION
"""

class ItineraryRevisionAgent(ChatAgent):
    """ReAct agent extending existing ChatAgent from project_lib"""
    
    def __init__(self, vacation_info, traveler_feedback, client, model):
        system_prompt = create_itinerary_revision_agent_prompt(vacation_info, traveler_feedback)
        super().__init__(system_prompt=system_prompt, client=client, model=model)
        self.tools = ALL_TOOLS
        self.vacation_info = vacation_info

    def get_observation_string(self, tool_call_obj) -> str:
        """Execute tool calls with proper error handling"""
        if "tool_name" not in tool_call_obj or "arguments" not in tool_call_obj:
            return "OBSERVATION: Missing tool_name or arguments."
        
        tool_name = tool_call_obj["tool_name"]
        arguments = tool_call_obj["arguments"]
        
        tool_fn = next((t for t in self.tools if t.__name__ == tool_name), None)
        if tool_fn is None:
            return f"OBSERVATION: Unknown tool '{tool_name}'."
        
        try:
            if tool_name == "run_evals_tool":
                arguments["vacation_info"] = self.vacation_info
                arguments["client"] = self.client
            
            tool_response = tool_fn(**arguments)
            return f"OBSERVATION: Tool {tool_name} executed successfully. Response: {tool_response}"
        except Exception as e:
            return f"OBSERVATION: Error in {tool_name}: {e}"

    def run_react_cycle(self, original_travel_plan: TravelPlan, max_steps: int = 10) -> TravelPlan:
        """Execute ReAct cycle using existing ChatAgent methods"""
        
        self.add_message("user", f"Here is the itinerary for revision:\n{original_travel_plan.model_dump_json(indent=2)}")
        
        for step in range(max_steps):
            print(f"\n--- ReAct Step {step + 1}/{max_steps} ---")
            
            resp = self.get_response() or ""
            print(f"Response: {resp[:300]}...")
            
            if "ACTION:" not in resp:
                self.add_message("user", "Please provide both THOUGHT and ACTION.")
                continue
            
            action_string = resp.split("ACTION:")[1].strip()
            
            try:
                action_string = repair_json(action_string)
                tool_call_obj = json.loads(action_string)
            except json.JSONDecodeError:
                self.add_message("user", f"Invalid JSON: {action_string}")
                continue
            
            tool_name = tool_call_obj.get("tool_name")
            
            if tool_name == "final_answer_tool":
                try:
                    final_output = tool_call_obj["arguments"].get("final_output")
                    if isinstance(final_output, dict):
                        return TravelPlan.model_validate(final_output)
                    return final_output
                except Exception as e:
                    self.add_message("user", f"Error with final answer: {e}")
                    continue
            
            observation = self.get_observation_string(tool_call_obj)
            self.add_message("user", observation)
        
        raise RuntimeError(f"ReAct cycle incomplete after {max_steps} steps")

# =============================================================================
# MAIN EXECUTION AND TESTING
# =============================================================================

def main():
    """Optimized main execution using project_lib components"""
    print("AgentsVille Trip Planner - Optimized Implementation")
    print("Using existing project_lib components")
    print("="*60)
    
    # Phase 1: Foundation
    vacation_info = test_vacation_info()
    if not vacation_info:
        return
    
    weather_data, activity_data = get_weather_and_activities(vacation_info)
    print("✅ Phase 1 completed - Foundation ready")
    
    try:
        client = setup_openai_client()
        
        # Phase 2: Itinerary Agent
        print("\nPhase 2: Testing Itinerary Agent...")
        system_prompt = create_itinerary_agent_prompt(weather_data, activity_data)
        agent = ItineraryAgent(system_prompt, client, MODEL)
        
        travel_plan = agent.get_itinerary(vacation_info)
        print("✅ Phase 2 completed - Initial itinerary generated")
        
        # Phase 3: Evaluation
        print("\nPhase 3: Testing Evaluation System...")
        eval_results = run_evals_tool(travel_plan, vacation_info, client)
        print(f"Evaluation: {eval_results}")
        print("✅ Phase 3 completed - Evaluation system working")
        
        # Phase 4: ReAct Agent
        print("\nPhase 4: Testing ReAct Agent...")
        react_agent = ItineraryRevisionAgent(vacation_info, TRAVELER_FEEDBACK, client, MODEL)
        revised_plan = react_agent.run_react_cycle(travel_plan, max_steps=15)
        
        # Phase 5: Final validation
        print("\nPhase 5: Final Validation...")
        final_results = run_evals_tool(revised_plan, vacation_info, client)
        
        success = final_results['success']
        print(f"Final Status: {'✅ SUCCESS' if success else '❌ FAILED'}")
        
        if success:
            print("\n🎉 All phases completed successfully!")
            print("Ready for notebook transfer!")
        else:
            print(f"Issues found: {final_results['failures']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()