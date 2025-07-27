#!/usr/bin/env python3
"""
AgentsVille Trip Planner - Development Implementation
Transient file for incremental development and testing before notebook population
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
    print(f"Added {WORKSPACE_DIRECTORY} to the Python path")

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
    print("Please install required packages:")
    print("pip install json-repair==0.47.1 numexpr==2.11.0 openai==1.74.0 pandas==2.3.0 pydantic==2.11.7 python-dotenv==1.1.0")
    sys.exit(1)

# Import project library
try:
    from project_lib import Interest, ChatAgent, print_in_box, do_chat_completion
    from project_lib import call_weather_api_mocked, call_activities_api_mocked, call_activity_by_id_api_mocked
    print("✅ Project library imported successfully")
except ImportError as e:
    print(f"❌ Project library import error: {e}")
    sys.exit(1)

# =============================================================================
# PHASE 1: ENVIRONMENT SETUP AND DATA STRUCTURES
# =============================================================================

class OpenAIModel(str, Enum):
    GPT_41 = "gpt-4.1"
    GPT_41_MINI = "gpt-4.1-mini"
    GPT_41_NANO = "gpt-4.1-nano"

MODEL = OpenAIModel.GPT_41_MINI

def setup_openai_client():
    """Setup OpenAI client with proper configuration"""
    from dotenv import load_dotenv
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("VOCAREUM_API_KEY")
    
    if not api_key:
        raise ValueError("No API key found. Please set OPENAI_API_KEY or VOCAREUM_API_KEY in .env file")
    
    # Determine if using Vocareum endpoint
    if api_key.startswith("voc-"):
        base_url = "https://openai.vocareum.com/v1"
        print("Using Vocareum API endpoint")
    else:
        base_url = None  # Use default OpenAI endpoint
        print("Using OpenAI API endpoint")
    
    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
    )
    return client

# Vacation Info Data
VACATION_INFO_DICT = {
    "travelers": [
        {
            "name": "Yuri",
            "age": 30,
            "interests": ["tennis", "cooking", "comedy", "technology"],
        },
        {
            "name": "Hiro",
            "age": 25,
            "interests": ["reading", "music", "theatre", "art"],
        },
    ],
    "destination": "AgentsVille",
    "date_of_arrival": "2025-06-10",
    "date_of_departure": "2025-06-12",
    "budget": 130,
}

class Traveler(BaseModel):
    """A traveler with a name, age, and list of interests."""
    name: str
    age: int
    interests: List[Interest]

class VacationInfo(BaseModel):
    """Vacation information including travelers, destination, dates, and budget."""
    # TODO: Fill in the missing fields for the VacationInfo class
    travelers: List[Traveler]
    destination: str
    date_of_arrival: datetime.date
    date_of_departure: datetime.date
    budget: int

def test_vacation_info():
    """Test VacationInfo model validation"""
    print("\n" + "="*50)
    print("TESTING VACATION INFO MODEL")
    print("="*50)
    
    try:
        vacation_info = VacationInfo.model_validate(VACATION_INFO_DICT)
        print("✅ VacationInfo validation successful")
        pprint(vacation_info.model_dump())
        
        # Run assertions
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
    """Retrieve weather and activity data for vacation dates"""
    print("\n" + "="*50)
    print("RETRIEVING WEATHER AND ACTIVITY DATA")
    print("="*50)
    
    # Set pandas display options
    pd.set_option("display.max_colwidth", None)
    
    # Get weather data
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
    
    weather_df = pd.DataFrame(weather_for_dates)
    print("Weather Data:")
    print(weather_df)
    
    # Get activity data
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
    
    activities_df = pd.DataFrame(activities_for_dates)
    print(f"\nActivity Data ({len(activities_for_dates)} activities):")
    print(activities_df[['name', 'start_time', 'price', 'related_interests']].head(10))
    
    return weather_for_dates, activities_for_dates

# =============================================================================
# PHASE 2: ITINERARY AGENT SYSTEM PROMPT
# =============================================================================

# Travel Plan Data Structures (from project_lib)
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

def create_itinerary_agent_prompt(weather_data, activity_data):
    """Create the system prompt for the Itinerary Agent"""
    
    # Format weather data for context
    weather_context = "Weather Data:\n"
    for weather in weather_data:
        weather_context += f"- {weather['date']}: {weather['condition']}, {weather['temperature']}°{weather['temperature_unit']}\n"
    
    # Format activity data for context (sample)
    activity_context = f"Available Activities ({len(activity_data)} total):\n"
    for activity in activity_data[:5]:  # Show first 5 as sample
        activity_context += f"- {activity['name']} ({activity['start_time']}) - ${activity['price']} - Interests: {activity['related_interests']}\n"
    activity_context += f"... and {len(activity_data) - 5} more activities\n"
    
    # Get TravelPlan schema
    travel_plan_schema = TravelPlan.model_json_schema()
    
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
    """An agent that plans itineraries based on vacation information, weather, and activities."""
    
    def __init__(self, system_prompt, client, model):
        super().__init__(system_prompt=system_prompt, client=client, model=model)
    
    def get_itinerary(self, vacation_info: VacationInfo, model: Optional[OpenAIModel] = None) -> TravelPlan:
        """Generates a travel itinerary based on the provided vacation information."""
        response = (self.chat(
            user_message=vacation_info.model_dump_json(indent=2),
            add_to_messages=False,
            model=model or self.model,
        ) or "").strip()

        print_in_box(response, "Raw Response")

        # Parse the response
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

def test_itinerary_agent(client, vacation_info, weather_data, activity_data):
    """Test the itinerary agent"""
    print("\n" + "="*50)
    print("TESTING ITINERARY AGENT")
    print("="*50)
    
    # Create system prompt
    system_prompt = create_itinerary_agent_prompt(weather_data, activity_data)
    print("System prompt created successfully")
    
    # Create agent
    agent = ItineraryAgent(system_prompt, client, MODEL)
    
    # Generate itinerary
    try:
        travel_plan = agent.get_itinerary(vacation_info, MODEL)
        print("✅ Initial itinerary generated successfully")
        return travel_plan
    except Exception as e:
        print(f"❌ Itinerary generation failed: {e}")
        return None

# =============================================================================
# PHASE 3: EVALUATION SYSTEM IMPLEMENTATION
# =============================================================================

class AgentError(Exception):
    pass

class EvaluationResults(BaseModel):
    success: bool
    failures: List[str]
    eval_functions: List[str]

def get_eval_results(vacation_info, final_output, eval_functions) -> EvaluationResults:
    """Evaluates the final output of the itinerary agent against a set of evaluation functions."""
    if not isinstance(vacation_info, VacationInfo):
        raise ValueError("vacation_info must be an instance of VacationInfo")
    if not isinstance(final_output, TravelPlan):
        raise ValueError("final_output must be an instance of TravelPlan")
    if not isinstance(eval_functions, list) or not all(callable(fn) for fn in eval_functions):
        raise ValueError("eval_functions must be a list of callable functions")
    
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

# Basic evaluation functions
def eval_start_end_dates_match(vacation_info: VacationInfo, final_output: TravelPlan):
    """Verifies that the arrival and departure dates in vacation_info match the start and end dates in final_output."""
    if (vacation_info.date_of_arrival != final_output.start_date or 
        vacation_info.date_of_departure != final_output.end_date):
        raise AgentError(
            f"Dates do not match: {vacation_info.date_of_arrival} != {final_output.start_date} or "
            f"{vacation_info.date_of_departure} != {final_output.end_date}"
        )
    
    if final_output.start_date > final_output.end_date:
        raise AgentError(f"Start date is after end date: {final_output.start_date} > {final_output.end_date}")

def eval_total_cost_is_accurate(vacation_info: VacationInfo, final_output: TravelPlan):
    """Verifies that the total cost stated in final_output matches the sum of all activity prices."""
    actual_total_cost = 0
    
    for itinerary_day in final_output.itinerary_days:
        for activity_recommendation in itinerary_day.activity_recommendations:
            actual_total_cost += activity_recommendation.activity.price
    
    stated_total_cost = int(final_output.total_cost)
    
    if actual_total_cost != stated_total_cost:
        raise AgentError(
            f"Stated total cost does not match calculated total cost: {actual_total_cost} != {stated_total_cost}"
        )

def eval_total_cost_is_within_budget(vacation_info: VacationInfo, final_output: TravelPlan):
    """Verifies that the total cost stated in final_output is within the budget specified in vacation_info."""
    stated_total_cost = int(final_output.total_cost)
    if stated_total_cost > vacation_info.budget:
        raise AgentError(f"Total cost exceeds budget: {stated_total_cost} > {vacation_info.budget}")

def eval_itinerary_events_match_actual_events(vacation_info: VacationInfo, final_output: TravelPlan):
    """Verifies that the events listed in the itinerary match the actual events"""
    event_ids_not_matching = []
    event_ids_missing = []
    
    for itinerary_day in final_output.itinerary_days:
        for activity_recommendation in itinerary_day.activity_recommendations:
            event_id = activity_recommendation.activity.activity_id
            reference_event = call_activity_by_id_api_mocked(event_id)
            
            if reference_event is None:
                event_ids_missing.append(event_id)
            elif Activity(**reference_event) != activity_recommendation.activity:
                event_ids_not_matching.append(event_id)
    
    if event_ids_missing or event_ids_not_matching:
        raise AgentError(
            f"Event IDs missing: {event_ids_missing}\nEvent IDs not matching: {event_ids_not_matching}"
        )

def eval_itinerary_satisfies_interests(vacation_info: VacationInfo, final_output: TravelPlan):
    """Verifies that the itinerary includes activities matching each traveler's interests."""
    traveler_to_interests = {}
    traveler_to_interest_hit_counts = {}
    
    for traveler in vacation_info.travelers:
        traveler_to_interests[traveler.name] = traveler.interests
        traveler_to_interest_hit_counts[traveler.name] = 0
    
    for traveler_name, interests in traveler_to_interests.items():
        for itinerary_day in final_output.itinerary_days:
            for activity_recommendation in itinerary_day.activity_recommendations:
                matching_interests = set(traveler_to_interests[traveler_name]) & set(
                    activity_recommendation.activity.related_interests
                )
                
                if matching_interests:
                    traveler_to_interest_hit_counts[traveler_name] += 1
                    print(f"✅ Traveler {traveler_name} has a match with interest {matching_interests} "
                          f"at {activity_recommendation.activity.name}")
    
    travelers_with_no_interest_hits = [
        traveler for traveler, interest_hit_count in traveler_to_interest_hit_counts.items()
        if interest_hit_count == 0
    ]
    
    if travelers_with_no_interest_hits:
        raise AgentError(f"Travelers {travelers_with_no_interest_hits} has no matches with the itinerary.")

