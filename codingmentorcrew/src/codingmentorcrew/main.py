#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from codingmentorcrew.crew import Codingmentorcrew
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4o")
MAX_TOKENS = 8192
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    
    inputs = {
        'current_year': str(datetime.now().year)
    }
    try:
        #result = Codingmentorcrew().crew().kickoff()
        
        print(str(Codingmentorcrew().crew().kickoff()))

        
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")