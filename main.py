import threading
import time
from fastapi import FastAPI, Request
from factory_simulator import simulate_factory
from agents_and_tasks import run_crew_tasks
from llm_query import query_factory_llm

app = FastAPI(
    title="AgentMesh Smart Factory API",
    description="An API to interact with the multi-agent digital twin of a smart factory."
)

@app.on_event("startup")
def startup_event():
    """
    On startup, we begin the factory simulation and the agent monitoring
    in background threads.
    """
    simulation_thread = threading.Thread(target=simulate_factory, daemon=True)
    simulation_thread.start()

    def agent_loop():
        print("🤖 Starting CrewAI agent monitoring loop...")
        while True:
            run_crew_tasks()
            time.sleep(15)
    agent_thread = threading.Thread(target=agent_loop, daemon=True)
    agent_thread.start()


@app.post("/ask-factory", summary="Ask a question to the factory's AI assistant")
async def ask_factory(request: Request):
    """
    Receives a natural language query, passes it to the LLM with real-time
    factory context, and returns the answer.

    - **body**: JSON with a "query" key. e.g., `{"query": "Is machine M001 overheating?"}`
    """
    body = await request.json()
    question = body.get("query")

    if not question:
        return {"error": "Query not provided"}, 400

    answer = query_factory_llm(question)
    return {"answer": answer}

@app.get("/", summary="Get the current factory state")
def get_factory_state():
    """Returns the entire current state of the factory for debugging or direct monitoring."""
    from factory_simulator import factory_state
    return factory_state
