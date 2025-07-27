#!/usr/bin/env python3
"""
AgentsVille Trip Planner - Final Implementation with YAML Prompt Management
Uses existing project_lib components and YAML-based prompt templates
"""

import os
import sys
import json
import datetime
import yaml
from typing import List, Optional
from pprint import pprint
from enum import Enum
from pathlib import Path

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

# Import from project_lib
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
# PROMPT MANAGEMENT SYSTEM
# =============================================================================

class PromptManager:
    """Manages YAML-based prompt templates"""
    
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)
        self._prompt_cache = {}
    
    def load_prompt(self, prompt_name: str) -> dict:
        """Load a prompt template from YAML file"""
        if prompt_name in self._prompt_cache:
            return self._prompt_cache[prompt_name]
        
        prompt_file = self.prompts_dir / f"{prompt_name}.yaml"
        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
        
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt_data = yaml.safe_load(f)
        
        self._prompt_cache[prompt_name] = prompt_data
        return prompt_data
    
    def build_prompt(self, prompt_name: str, **template_vars) -> str:
        """Build a complete prompt by filling template variables"""
        prompt_data = self.load_prompt(prompt_name)
        
        # Build sections
        sections = []
        
        # Add role
        if 'role' in prompt_data:
            sections.append(prompt_data['role'].strip())
        
        # Add task
        if 'task' in prompt_data:
            sections.append("## Task\n\n" + prompt_data['task'].strip())
        
        # Add available tools (for ReAct agents)
        if 'available_tools_template' in prompt_data:
            tools_section = prompt_data['available_tools_template'].format(**template_vars)
            sections.append(tools_section.strip())
        
        # Add output format
        if 'output_format' in prompt_data:
            sections.append("## Output Format\n\n" + prompt_data['output_format'].strip())
        
        # Add context
        if 'context_template' in prompt_data:
            context_section = prompt_data['context_template'].format(**template_vars)
            sections.append(context_section.strip())
        
        # Add ReAct cycle info
        if 'react_cycle' in prompt_data:
            sections.append(prompt_data['react_cycle'].strip())
        
        # Add instructions
        if 'instructions' in prompt_data:
            sections.append(prompt_data['instructions'].strip())
        
        # Add examples (for evaluation prompts)
        if 'examples' in prompt_data:
            examples_section = self._format_examples(prompt_data['examples'])
            sections.append("## Examples\n\n" + examples_section)
        
        return "\n\n".join(sections)
    
    def _format_examples(self, examples) -> str:
        """Format examples section from YAML data"""
        if isinstance(examples, list):
            # List of examples (like weather compatibility)
            formatted = []
            for example in examples:
                ex_text = f"Activity: {example['activity']}\n"
                ex_text += f"Description: {example['description']}\n"
                ex_text += f"Weather Condition: {example['weather']}\n"
                ex_text += f"REASONING: {example['reasoning']}\n"
                ex_text += f"FINAL ANSWER: {example['answer']}"
                formatted.append(ex_text)
            return "\n\n".join(formatted)
        
        elif isinstance(examples, dict):
            # Dict with positive/negative examples
            formatted = []
            for category, example in examples.items():
                ex_text = f"**{category.upper()}:**\n"
                ex_text += f"Feedback: {example['feedback']}\n"
                ex_text += f"Analysis: {example['analysis']}\n"
                ex_text += f"Result: {example['result']}"
                formatted.append(ex_text)
            return "\n\n".join(formatted)
        
        return str(examples)

# Global prompt manager
prompt_manager = PromptManager()

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
# DATA STRUCTURES
# =============================================================================

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
    travelers: List[Traveler]
    destination: str
    date_of_arrival: datetime.date
    date_of_departure: datetime.date
    budget: int

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
# PHASE 1: SETUP AND VALIDATION
# =============================================================================

