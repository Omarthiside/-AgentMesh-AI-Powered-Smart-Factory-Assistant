import os
from openai import OpenAI
from factory_simulator import factory_state 
from agents_and_tasks import ProductionAgent, InventoryAgent, MaintenanceAgent

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_factory_llm(question: str):
    """
    Queries the GPT-4 model with a question about the factory, providing
    it with real-time context from the simulation.
    """
    context = f"""
    Here is the current, real-time status of the smart factory:

    **Machine Status:**
    {factory_state['machines']}

    **Inventory Levels:**
    {factory_state['inventory']}

    **Active Alerts:**
    {factory_state['alerts']}

    **Agent Logs & Decisions (Memory):**
    {factory_state['agent_logs'][-5:]}  # Provide the last 5 logs for context

    **Agent Roles:**
    - {ProductionAgent.role}: {ProductionAgent.goal}
    - {InventoryAgent.role}: {InventoryAgent.goal}
    - {MaintenanceAgent.role}: {MaintenanceAgent.goal}
    """

    prompt = f"""
    You are the lead operations AI for the 'AgentMesh' Smart Factory.
    Your role is to answer questions from the factory manager based on the real-time data provided.
    Be concise and clear in your answers.

    ---
    CONTEXT:
    {context}
    ---

    QUESTION:
    {question}
    """

    print("--- Sending Query to LLM ---")

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
