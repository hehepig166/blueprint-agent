# LeanSearch Agent

A specialized agent for searching Lean4 mathematical content using the Lean Explore API.

## Features

- **Smart Query Generation**: Uses LLM to convert mathematical questions into effective search queries
- **Lean Explore Integration**: Direct search in Lean4 mathematical library
- **Result Analysis**: Intelligent analysis of search results to identify relevant theorems and cover matches
- **Interactive Usage**: Supports interactive query mode with detailed logging

## Quick Start

### Basic Usage

```python
from agents import LeanSearchAgent
from kernel import GeminiProvider
import asyncio

# Initialize
llm_provider = GeminiProvider(api_key="your_gemini_api_key")
search_agent = LeanSearchAgent(llm_provider=llm_provider)

# Search
async def search_example():
    result = await search_agent.search("prove that 1+1=2", limit=10)
    print(f"Search query: {result['search_query']}")
    print(f"Results found: {len(result['search_results'])}")
    print(f"Cover match: {result['cover_match']}")

asyncio.run(search_example())
```

### Interactive Mode

Run the example script for interactive searching:

```bash
python example_leansearch_usage.py
```

## example_leansearch_usage.py Usage

This script demonstrates the full functionality of LeanSearch Agent.

### How to Use

1. **Run the script**:
   ```bash
   python example_leansearch_usage.py
   ```

2. **Enter API key**: Input your Gemini API key when prompted

3. **Ask questions**: Enter mathematical queries like:
   - "What is the fundamental theorem of calculus?"
   - "prove that 1+1=2"
   - "group axioms"
   - "prove (a + b)/2 ≥ √(ab)"

4. **View results**: The script displays:
   - Generated search query
   - Number of results found
   - Detailed search results
   - Cover match analysis
   - Complete analysis report

5. **Exit**: Type 'quit', 'exit' or 'q' to exit

### Logging

The script automatically creates detailed log files:
- **Session log**: `logs/leansearch_session_YYYYMMDD_HHMMSS.log`
- **Query logs**: `logs/query_N_YYYYMMDD_HHMMSS.log`

Each query generates a separate log file with complete search process and analysis.

## Configuration

### Required
- **Gemini API key**: For LLM query generation and result analysis
- **Lean Explore API key**: For actual Lean4 library search (mandatory for full functionality)

### Setup Lean Explore

1. **Install Lean Explore**:
   ```bash
   pip install lean-explore
   ```

2. **Get API key**: Visit [Lean Explore](https://www.leanexplore.com) to get your API key

3. **Configure API key** (choose one method):
   
   **Method 1: Environment variable**
   ```bash
   export LEAN_EXPLORE_API_KEY="your_api_key_here"
   ```
   
   **Method 2: Pass directly to agent**
   ```python
   search_agent = LeanSearchAgent(
       llm_provider=llm_provider,
       lean_api_key="your_api_key_here"
   )
   ```

### Dependencies
```bash
pip install -r requirements.txt
```

## Notes

- Queries should be mathematical questions or statements
- Non-mathematical queries (like greetings) will be identified as "NO_SEARCH"
- Search result quality depends on query accuracy and Lean4 library coverage

## Example Results

```

==================================================
Session started at: 2025-09-30 10:00:28
==================================================


--- Query #1 ---
Time: 2025-09-30 10:00:34
User Query: hello, who are you
Query Log File: logs/query_1_20250930_100034.log
Generated Search Query: NO_SEARCH
Result: Identified as non-mathematical query

--- Query #2 ---
Time: 2025-09-30 10:00:45
User Query: ⊢ (Nat.digits 10 a).length ≤ (Nat.digits 10 b).length
Query Log File: logs/query_2_20250930_100045.log
Generated Search Query: inequality involving the length of base 10 digits for natural numbers a and b where (Nat.digits 10 a).length ≤ (Nat.digits 10 b).length
Search Results: 50 found
Cover Match: `Nat.le_digits_len_le`
Analysis: Cover match found - `Nat.le_digits_len_le`

--- Query #3 ---
Time: 2025-09-30 10:01:17
User Query: SimpleGraph iscycle
Query Log File: logs/query_3_20250930_100117.log
Generated Search Query: SimpleGraph and the property of `isCycle` within graph theory, including cycle detection and definitions
Search Results: 50 found
Cover Match: `SimpleGraph.Walk.IsCycle`
Analysis: Cover match found - `SimpleGraph.Walk.IsCycle`

--- Query #4 ---
Time: 2025-09-30 10:01:50
User Query: A convergent sequence is bounded.
Query Log File: logs/query_4_20250930_100150.log
Generated Search Query: convergent sequence is bounded in real analysis and topology
Search Results: 50 found
Cover Match: `Metric.isBounded_range_of_tendsto`
Analysis: Cover match found - `Metric.isBounded_range_of_tendsto`

==================================================
Session ended at: 2025-09-30 10:02:41
Total queries processed: 4
==================================================

```