# Weather compatibility evaluation
def create_weather_compatibility_prompt():
    """Create the system prompt for weather-activity compatibility evaluation"""
    ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT = """You are an expert event coordinator and weather analyst responsible for determining whether outdoor activities should proceed given specific weather conditions.

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
FINAL ANSWER: IS_COMPATIBLE
""".strip()
    
    return ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT

def eval_activities_and_weather_are_compatible(vacation_info: VacationInfo, final_output: TravelPlan, client=None):
    """Verifies that no outdoor-only activities are scheduled during inclement weather conditions."""
    if client is None:
        print("⚠️ Skipping weather compatibility evaluation - no OpenAI client provided")
        return
    
    weather_prompt = create_weather_compatibility_prompt()
    activities_that_are_incompatible = []
    
    for itinerary_day in final_output.itinerary_days:
        weather_condition = itinerary_day.weather.condition
        
        for activity_recommendation in itinerary_day.activity_recommendations:
            resp = do_chat_completion(
                messages=[
                    {"role": "system", "content": weather_prompt},
                    {"role": "user", "content": 
                     f"Activity: {activity_recommendation.activity.name}\n"
                     f"Description: {activity_recommendation.activity.description}\n"
                     f"Weather Condition: {weather_condition}"},
                ],
                client=client,
                model=OpenAIModel.GPT_41_NANO,
            )
            
            if "IS_COMPATIBLE" in (resp or ""):
                is_compatible = True
            elif "IS_INCOMPATIBLE" in (resp or ""):
                is_compatible = False
            else:
                raise RuntimeError(
                    f"Unexpected response from the model: {resp}. Expected 'IS_COMPATIBLE' or 'IS_INCOMPATIBLE'."
                )
            
            if is_compatible:
                print(f"✅ Activity {activity_recommendation.activity.name} (on {itinerary_day.date}) "
                      f"and weather '{weather_condition}' are compatible.")
            else:
                activities_that_are_incompatible.append(activity_recommendation.activity.name)
                print(f"❌ Activity {activity_recommendation.activity.name} (on {itinerary_day.date}) "
                      f"and weather '{weather_condition}' are incompatible.")
    
    if activities_that_are_incompatible:
        raise AgentError(f"Activities that may be ruined by inclement weather: {activities_that_are_incompatible}")

