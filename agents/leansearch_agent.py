"""
LeanSearch Agent

Responsible for searching Lean4 mathematical content using Lean Explore API,
with intelligent query generation and result analysis.
"""

import json
from typing import List, Optional, Any, Dict, Tuple
from datetime import datetime

from kernel import BaseAgent, GeminiProvider
import prompts

from lean_explore.api.client import Client
from lean_explore.cli import config_utils


class LeanSearchAgent(BaseAgent):
    """Agent specialized in searching Lean4 mathematical content using Lean Explore."""
    
    def __init__(self, 
                 llm_provider: GeminiProvider = None, 
                 agent_id: str = "LeanSearchAgent",
                 lean_api_key: str = None):
        """
        Initialize LeanSearch Agent.
        
        Args:
            llm_provider: LLM provider instance
            agent_id: Unique identifier for the agent
            lean_api_key: Lean Explore API key. If None, will try to load from config
        """
        if llm_provider is None:
            llm_provider = GeminiProvider()
        super().__init__(llm_provider=llm_provider, agent_id=agent_id, system_prompt=None)
        
        # Initialize Lean Explore client
        try:
            if lean_api_key:
                self.lean_client = Client(api_key=lean_api_key)
            else:
                self.lean_client = Client(api_key=config_utils.load_api_key())
        except Exception as e:
            print(f"Warning: Could not initialize Lean Explore client: {e}")
            self.lean_client = None
    
    def generate_search_query(self, user_query: str) -> str:
        """
        Generate a search query from user input using LLM.
        
        Args:
            user_query: The user's mathematical question or statement
            
        Returns:
            Generated search query string, or "NO_SEARCH" if no search needed
        """
        prompt = f"{prompts.CREATE_LEANSEARCH_QUERY}\n\nUser query: {user_query}"
        response = self.send_message(prompt)
        return response.strip()
    
    def analyze_search_results(self, 
                             user_query: str, 
                             search_query: str, 
                             search_results: List[Any]) -> str:
        """
        Analyze search results and identify relevant theorems and cover matches.
        
        Args:
            user_query: Original user query
            search_query: Search query that was used
            search_results: List of search results from Lean Explore
            
        Returns:
            Formatted analysis of the search results
        """
        # Format search results for analysis
        search_results_text = f"Search Query: {search_query}\n"
        search_results_text += f"Total Found: {len(search_results)} results\n\n"
        
        search_results_text += f"SEARCH RESULTS ({len(search_results)} total):\n"
        for i, item in enumerate(search_results, 1):
            search_results_text += f"\n{i}. {item.primary_declaration.lean_name if item.primary_declaration else 'N/A'}\n"
            search_results_text += f"   File: {item.source_file}:{item.range_start_line}\n"
            if item.display_statement_text:
                search_results_text += f"   Statement: {item.display_statement_text}\n"
            if item.docstring:
                search_results_text += f"   Docstring: {item.docstring}\n"
            if item.informal_description:
                search_results_text += f"   Description: {item.informal_description}\n"
        
        # Create analysis prompt
        analysis_prompt = prompts.IDENTIFY_LEANSEARCH_RESULT
        analysis_prompt += "\n\n"
        analysis_prompt += f"**User Query**: {user_query}\n"
        analysis_prompt += f"**Search Query**: {search_query}\n\n"
        analysis_prompt += "**Search Results**:\n"
        analysis_prompt += search_results_text
        analysis_prompt += "\n\nPlease analyze these results and provide your response in the specified format."
        
        response = self.send_message(analysis_prompt)
        return response
    
    async def search_lean_explore(self, query: str, limit: int = 50) -> List[Any]:
        """
        Search Lean Explore with the given query.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of search results
        """
        if not self.lean_client:
            raise RuntimeError("Lean Explore client not available. Please check your API key.")
        
        try:
            search_response = await self.lean_client.search(query=query)
            return search_response.results[:limit]
        except Exception as e:
            print(f"Error searching Lean Explore: {e}")
            return []
    
    async def search(self, 
               user_query: str, 
               limit: int = 50,
               log_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Complete search workflow: generate query, search, and analyze results.
        
        Args:
            user_query: The user's mathematical question or statement
            limit: Maximum number of search results to return
            log_file: Optional file path to log the search process
            
        Returns:
            Dictionary containing search results and analysis
        """
        if log_file:
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(f"Lean Search Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"User Query: {user_query}\n")
                f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 40 + "\n")
        
        # Stage 1: Generate search query
        print("📝 Stage 1: Generating search query...")
        search_query = self.generate_search_query(user_query)
        
        if log_file:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"Search Query: {search_query}\n")
        
        if search_query == "NO_SEARCH":
            print("❌ No search needed for this query")
            result = {
                "user_query": user_query,
                "search_query": "NO_SEARCH",
                "search_results": [],
                "analysis": "No search needed for this query",
                "cover_match": None
            }
            if log_file:
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write("Result: No search needed\n\n")
            return result
        
        print(f"🔍 Generated search query: {search_query}")
        
        # Stage 2: Perform search
        print("🔍 Stage 2: Searching Lean Explore...")
        search_results = await self.search_lean_explore(search_query, limit)
        
        print(f"📊 Found {len(search_results)} results")
        
        if log_file:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"Search Results: {len(search_results)} found\n")
        
        # Stage 3: Analyze results
        print("🧠 Stage 3: Analyzing results...")
        analysis = self.analyze_search_results(user_query, search_query, search_results)
        
        print("🤖 Analysis complete!")
        
        if log_file:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write("Final Response:\n")
                f.write(analysis)
                f.write("\n\n" + "=" * 60 + "\n\n")
        
        # Extract cover match from analysis (simple parsing)
        cover_match = None
        if "Cover match" in analysis:
            lines = analysis.split('\n')
            for line in lines:
                if "Cover match" in line and ":" in line:
                    cover_match = line.split(":")[1].strip()
                    if cover_match == "None":
                        cover_match = None
                    break
        
        result = {
            "user_query": user_query,
            "search_query": search_query,
            "search_results": search_results,
            "analysis": analysis,
            "cover_match": cover_match
        }
        
        return result
    
    
    def get_lean_client_status(self) -> Dict[str, Any]:
        """
        Get the status of the Lean Explore client.
        
        Returns:
            Dictionary with client status information
        """
        return {
            "client_initialized": self.lean_client is not None,
            "agent_id": self.agent_id
        }
