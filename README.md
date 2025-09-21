# Blueprint Agent

A Python agent for generating structured LaTeX blueprints of mathematical proofs. Supports multiple AI providers and is easily extensible.

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Usage

```python
from agents import BlueprintGeneratorAgent

# Initialize agent
agent = BlueprintGeneratorAgent()

# Generate blueprint
response = agent.generate_blueprint(
    statement="The theorem's name and other requirements",
    pdf_files=["path/to/document.pdf"],
    reference_urls=["https://example.com"],
    refine_times=2
)

# Get conversation history
history = agent.get_history()
```

## Project Structure

```
blueprint-agent/
├── agents/                    # Agent implementations
│   └── blueprint_generator.py
├── kernel/                    # Core functionality
│   ├── base_agent.py
│   ├── llm_providers.py
│   └── message.py
├── prompts/                   # AI prompts
│   ├── prompt_generate_blueprint.txt
│   ├── prompt_identify_nontrivial.txt
│   └── prompt_fix_blueprint_format.txt
├── usage_example.py          # Usage example
└── requirements.txt
```

## Features

- Generate structured LaTeX proof blueprints
- Support for PDF file analysis
- Reference URL integration
- Multi-step refinement process
- Non-trivial statement identification
- LaTeX format fixing
- Extensible AI provider support (currently Google Gemini, easily add others)
