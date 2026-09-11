
import sys
import os

def verify_environment():
    print("=" * 50)
    print("AI RESUME ANALYZER - ENVIRONMENT VERIFICATION")
    print("=" * 50)
    
    # Check Python Executable Path
    python_exe = sys.executable
    print(f"Python Executable : {python_exe}")
    
    # Check Python Version
    python_ver = sys.version.split()[0]
    print(f"Python Version    : {python_ver}")
    
    # Check if running inside Virtual Environment
    in_venv = sys.prefix != sys.base_prefix
    print(f"Virtual Env Active: {in_venv}")
    
    print("=" * 50)
    if in_venv:
        print("SUCCESS: Project environment is configured correctly!")
    else:
        print("WARNING: Running outside the virtual environment.")
    print("=" * 50)

if __name__ == "__main__":
    verify_environment()