def test_vacation_info():
    """Test VacationInfo model validation"""
    print("\n" + "="*50)
    print("TESTING VACATION INFO MODEL")
    print("="*50)
    
    try:
        vacation_info = VacationInfo.model_validate(VACATION_INFO_DICT)
        print("✅ VacationInfo validation successful")
        
        # All required assertions
        assert "travelers" in vacation_info.model_dump().keys()
        assert "destination" in vacation_info.model_dump().keys()
        assert "date_of_arrival" in vacation_info.model_dump().keys()
        assert "date_of_departure" in vacation_info.model_dump().keys()
        assert "budget" in vacation_info.model_dump().keys()
        
        print("✅ All VacationInfo assertions passed")
        return vacation_info
    except Exception as e:
        print(f"❌ VacationInfo validation failed: {e}")
        return None

def get_weather_and_activities(vacation_info: VacationInfo):
    """Retrieve weather and activity data using project_lib functions"""
    print("\n" + "="*50)
    print("RETRIEVING WEATHER AND ACTIVITY DATA")
    print("="*50)
    
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
# PHASE 2: ITINERARY AGENT WITH YAML PROMPTS
# =============================================================================

def create_itinerary_agent_prompt(weather_data, activity_data):
    """Create ITINERARY_AGENT_SYSTEM_PROMPT using YAML template"""
    
    # Format context data
    weather_context = "Weather Data:\n"
    for weather in weather_data:
        weather_context += f"- {weather['date']}: {weather['condition']}, {weather['temperature']}°{weather['temperature_unit']}\n"
    
    activity_context = f"Available Activities ({len(activity_data)} total):\n"
    for activity in activity_data[:5]:
        activity_context += f"- {activity['name']} ({activity['start_time']}) - ${activity['price']} - Interests: {activity['related_interests']}\n"
    activity_context += f"... and {len(activity_data) - 5} more activities\n"
    
    # Get TravelPlan schema
    travel_plan_schema = TravelPlan.model_json_schema()
    
    # Build prompt using YAML template
    return prompt_manager.build_prompt(
        "itinerary_agent",
        travel_plan_schema=travel_plan_schema,
        weather_context=weather_context,
        activity_context=activity_context
    )

class ItineraryAgent(ChatAgent):
    """Itinerary agent using YAML-based prompts"""
    
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
            print(json_text[:500] + "..." if len(json_text) > 500 else json_text)
            raise

# =============================================================================
# PHASE 3: EVALUATION SYSTEM WITH YAML PROMPTS
# =============================================================================

class AgentError(Exception):
    pass

class EvaluationResults(BaseModel):
    success: bool
    failures: List[str]
    eval_functions: List[str]

def get_eval_results(vacation_info, final_output, eval_functions) -> EvaluationResults:
    """Evaluation framework using existing print_in_box"""
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

# Evaluation functions (unchanged)
def eval_start_end_dates_match(vacation_info: VacationInfo, final_output: TravelPlan):
    if (vacation_info.date_of_arrival != final_output.start_date or 
        vacation_info.date_of_departure != final_output.end_date):
        raise AgentError(f"Dates do not match: {vacation_info.date_of_arrival} != {final_output.start_date}")

def eval_total_cost_is_accurate(vacation_info: VacationInfo, final_output: TravelPlan):
    actual_total_cost = sum(
        activity_rec.activity.price 
        for day in final_output.itinerary_days 
        for activity_rec in day.activity_recommendations
    )
    if actual_total_cost != final_output.total_cost:
        raise AgentError(f"Cost mismatch: {actual_total_cost} != {final_output.total_cost}")

def eval_total_cost_is_within_budget(vacation_info: VacationInfo, final_output: TravelPlan):
    if final_output.total_cost > vacation_info.budget:
        raise AgentError(f"Over budget: {final_output.total_cost} > {vacation_info.budget}")

def eval_itinerary_events_match_actual_events(vacation_info: VacationInfo, final_output: TravelPlan):
    event_ids_missing = []
    for day in final_output.itinerary_days:
        for activity_rec in day.activity_recommendations:
            event_id = activity_rec.activity.activity_id
            reference_event = call_activity_by_id_api_mocked(event_id)
            if reference_event is None:
                event_ids_missing.append(event_id)
    
    if event_ids_missing:
        raise AgentError(f"Missing event IDs: {event_ids_missing}")

def eval_itinerary_satisfies_interests(vacation_info: VacationInfo, final_output: TravelPlan):
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