# =============================================================================
# PHASE 4: REACT AGENT TOOLS
# =============================================================================

def calculator_tool(input_expression) -> float:
    """Evaluates a mathematical expression and returns the result as a float.
    
    Args:
        input_expression (str): A string containing a valid mathematical expression to evaluate.
    
    Returns:
        float: The result of the evaluated expression.
    """
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
    resp = call_activities_api_mocked(date=date, city=city)
    return [Activity.model_validate(activity).model_dump() for activity in resp]

def run_evals_tool(travel_plan: TravelPlan, vacation_info: VacationInfo, client=None) -> dict:
    """Runs all evaluation tools on the provided travel plan and vacation info.
    
    Args:
        travel_plan (TravelPlan): The travel plan to evaluate.
        vacation_info (VacationInfo): The vacation information for context.
        client: OpenAI client for weather compatibility evaluation (optional).
    
    Returns:
        dict: The results of the evaluations including success status and any failures.
    """
    if isinstance(travel_plan, dict):
        travel_plan = TravelPlan.model_validate(travel_plan)
    
    # Base evaluation functions (no client needed)
    base_eval_functions = [
        eval_start_end_dates_match,
        eval_total_cost_is_accurate,
        eval_itinerary_events_match_actual_events,
        eval_itinerary_satisfies_interests,
        eval_total_cost_is_within_budget,
    ]
    
    resp = get_eval_results(
        vacation_info=vacation_info,
        final_output=travel_plan,
        eval_functions=base_eval_functions,
    )
    
    # Add weather compatibility if client available
    if client:
        try:
            eval_activities_and_weather_are_compatible(vacation_info, travel_plan, client)
        except AgentError as e:
            resp.failures.append(str(e))
            resp.success = False
    
    return {
        "success": resp.success,
        "failures": resp.failures,
    }

