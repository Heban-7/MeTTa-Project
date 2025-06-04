# scripts/call_llm.py : calls LLM to summarize a list of gene fields

import os
import openai
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

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
    textual_fields = [str(atom) for atom in field_atoms]
    
    return "\n".join(textual_fields) # for readability, put each field on its own line

def call_llm(field_expression, file_path_atom=None):
    """
    This function is wrapped by an OperationAtom and will be called from MeTTa.
    Args:
        field_expression: a hyperon Expression, e.g. (list "ENSG…" "SFN" "protein_coding" "chr1" "26863149" "26864456" "(synonym1 synonym2 …)")
        file_path_atom: appends the summary to that file (not strictly needed here).
    Returns:
        A hyperon Symbol (String) containing the summary text.
    """
    

    # Extract the python list of atoms from the Metta Expression
    if not isinstance(field_expression, list):
        # Just ensure we have a list
        raise TypeError("call_llm expects a list of atoms, got: %r" % (field_expression,))
    
    # Turn that list of Atoms into a prompt text
    prompt_text = assemble_text_from_fields(field_expression)
    
    # Call the OpenAI API to get a summary
    response = client.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant specialized in summarizing gene information. "
                    "Given the following lines (each line is one field about a gene), "
                    "produce a concise summary (2–3 sentences) highlighting the gene ID, gene name, type, location, and any notable synonyms."
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
    
    # Return the summary as a MeTTa‐grounded string atom. In Hyperon/MeTTa, Python strings are automatically “grounded” into MeTTa atoms.
    return summary_text