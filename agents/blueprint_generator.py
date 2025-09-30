"""
Blueprint Generator Agent

Responsible for generating Lean4 blueprints from mathematical statements,
with support for PDF attachments and reference URLs.
"""

import sys
import os
from typing import List, Optional, Any, Dict

from kernel import BaseAgent, GeminiProvider
import prompts
from google.genai import types


class BlueprintGeneratorAgent(BaseAgent):
    """Agent specialized in generating Lean4 blueprints from mathematical statements."""
    
    def __init__(self, llm_provider: GeminiProvider = None, agent_id: str = "BlueprintGenerator"):
        """
        Initialize Blueprint Generator Agent.
        
        Args:
            llm_provider: LLM provider instance
            agent_id: Unique identifier for the agent
        """
        if llm_provider is None:
            llm_provider = GeminiProvider()
        super().__init__(llm_provider=llm_provider, agent_id=agent_id, system_prompt=None)
    
    def generate_original_blueprint(self, 
                          statement: str, 
                          pdf_files: Optional[List[str]] = None,
                          reference_urls: Optional[List[str]] = None,
                          additional_context: Optional[str] = None) -> str:
        """
        Generate an original Lean4 blueprint from a mathematical statement.
        
        Args:
            statement: The mathematical statement to prove
            pdf_files: List of PDF file paths to analyze
            reference_urls: List of reference URLs to consider
            additional_context: Additional context or constraints
            
        Returns:
            Generated blueprint as LaTeX string
        """      

        # Upload files
        uploaded_files = []
        if pdf_files:
            for pdf_file in pdf_files:
                file_obj = self.upload_file(pdf_file)
                uploaded_files.append(pdf_file)  

        # Build the complete message with prompt and statement
        prompt = prompts.GENERATE_BLUEPRINT
        prompt += f"\nTheorem statement:\n{statement}\n"

        # Add reference URLs if provided
        if reference_urls:
            prompt += "\nReference URLs:"
            for url in reference_urls:
                prompt += f"\n- {url}"
            prompt += "\n"

        # Add additional context if provided
        if additional_context:
            prompt += f"\nAdditional context:\n{additional_context}"

        # Add attached files if provided
        if uploaded_files:
            prompt += "\nReference files:"
            for file in uploaded_files:
                prompt += f"\n- {file}"
            prompt += "\n"
        
        # Configure for web search
        config = types.GenerateContentConfig(
            tools=[
                {"url_context": {}},
                {"google_search": {}},
            ]
        )

        # Send the complete message as a list with web search config
        # response = self.generate_content(message_parts, config=config)
        response = self.send_message(prompt, config=config)
        
        return response
    
    def refine_blueprint(self) -> str:
        prompt = prompts.REFINE_BLUEPRINT
        response = self.send_message(prompt)
        prompt = "Now refine, split these lemmas / theorems, and make them more detailed. Output the refined blueprint directly."
        response = self.send_message(prompt)
        return response
    
    def fix_format(self) -> str:
        prompt = prompts.FIX_BLUEPRINT_FORMAT
        response = self.send_message(prompt)
        return response

    def analyze_statement_complexity(self, statement: str) -> Dict[str, Any]:
        """
        Analyze the complexity of a mathematical statement.
        
        Args:
            statement: The mathematical statement to analyze
            
        Returns:
            Dictionary with complexity analysis
        """
        # TODO: Implement complexity analysis
        # 1. Send statement to LLM for analysis
        # 2. Parse response into structured format
        # 3. Return analysis dictionary with:
        #    - difficulty_level
        #    - estimated_lemmas
        #    - key_concepts
        #    - challenges
        #    - proof_strategy
        pass

    def generate_blueprint(self, 
                          statement: str,
                          refine_times: int = 1,
                          pdf_files: Optional[List[str]] = None,
                          reference_urls: Optional[List[str]] = None,
                          additional_context: Optional[str] = None) -> str:
        """
        Generate a Lean4 blueprint from a mathematical statement.

        pipeline:
        1. Generate an original blueprint
        2. Refine the blueprint
        3. Fix the format of the blueprint
        4. Return the refined blueprint
        """
        self.generate_original_blueprint(statement, pdf_files, reference_urls, additional_context)
        for _ in range(refine_times):
            refined_blueprint = self.refine_blueprint()
        fixed_blueprint = self.fix_format()
        return fixed_blueprint