def final_answer_tool(final_output: TravelPlan) -> TravelPlan:
    """Returns the final travel plan
    
    Args:
        final_output (TravelPlan): The final travel plan to return.
    
    Returns:
        TravelPlan: The final travel plan.
    """
    return final_output

# All available tools for ReAct agent
ALL_TOOLS = [
    calculator_tool,
    get_activities_by_date_tool,
    run_evals_tool,
    final_answer_tool,
]

def get_tool_descriptions_string(fns):
    """Generates a tool description from a function's docstring."""
    resp = ""
    for fn in fns:
        function_name = fn.__name__
        function_doc = fn.__doc__ or "No description provided."
        resp += f"* `{function_name}`: {function_doc}\n"
    return resp

# =============================================================================
# PHASE 4: REACT AGENT IMPLEMENTATION  
# =============================================================================

# Traveler feedback for final evaluation
TRAVELER_FEEDBACK = "I want to have at least two activities per day."

def eval_traveler_feedback_is_incorporated(vacation_info: VacationInfo, final_output: TravelPlan, client=None):
    """Checks if the traveler's feedback was incorporated into the revised travel plan."""
    if client is None:
        print("⚠️ Skipping traveler feedback evaluation - no OpenAI client provided")
        return
    
    agent = ChatAgent(
        system_prompt="""You are an expert in evaluating whether a travel plan incorporates traveler feedback.

## Output Format

Respond using two sections (ANALYSIS AND FINAL OUTPUT) in the following format:

    ANALYSIS:
    * [step-by-step analysis]

    FINAL OUTPUT:
    [FULLY_INCORPORATED, PARTIALLY_INCORPORATED, NOT_INCORPORATED, or UNKNOWN]
    REASON: [reasoning for the final output]
""",
        client=client,
        model=OpenAIModel.GPT_41,
    )

    resp = agent.chat(
        f"""Traveler Feedback: {TRAVELER_FEEDBACK}
Revised Travel Plan: {final_output.model_dump_json()}
""",
    )
    if "FINAL OUTPUT:" not in resp:
        raise RuntimeError(f"Unexpected response from the model: {resp}. Expected 'FINAL OUTPUT:'.")
    if "FULLY_INCORPORATED" not in resp:
        final_output_text = resp.split("FINAL OUTPUT:")[-1].strip()
        raise AgentError(f"Traveler feedback was not successfully incorporated into the revised travel plan. Response: {final_output_text}")

