from fastapi import FastAPI
from pydantic import BaseModel

from planner import create_plan
from executor import execute_plan
from doc_generator import generate_document

app = FastAPI(title="Autonomous AI Agent", version="1.0")


class AgentRequest(BaseModel):
    request: str


@app.get("/")
def home():
    return {"message": "Autonomous AI Agent is running. POST to /agent to use it."}


@app.post("/agent")
def run_agent(body: AgentRequest):
    user_request = body.request

    if not user_request or not user_request.strip():
        return {
            "status": "error",
            "message": "The 'request' field cannot be empty.",
        }

    try:
        print("Planning...")
        plan = create_plan(user_request)

        print("Executing plan...")
        sections = execute_plan(user_request, plan)

        print("Generating document...")
        file_path = generate_document(user_request, sections)

        return {
            "status": "success",
            "original_request": user_request,
            "generated_plan": plan,
            "output_file_path": file_path,
            "message": "Document generated successfully.",
        }

    except Exception as error:
        return {
            "status": "error",
            "original_request": user_request,
            "message": f"Something went wrong: {error}",
        }