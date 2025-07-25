#!/usr/bin/env python3
"""Initialize git submodules if they haven't been pulled yet."""

import subprocess
import os
from pathlib import Path

def setup_submodules():
    """Initialize and update git submodules if needed."""
    try:
        # Check if we're in a git repository
        if not Path('.git').exists():
            print("Not in a git repository, skipping submodule setup")
            return
        
        # Check if submodules are already initialized
        submodule_paths = ['fedramp-docs', 'fedramp-rfcs', 'fedramp-roadmap']
        need_init = False
        
        for path in submodule_paths:
            submodule_dir = Path(path)
            # Check if directory exists and has content
            if not submodule_dir.exists() or not any(submodule_dir.iterdir()):
                need_init = True
                break
        
        if need_init:
            print("Initializing git submodules...")
            # Initialize submodules
            subprocess.run(['git', 'submodule', 'init'], check=True)
            # Update submodules
            subprocess.run(['git', 'submodule', 'update'], check=True)
            print("Submodules initialized successfully")
        else:
            print("Submodules already initialized")
            
    except subprocess.CalledProcessError as e:
        print(f"Error setting up submodules: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    setup_submodules()