def eval_activities_and_weather_are_compatible(vacation_info: VacationInfo, final_output: TravelPlan, client=None):
    """Weather compatibility evaluation using YAML prompt"""
    if client is None:
        print("⚠️ Skipping weather compatibility evaluation")
        return
    
    # Build prompt using YAML template
    weather_prompt = prompt_manager.build_prompt("weather_compatibility")
    incompatible_activities = []
    
    for day in final_output.itinerary_days:
        for activity_rec in day.activity_recommendations:
            resp = do_chat_completion(
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
# PHASE 4: TOOLS AND REACT AGENT WITH YAML PROMPTS
# =============================================================================

def calculator_tool(input_expression) -> float:
    """Evaluates mathematical expressions"""
    return float(ne.evaluate(input_expression))

def get_activities_by_date_tool(date: str, city: str) -> List[dict]:
    """Retrieves available activities for a specific date and city from the activity database.
    
    Args:
        date (str): The date to search for activities in YYYY-MM-DD format (e.g., "2025-06-10")
        city (str): The name of the city to search in (e.g., "AgentsVille")
    
    Returns:
        List[dict]: A list of activity dictionaries containing activity details
    """
    resp = call_activities_api_mocked(date=date, city=city)
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

TRAVELER_FEEDBACK = "I want to have at least two activities per day."

class ItineraryRevisionAgent(ChatAgent):
    """ReAct agent using YAML-based prompts"""
    
    def __init__(self, vacation_info, traveler_feedback, client, model):
        # Build system prompt using YAML template
        system_prompt = prompt_manager.build_prompt(
            "itinerary_revision_agent",
            tool_descriptions=get_tool_descriptions_string(ALL_TOOLS),
            traveler_feedback=traveler_feedback,
            travelers_info=[t.name + " (interests: " + str(t.interests) + ")" for t in vacation_info.travelers],
            destination=vacation_info.destination,
            date_of_arrival=vacation_info.date_of_arrival,
            date_of_departure=vacation_info.date_of_departure,
            budget=vacation_info.budget
        )
        
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
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution using YAML-based prompts"""
    print("AgentsVille Trip Planner - Final Implementation with YAML Prompts")
    print("="*70)
    
    # Test prompt loading
    try:
        test_prompt = prompt_manager.load_prompt("itinerary_agent")
        print("✅ YAML prompt system working")
    except Exception as e:
        print(f"❌ YAML prompt system failed: {e}")
        return
    
    # Phase 1: Foundation
    vacation_info = test_vacation_info()
    if not vacation_info:
        return
    
    weather_data, activity_data = get_weather_and_activities(vacation_info)
    print("✅ Phase 1 completed")
    
    try:
        client = setup_openai_client()
        
        # Phase 2: Itinerary Agent with YAML prompts
        print("\nPhase 2: Itinerary Agent (YAML prompts)...")
        system_prompt = create_itinerary_agent_prompt(weather_data, activity_data)
        print(f"Prompt length: {len(system_prompt)} characters")
        
        agent = ItineraryAgent(system_prompt, client, MODEL)
        travel_plan = agent.get_itinerary(vacation_info)
        print("✅ Phase 2 completed")
        
        # Phase 3: Evaluation with YAML prompts
        print("\nPhase 3: Evaluation System (YAML prompts)...")
        eval_results = run_evals_tool(travel_plan, vacation_info, client)
        print(f"Evaluation: {eval_results}")
        print("✅ Phase 3 completed")
        
        # Phase 4: ReAct Agent with YAML prompts
        print("\nPhase 4: ReAct Agent (YAML prompts)...")
        react_agent = ItineraryRevisionAgent(vacation_info, TRAVELER_FEEDBACK, client, MODEL)
        revised_plan = react_agent.run_react_cycle(travel_plan, max_steps=15)
        
        # Phase 5: Final validation
        print("\nPhase 5: Final Validation...")
        final_results = run_evals_tool(revised_plan, vacation_info, client)
        
        success = final_results['success']
        print(f"Final Status: {'✅ SUCCESS' if success else '❌ FAILED'}")
        
        if success:
            print("\n🎉 All phases completed successfully with YAML prompts!")
            print("✅ Ready for notebook transfer!")
        else:
            print(f"Issues: {final_results['failures']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()