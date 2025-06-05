import os
import sys
import importlib.util
from dotenv import load_dotenv, find_dotenv

def check_module_import(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def main():
    # Print Python version and path
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Check .env file
    env_path = os.path.join(os.getcwd(), '.env')
    print(f".env file location: {env_path}")
    print(f"API_KEY present: {bool(os.getenv('API_KEY'))}")
    print(f"MODEL_NAME present: {bool(os.getenv('MODEL_NAME'))}")
    
    # Check module imports
    print(f"OpenAI module imported successfully: {check_module_import('openai')}")
    print(f"Hyperon module imported successfully: {check_module_import('hyperon')}")
    
    # Check if scripts directory is in path
    scripts_dir = os.path.join(os.getcwd(), 'scripts')
    print(f"Scripts directory in path: {scripts_dir in sys.path}")
    
    # Add scripts directory to path if not present
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
        print("Added scripts directory to Python path")
    
    # Try importing from scripts
    try:
        from scripts.call_llm import call_llm
        from scripts.write_to_file import write_to_file
        print("Successfully imported functions from scripts directory")
    except ImportError as e:
        print(f"Error importing from scripts: {e}")

if __name__ == "__main__":
    main() 