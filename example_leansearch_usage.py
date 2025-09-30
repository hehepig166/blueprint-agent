"""
Example usage of LeanSearchAgent

This script demonstrates how to use the LeanSearchAgent to search for
mathematical content in Lean4 using the Lean Explore API.
"""

import os
import asyncio
from datetime import datetime
from agents import LeanSearchAgent
from kernel import GeminiProvider, OpenAIProvider


async def main():
    """Main function demonstrating LeanSearchAgent usage."""
    
    # Setup logging directory
    os.makedirs("logs", exist_ok=True)
    session_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_log_file = f"logs/leansearch_session_{session_timestamp}.log"
    print(f"📝 Session logging to: {session_log_file}")
    
    # Get API key from environment variable
    # api_key = os.getenv("GEMINI_API_KEY")
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = "https://openrouter.ai/api/v1"
    
    if not api_key:
        print("❌ API key cannot be empty")
        return
    
    # Initialize the agent
    print("🚀 Initializing LeanSearchAgent...")
    # llm_provider = GeminiProvider(api_key=api_key)
    llm_provider = OpenAIProvider(api_key=api_key, base_url=base_url)
    search_agent = LeanSearchAgent(llm_provider=llm_provider)
    
    # Check client status
    status = search_agent.get_lean_client_status()
    print(f"📊 Client Status: {status}")
    
    if not status["client_initialized"]:
        print("⚠️ Lean Explore client not initialized. Please check your Lean API key.")
        print("   You can still test query generation without actual search.")
    
    print("\n🔍 LeanSearchAgent Interactive Mode")
    print("=" * 50)
    print("Enter your mathematical queries (type 'quit' to exit)")
    
    # Write session start to log
    with open(session_log_file, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Session started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*50}\n\n")
    
    query_count = 0
    while True:
        print("\n" + "-" * 30)
        query = input("📝 Enter your query: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            # Write session end to log
            with open(session_log_file, "a", encoding="utf-8") as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"Session ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total queries processed: {query_count}\n")
                f.write(f"{'='*50}\n")
            break
            
        if not query:
            print("⚠️ Please enter a valid query")
            continue
        
        query_count += 1
        print(f"\n🔍 Processing: {query}")
        
        # Create individual query log file
        query_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_log_file = f"logs/query_{query_count}_{query_timestamp}.log"
        print(f"📝 Query logging to: {query_log_file}")
        
        # Log query start to both session and query logs
        with open(session_log_file, "a", encoding="utf-8") as f:
            f.write(f"\n--- Query #{query_count} ---\n")
            f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"User Query: {query}\n")
            f.write(f"Query Log File: {query_log_file}\n")
        
        with open(query_log_file, "w", encoding="utf-8") as f:
            f.write(f"Query #{query_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*50}\n")
            f.write(f"User Query: {query}\n")
            f.write(f"{'='*50}\n\n")
        
        try:
            # Test query generation first
            search_query = search_agent.generate_search_query(query)
            print(f"🔍 Generated search query: {search_query}")
            
            # Log generated query to both logs
            with open(session_log_file, "a", encoding="utf-8") as f:
                f.write(f"Generated Search Query: {search_query}\n")
            
            with open(query_log_file, "a", encoding="utf-8") as f:
                f.write(f"Generated Search Query: {search_query}\n\n")
            
            if search_query == "NO_SEARCH":
                print("✅ Correctly identified as non-mathematical query")
                with open(session_log_file, "a", encoding="utf-8") as f:
                    f.write("Result: Identified as non-mathematical query\n")
                with open(query_log_file, "a", encoding="utf-8") as f:
                    f.write("Result: Identified as non-mathematical query\n")
                continue
            
            # If we have a valid search query and client is available, perform full search
            if status["client_initialized"]:
                print("🔍 Performing full search...")
                result = await search_agent.search(query, limit=50, log_file=query_log_file)
                
                print("📊 Search Results:")
                print(f"   - Found {len(result['search_results'])} results")
                print(f"   - Cover match: {result['cover_match']}")
                
                # Print all search results in detail
                print("\n📋 Detailed Search Results:")
                for i, search_result in enumerate(result['search_results'], 1):
                    print(f"\n--- Result {i} ---")
                    print(f"Lean Name: {search_result.primary_declaration.lean_name if search_result.primary_declaration else 'N/A'}")
                    print(f"File: {search_result.source_file}:{search_result.range_start_line}")
                    if search_result.display_statement_text:
                        print(f"Statement: {search_result.display_statement_text}")
                    if search_result.docstring:
                        print(f"Docstring: {search_result.docstring}")
                    if search_result.informal_description:
                        print(f"Description: {search_result.informal_description}")
                
                # Log search results summary to session log (only cover match)
                with open(session_log_file, "a", encoding="utf-8") as f:
                    f.write(f"Search Results: {len(result['search_results'])} found\n")
                    f.write(f"Cover Match: {result['cover_match']}\n")
                
                with open(query_log_file, "a", encoding="utf-8") as f:
                    f.write(f"\nDetailed Search Results ({len(result['search_results'])} found):\n")
                    f.write(f"Cover Match: {result['cover_match']}\n")
                    for i, search_result in enumerate(result['search_results'], 1):
                        f.write(f"\n--- Result {i} ---\n")
                        f.write(f"Lean Name: {search_result.primary_declaration.lean_name if search_result.primary_declaration else 'N/A'}\n")
                        f.write(f"File: {search_result.source_file}:{search_result.range_start_line}\n")
                        if search_result.display_statement_text:
                            f.write(f"Statement: {search_result.display_statement_text}\n")
                        if search_result.docstring:
                            f.write(f"Docstring: {search_result.docstring}\n")
                        if search_result.informal_description:
                            f.write(f"Description: {search_result.informal_description}\n")
                
                # Print full analysis
                print("\n📝 Full Analysis:")
                print(result['analysis'])
                
                # Log analysis summary to session log (only cover match info)
                with open(session_log_file, "a", encoding="utf-8") as f:
                    f.write(f"Analysis: Cover match found - {result['cover_match']}\n")
                
                with open(query_log_file, "a", encoding="utf-8") as f:
                    f.write(f"\nFull Analysis:\n{result['analysis']}\n")
            else:
                print("⚠️ Skipping full search (Lean client not available)")
                with open(session_log_file, "a", encoding="utf-8") as f:
                    f.write("Result: Skipped (Lean client not available)\n")
                with open(query_log_file, "a", encoding="utf-8") as f:
                    f.write("Result: Skipped (Lean client not available)\n")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            with open(session_log_file, "a", encoding="utf-8") as f:
                f.write(f"Error: {e}\n")
            with open(query_log_file, "a", encoding="utf-8") as f:
                f.write(f"Error: {e}\n")
    
    print("\n✅ Session complete!")


if __name__ == "__main__":
    print("🧪 LeanSearchAgent Example Usage")
    print("=" * 40)
    
    # Run main example
    asyncio.run(main())
    
    print("\n🎉 All examples completed!")
