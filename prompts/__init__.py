"""
Prompts module for Blueprint Agent System

This module provides easy access to all prompts used in the system.
"""

import os


def _load_prompt_from_file(filename: str) -> str:
    """Load a prompt from a text file."""
    try:
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Remove the r""" wrapper if present
            if content.startswith('r"""') and content.endswith('"""'):
                return content[4:-3].strip()
            return content.strip()
    except Exception as e:
        print(f"Warning: Could not load prompt from {filename}: {e}")
        return ""


# Load all prompts from text files
GENERATE_BLUEPRINT = _load_prompt_from_file("prompt_generate_blueprint.txt")
REFINE_BLUEPRINT = _load_prompt_from_file("prompt_identify_nontrivial.txt")
FIX_BLUEPRINT_FORMAT = _load_prompt_from_file("prompt_fix_blueprint_format.txt")

# Create a dictionary for easy access
PROMPTS = {
    "generate_blueprint": GENERATE_BLUEPRINT,
}

# Export the main prompts as module attributes
__all__ = [
    "GENERATE_BLUEPRINT",
    "REFINE_BLUEPRINT",
    "FIX_BLUEPRINT_FORMAT",
    "PROMPTS"
]