def create_itinerary_revision_agent_prompt(vacation_info, traveler_feedback):
    """Create the system prompt for the Itinerary Revision Agent"""
    
    # Get tool descriptions
    tool_descriptions = get_tool_descriptions_string(ALL_TOOLS)
    
    ITINERARY_REVISION_AGENT_SYSTEM_PROMPT = f"""You are an expert travel itinerary revision specialist with extensive experience in refining travel plans based on feedback and evaluation criteria.

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
    
    return ITINERARY_REVISION_AGENT_SYSTEM_PROMPT

class ItineraryRevisionAgent(ChatAgent):
    """ReAct agent that revises itineraries based on feedback and evaluation criteria"""
    
    def __init__(self, vacation_info, traveler_feedback, client, model):
        system_prompt = create_itinerary_revision_agent_prompt(vacation_info, traveler_feedback)
        super().__init__(system_prompt=system_prompt, client=client, model=model)
        self.tools = ALL_TOOLS
        self.vacation_info = vacation_info

    def get_observation_string(self, tool_call_obj) -> str:
        """Extracts the observation from the thought-action response."""
        
        if "tool_name" not in tool_call_obj:
            return "OBSERVATION: No tool name specified."

        if "arguments" not in tool_call_obj:
            return "OBSERVATION: No arguments specified."

        if not isinstance(tool_call_obj["arguments"], dict):
            return f"OBSERVATION: Arguments should be a dictionary, got {type(tool_call_obj['arguments'])} instead."

        if not isinstance(tool_call_obj["tool_name"], str):
            return f"OBSERVATION: Tool name should be a string, got {type(tool_call_obj['tool_name'])} instead."

        tool_name = tool_call_obj["tool_name"]
        arguments = tool_call_obj["arguments"]

        tool_fn = None
        for tool in self.tools:
            if tool.__name__ == tool_name:
                tool_fn = tool
                break

        if tool_fn is None:
            return f"OBSERVATION: Unknown tool name '{tool_name}' in action string."

        try:
            # Special handling for tools that need vacation_info
            if tool_name == "run_evals_tool":
                arguments["vacation_info"] = self.vacation_info
                arguments["client"] = self.client
            
            tool_response = tool_fn(**arguments)
            return f"OBSERVATION: Tool {tool_name} called successfully with response: {tool_response}"
        except Exception as e:
            return f"OBSERVATION: Error occurred while calling tool {tool_name}: {e}"

    def run_react_cycle(self, original_travel_plan: TravelPlan, max_steps: int = 10, model: Optional[OpenAIModel] = None) -> TravelPlan:
        """Runs the ReAct cycle to revise the itinerary based on the evaluation results."""
        
        # Provide the original travel plan to revise
        self.add_message(
            role="user",
            content=f"Here is the itinerary for revision:\n{original_travel_plan.model_dump_json(indent=2)}",
        )
        resp = None

        # Run the ReAct cycle for a maximum number of steps
        for step in range(max_steps):
            print(f"\n--- ReAct Step {step + 1}/{max_steps} ---")
            
            # Get the thought-action response from the agent
            resp = self.get_response(model=model or self.model) or ""
            print(f"Agent Response:\n{resp[:500]}..." if len(resp) > 500 else resp)

            # If there is no action, report it to the LLM and continue
            if "ACTION:" not in resp:
                self.add_message(role="user", content="No action found in response. Please provide both THOUGHT and ACTION.")
                continue

            action_string = resp.split("ACTION:")[1].strip()
            print(f"Action String: {action_string}")

            # Parse the tool call JSON from the action string
            try:
                # Fix any JSON formatting issues
                action_string = repair_json(action_string)
                tool_call_obj = json.loads(action_string)
                print(f"Parsed Tool Call: {tool_call_obj}")
            except json.JSONDecodeError as e:
                print(f"Invalid JSON in action string: {action_string}, Error: {e}")
                self.add_message(
                    role="user",
                    content=f"Invalid JSON in action string: {action_string}. Please provide valid JSON format.",
                )
                continue

            tool_name = tool_call_obj.get("tool_name", None)

            # If the final answer tool is called, validate and return the final travel plan
            if tool_name == "final_answer_tool":
                try:
                    final_output_arg = tool_call_obj["arguments"].get("final_output")
                    if isinstance(final_output_arg, dict):
                        new_travel_plan = TravelPlan.model_validate(final_output_arg)
                    else:
                        new_travel_plan = final_output_arg
                    
                    print("✅ Final answer tool called successfully")
                    return new_travel_plan
                except Exception as e:
                    print(f"Error validating final answer: {e}")
                    self.add_message(
                        role="user", content=f"Error validating final answer: {e}. Please provide a valid TravelPlan object."
                    )
                    continue

            # For all other tools, execute the tool call and add the observation
            else:
                observation_string = self.get_observation_string(tool_call_obj=tool_call_obj)
                print(f"Observation: {observation_string[:200]}..." if len(observation_string) > 200 else observation_string)
                self.add_message(role="user", content=observation_string)

        raise RuntimeError(f"ReAct cycle did not complete within {max_steps} steps. Last response: {resp}")

def test_react_agent(client, vacation_info, initial_travel_plan):
    """Test the ReAct agent with itinerary revision"""
    print("\n" + "="*50)
    print("TESTING REACT AGENT")
    print("="*50)
    
    # Create ReAct agent
    agent = ItineraryRevisionAgent(
        vacation_info=vacation_info,
        traveler_feedback=TRAVELER_FEEDBACK,
        client=client,
        model=MODEL
    )
    
    # Run ReAct cycle
    try:
        revised_travel_plan = agent.run_react_cycle(
            original_travel_plan=initial_travel_plan,
            max_steps=15,
            model=MODEL
        )
        print("✅ ReAct agent completed successfully")
        return revised_travel_plan
    except Exception as e:
        print(f"❌ ReAct agent failed: {e}")
        return None

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function for incremental testing"""
    print("AgentsVille Trip Planner - Development Implementation")
    print("="*60)
    
    # Phase 1: Test VacationInfo model
    vacation_info = test_vacation_info()
    if not vacation_info:
        print("❌ Phase 1 failed - VacationInfo model validation")
        return
    
    # Get weather and activity data
    weather_data, activity_data = get_weather_and_activities(vacation_info)
    
    print("\n✅ Phase 1 completed successfully")
    print(f"- VacationInfo model validated")
    print(f"- Weather data: {len(weather_data)} days")
    print(f"- Activity data: {len(activity_data)} activities")
    
    # Test Phase 2: Itinerary Agent
    print("\n" + "="*50)
    print("STARTING PHASE 2: ITINERARY AGENT")
    print("="*50)
    
    try:
        client = setup_openai_client()
        travel_plan = test_itinerary_agent(client, vacation_info, weather_data, activity_data)
        if travel_plan:
            print("✅ Phase 2 completed successfully")
            
            # Test Phase 3: Evaluation System
            print("\n" + "="*50)
            print("STARTING PHASE 3: EVALUATION SYSTEM")
            print("="*50)
            
            # Test evaluation tools
            test_results = run_evals_tool(travel_plan, vacation_info, client)
            print(f"Evaluation Results: {test_results}")
            
            if test_results['success']:
                print("✅ Phase 3 completed successfully - All evaluations passed")
            else:
                print("⚠️ Phase 3 completed with some evaluation failures:")
                for failure in test_results['failures']:
                    print(f"  - {failure}")
            
            # Test Phase 4: ReAct Agent
            print("\n" + "="*50)
            print("STARTING PHASE 4: REACT AGENT")
            print("="*50)
            
            revised_travel_plan = test_react_agent(client, vacation_info, travel_plan)
            
            if revised_travel_plan:
                print("✅ Phase 4 completed successfully")
                
                # Test Phase 5: Final Validation
                print("\n" + "="*50)
                print("STARTING PHASE 5: FINAL VALIDATION")
                print("="*50)
                
                # Add traveler feedback evaluation to the mix
                final_eval_functions = [
                    eval_start_end_dates_match,
                    eval_total_cost_is_accurate,
                    eval_itinerary_events_match_actual_events,
                    eval_itinerary_satisfies_interests,
                    eval_total_cost_is_within_budget,
                ]
                
                # Test all evaluations
                final_results = get_eval_results(
                    vacation_info=vacation_info,
                    final_output=revised_travel_plan,
                    eval_functions=final_eval_functions,
                )
                
                # Test weather compatibility
                try:
                    eval_activities_and_weather_are_compatible(vacation_info, revised_travel_plan, client)
                    weather_compatible = True
                except AgentError as e:
                    final_results.failures.append(str(e))
                    final_results.success = False
                    weather_compatible = False
                
                # Test traveler feedback
                try:
                    eval_traveler_feedback_is_incorporated(vacation_info, revised_travel_plan, client)
                    feedback_incorporated = True
                except AgentError as e:
                    final_results.failures.append(str(e))
                    final_results.success = False
                    feedback_incorporated = False
                
                print(f"\nFinal Evaluation Results:")
                print(f"- Basic evaluations: {'✅ PASS' if len([f for f in final_results.failures if 'weather' not in f.lower() and 'feedback' not in f.lower()]) == 0 else '❌ FAIL'}")
                print(f"- Weather compatibility: {'✅ PASS' if weather_compatible else '❌ FAIL'}")
                print(f"- Traveler feedback: {'✅ PASS' if feedback_incorporated else '❌ FAIL'}")
                print(f"- Overall success: {'✅ ALL PASS' if final_results.success and weather_compatible and feedback_incorporated else '❌ SOME FAILURES'}")
                
                if final_results.failures:
                    print("\nFailures:")
                    for failure in final_results.failures:
                        print(f"  - {failure}")
                
                if final_results.success and weather_compatible and feedback_incorporated:
                    print("\n🎉 ✅ Phase 5 completed successfully - ALL EVALUATIONS PASSED!")
                    print("✅ Implementation ready for notebook transfer!")
                else:
                    print("\n⚠️ Phase 5 completed with some evaluation failures")
                    print("Implementation may need further refinement")
                
            else:
                print("❌ Phase 4 failed")
            
        else:
            print("❌ Phase 2 failed")
    except Exception as e:
        print(f"❌ Phase 2/3/4/5 setup failed: {e}")
        print("Please check your API key configuration in .env file")

if __name__ == "__main__":
    main()