"""
Simple prompt loader for YAML-based prompts.
Extremely lean implementation for loading prompts from prompts/ directory.
"""

import yaml
from pathlib import Path
from typing import Dict, Any


def load_prompt(prompt_name: str, **template_vars) -> str:
    """
    Load a prompt from the prompts/ directory and format it with template variables.
    
    Args:
        prompt_name: Name of the prompt file (without .yaml extension)
        **template_vars: Variables to substitute in the prompt template
        
    Returns:
        Formatted prompt string
    """
    prompt_file = Path("prompts") / f"{prompt_name}.yaml"
    
    with open(prompt_file, 'r') as f:
        prompt_data = yaml.safe_load(f)
    
    # Build the prompt string
    prompt_parts = []
    
    # Add role if present
    if 'role' in prompt_data:
        prompt_parts.append(prompt_data['role'].strip())
    
    # Add task if present  
    if 'task' in prompt_data:
        prompt_parts.append("\n## Task\n")
        prompt_parts.append(prompt_data['task'].strip())
    
    # Add available tools template if present
    if 'available_tools_template' in prompt_data:
        prompt_parts.append("\n")
        prompt_parts.append(prompt_data['available_tools_template'].strip())
    
    # Add output format if present
    if 'output_format' in prompt_data:
        prompt_parts.append("\n## Output Format\n")
        prompt_parts.append(prompt_data['output_format'].strip())
    
    # Add context template if present
    if 'context_template' in prompt_data:
        prompt_parts.append("\n")
        prompt_parts.append(prompt_data['context_template'].strip())
    
    # Add react cycle if present
    if 'react_cycle' in prompt_data:
        prompt_parts.append("\n")
        prompt_parts.append(prompt_data['react_cycle'].strip())
    
    # Add instructions if present
    if 'instructions' in prompt_data:
        prompt_parts.append("\n")
        prompt_parts.append(prompt_data['instructions'].strip())
    
    # Join all parts
    prompt = "".join(prompt_parts)
    
    # Format with template variables
    if template_vars:
        prompt = prompt.format(**template_vars)
    
    return prompt


# Convenience functions for each prompt type
def load_itinerary_agent_prompt(**template_vars) -> str:
    """Load the itinerary agent prompt."""
    return load_prompt("itinerary_agent", **template_vars)


def load_itinerary_revision_agent_prompt(**template_vars) -> str:
    """Load the itinerary revision agent prompt.""" 
    return load_prompt("itinerary_revision_agent", **template_vars)


def load_traveler_feedback_evaluator_prompt(**template_vars) -> str:
    """Load the traveler feedback evaluator prompt."""
    return load_prompt("traveler_feedback_evaluator", **template_vars)


def load_weather_compatibility_prompt(**template_vars) -> str:
    """Load the weather compatibility prompt."""
    return load_prompt("weather_compatibility", **template_vars)