# MeTTa ↔ LLM Summarization Project

A powerful integration between MeTTa (a declarative/functional knowledge-graph DSL) and Large Language Models (LLMs) for intelligent gene data summarization.

## Overview

This project demonstrates how to combine the structured data processing capabilities of MeTTa with the natural language understanding of LLMs to create meaningful summaries of gene data. The system:

1. **Loads** raw gene atoms from `data/nodes.metta`
2. **Extracts** key fields for each gene (ID, name, type, chr, start, end, synonyms)
3. **Sends** those fields to an LLM for intelligent summarization
4. **Writes** both the original fields and the LLM's summary into `output/summaries.txt`

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (for LLM integration)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MeTTa-Project.git
cd MeTTa-Project
```

2. Create and activate a virtual environment:
```bash
python -m venv MeTTavenv
source MeTTavenv/bin/activate  # On Windows: MeTTavenv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Project Structure

```
MeTTa-Project/
├── data/               # Contains input gene data
│   └── nodes.metta    # Raw gene atoms
├── scripts/           # Python implementation
│   ├── call_llm.py    # LLM integration
│   └── write_to_file.py # Output handling
├── output/            # Generated summaries
│   ├── llm_operations.py    # LLM integratio
│   └── main.metta  # MeTTa integration for all 
├── requirements.txt   # Project dependencies
└── README.md         # This file
```

## Usage

1. Ensure your gene data is properly formatted in `data/nodes.metta`
2. Run the summarization script:
```bash
metta src/main.metta
```

The summaries will be generated in `output/summaries.txt`.

## Dependencies

- `hyperon`: MeTTa implementation
- `openai`: OpenAI API client
- `python-dotenv`: Environment variable management

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

