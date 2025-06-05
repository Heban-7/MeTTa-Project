# src/llm_ops.py
# Defines two Python‐grounded atoms for MeTTa:
#   1. scripts/call_llm      : calls OpenAI to summarize a list of gene fields
#   2. scripts/write_to_file : writes original gene fields + summary to a text file

import os, sys
from hyperon.ext import register_atoms
from hyperon.atoms import OperationAtom, S

# Add the project root directory and scripts directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scripts_dir = os.path.join(project_root, 'scripts')
sys.path.insert(0, project_root)
sys.path.insert(0, scripts_dir)

# Debug: Print Python path
print("Python path:", sys.path)

from scripts.call_llm import call_llm
from scripts.write_to_file import write_to_file


@register_atoms(pass_metta=True)
def llm_ops(metta):
    """
    This function is invoked by MeTTa at startup.  It should return a dict of
    { "registered_atom_name": OperationAtom(...) } mappings.  MeTTa uses this
    to know "call_llm" and "write_to_file" as valid operations.
    """

    call_llm_atom = OperationAtom(
        "call_llm",
        lambda afield_list: call_llm(afield_list),  
        # Type signature: expect an Expression (Python list) → return a String atom
        ["Expression"], 
        unwrap=True  # MeTTa will pass a Python list of Atoms to us
    )

    write_to_file_atom = OperationAtom(
        "write_to_file",
        lambda afield_list, asummary, afilepath, aformat: write_to_file(afield_list, asummary, afilepath, aformat),
        # Type signature: [Expression, String, String, String]
        ["Expression", "String", "String", "String"],
        unwrap=True
    )

    return {
        "call_llm": call_llm_atom,
        "write_to_file": write_to_file_atom
    }

