# scripts/call_llm.py : calls LLM to summarize a list of gene fields

import os
import sys
import openai
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Load environment variables
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

API_KEY=os.getenv("API_KEY")
MODEL_NAME=os.getenv("MODEL_NAME")

client=OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

def assemble_text_from_fields(field_atoms):
    """
    Assembles text from a list of field atoms.
    Args:
        field_atoms (list): List of field atoms containing gene information
        field_atoms is a Python list of hyperon.atoms.Atom objects (Symbol, Expression, etc.)

    Returns:
        str: Concatenated text from all field atoms
    """
    try:
        # Convert each atom to string and format it nicely
        field_names = ["Gene ID", "Gene Name", "Type", "Chromosome", "Start", "End", "Synonyms"]
        formatted_fields = []
        
        for i, atom in enumerate(field_atoms):
            field_name = field_names[i] if i < len(field_names) else f"Field {i}"
            field_value = str(atom)
            formatted_fields.append(f"{field_name}: {field_value}")
        
        return "\n".join(formatted_fields)
    except Exception as e:
        print(f"Error in assemble_text_from_fields: {str(e)}", file=sys.stderr)
        return str(field_atoms)  # Fallback to simple string representation

def call_llm(field_expression):
    """
    This function is wrapped by an OperationAtom and will be called from MeTTa.
    Args:
        field_expression: a hyperon Expression, e.g. (list "ENSG…" "SFN" "protein_coding" "chr1" "26863149" "26864456" "(synonym1 synonym2 …)")
    Returns:
        A hyperon Symbol (String) containing the summary text.
    """
    try:
        # Check if API is configured
        if not client:
            return "Error: API_KEY environment variable is not set. Please set it in .env file"

        # Extract the python list of atoms from the Metta Expression
        if not isinstance(field_expression, list):
            raise TypeError("call_llm expects a list of atoms, got: %r" % (field_expression,))
        
        # Turn that list of Atoms into a prompt text
        prompt_text = assemble_text_from_fields(field_expression)
        
        # Call the OpenAI API to get a summary
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful assistant specialized in summarizing gene information. "
                            "Given the following gene information, produce a concise short summary"
                            "highlighting the gene ID, gene name, type, location, and any notable synonyms. "
                            "Format the summary in a clear, scientific manner."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt_text
                    }
                ],
                temperature=0.0,
                max_tokens=150
            )
            summary_text = response.choices[0].message.content.strip()
            
            if not summary_text:
                raise ValueError("Received empty summary from LLM")
                
            return summary_text
            
        except Exception as e:
            raise RuntimeError(f"Error calling LLM API: {str(e)}")
            
    except Exception as e:
        # Log the error and return a fallback message
        print(f"Error in call_llm: {str(e)}", file=sys.stderr)
        return f"Error generating summary: {str(e)}"