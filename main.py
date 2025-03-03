#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from crew import Codingmentorcrew, crawlTool
import tiktoken
import os
#Exposing crew to API
import uvicorn
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import List, Optional

load_dotenv()
app = FastAPI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#Temporary in-memory job store (WILL BE REPLACED WITH DATABASE)
jobs = {}

class KeyValuePair(BaseModel):
    key: str
    value: str

class StartJobRequest(BaseModel):
    # Per MIP-003, input_data should be defined under input_schema endpoint
    query: str

class ProvideInputRequest(BaseModel):
    job_id: str
# ─────────────────────────────────────────────────────────────────────────────
# 1) Start Job (MIP-003: /start_job)
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/start_job")
async def start_job(request_body: StartJobRequest):
    """
    Initiates a job with specific input data.
    Fulfills MIP-003 /start_job endpoint.
    """
    if not OPENAI_API_KEY:
        return {"status": "error", "message": "Missing OpenAI API Key. Check your .env file."}

    # Generate unique job & payment IDs
    job_id = str(uuid.uuid4())
    payment_id = str(uuid.uuid4())  # Placeholder, in production track real payment

    # For demonstration: set job status to 'awaiting payment'
    jobs[job_id] = {
        "status": "awaiting payment",  # Could also be 'awaiting payment', 'running', etc.
        "payment_id": payment_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input_data": request_body.query,
        "result": None
    }

    # Here you invoke your crew
    crew = Codingmentorcrew()
    query = request_body.query
    websites = str(crawlTool.run(search_query=query))
    inputs = {
        'topic': websites,
        'query':query,
        'current_year': str(datetime.now().year)
    }
    try:
        result = Codingmentorcrew().crew().kickoff(inputs = inputs)

        print(str(result))

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    # Store result as if we immediately completed it (placeholder)
    jobs[job_id]["status"] = "completed"
    jobs[job_id]["result"] = result

    return {
        "status": "success",
        "job_id": job_id,
        "payment_id": payment_id
    }

# ─────────────────────────────────────────────────────────────────────────────
# 2) Check Job Status (MIP-003: /status)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/status")
async def check_status(job_id: str = Query(..., description="Job ID to check status")):
    """
    Retrieves the current status of a specific job.
    Fulfills MIP-003 /status endpoint.
    """
    if job_id not in jobs:
        # Return 404 in a real system; here, just return a JSON error
        return {"error": "Job not found"}

    job = jobs[job_id]
    return {
        "job_id": job_id,
        "status": job["status"],
        "result": job["result"]  # Optional in MIP-003, included if available
    }

# ─────────────────────────────────────────────────────────────────────────────
# 3) Provide Input (MIP-003: /provide_input)
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/provide_input")
async def provide_input(request_body: ProvideInputRequest):
    """
    Allows users to send additional input if a job is in an 'awaiting input' status.
    Fulfills MIP-003 /provide_input endpoint.
    
    In this example we do not require any additional input, so it always returns success.
    """
    job_id = request_body.job_id

    if job_id not in jobs:
        return {"status": "error", "message": "Job not found"}

    job = jobs[job_id]

    return {"status": "success"}

# ─────────────────────────────────────────────────────────────────────────────
# 4) Check Server Availability (MIP-003: /availability)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/availability")
async def check_availability():
    """
    Checks if the server is operational.
    Fulfills MIP-003 /availability endpoint.
    """
    # Simple placeholder. In a real system, you might run
    # diagnostic checks or return server load info.
    return {
        "status": "available",
        "message": "The server is running smoothly."
    }

# ─────────────────────────────────────────────────────────────────────────────
# 5) Retrieve Input Schema (MIP-003: /input_schema)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/input_schema")
async def input_schema():
    """
    Returns the expected input schema for the /start_job endpoint.
    Fulfills MIP-003 /input_schema endpoint.
    """
    # Example response defining the accepted key-value pairs
    query_input = {
        "input_data": [
            {"key": "query", "value": "string"}
        ]
    }
    return query_input

# ─────────────────────────────────────────────────────────────────────────────
# Main logic if called as a script
# ─────────────────────────────────────────────────────────────────────────────
def main():
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY is missing. Please check your .env file.")
        return

    crew = Codingmentorcrew()
    # Get user input directly instead of using input_schema
    query = input("Enter search query: ")
    websites = str(crawlTool.run(search_query=query))
    inputs = {
        'topic': websites,
        'query': query,
        'current_year': str(datetime.now().year)
    }
    try:
        result = Codingmentorcrew().crew().kickoff(inputs=inputs)
        print(str(result))
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    import sys

    # If 'api' argument is passed, start the FastAPI server
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        print("Starting FastAPI server...")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        main()



def run():
    """
    Run the crew.
    """

    query = str(input("Enter search query: "))
    websites = str(crawlTool.run(search_query= query))
    inputs = {
        'topic': websites,
        'query':query,
        'current_year': str(datetime.now().year)
    }
    
    try:
        result = Codingmentorcrew().crew().kickoff(inputs = inputs)

        print(str(result))

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")



        