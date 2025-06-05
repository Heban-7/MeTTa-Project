# scripts/write_to_file : writes original gene fields + summary to a text file

import os, sys
import csv
from datetime import datetime

# get working directory
sys.path.append(os.path.abspath('..'))
from .call_llm import call_llm

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


def write_to_file(field_expression, summary_atom, file_path_atom, format='text'):
    """
    Writes the original fields + LLM summary to a file in specified format.
    Arguments:
      - field_expression: a Python list of Atoms (same as above).
      - summary_atom: a Python string (the summary from call_llm).
      - file_path_atom: a Python string (path where to write).
      - format_type: str, either "text" or "csv" (default: "text")
      
    Behavior:
          ==== Gene: <GID> ===
          <Original fields...>
          --- Summary from LLM ---
          <Summary text>
    """
    try:
        # Sanity-check types
        if not isinstance(field_expression, list):
            raise TypeError("write_to_file: expected a list of atoms as first arg, got %r" % (field_expression,))
        if not isinstance(summary_atom, str):
            raise TypeError("write_to_file: expected summary (str) as second arg, got %r" % (summary_atom,))
        if not isinstance(file_path_atom, str):
            raise TypeError("write_to_file: expected file path (str) as third arg, got %r" % (file_path_atom,))
        
        # Convert fields → lines
        lines = [str(atom) for atom in field_expression]
        gene_id = lines[0] if len(lines) > 0 else "UnknownGene"
        
        # Ensure output directory exists
        out_path = os.path.abspath(file_path_atom)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        # Build text format content
        block = []
        block.append(f"=== Gene: {gene_id} ====")
        block.extend(lines)
        block.append("--- Summary from LLM ---")
        block.append(summary_atom)
        block.append("")  # blank line
        
        # Append to file
        try:
            with open(out_path, "a", encoding="utf-8") as f:
                f.write("\n".join(block) + "\n")
            print(f"Successfully wrote summary for gene {gene_id} to {out_path}")
        except IOError as e:
            print(f"Error writing to file {out_path}: {str(e)}", file=sys.stderr)
            raise
            
    except Exception as e:
        print(f"Error in write_to_file: {str(e)}", file=sys.stderr)
        raise
        

