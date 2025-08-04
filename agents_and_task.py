from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from factory_simulator import factory_state 

load_dotenv()


ProductionAgent = Agent(
    role='Production Manager',
    goal='Optimize production scheduling and ensure machine uptime by monitoring the factory state.',
    backstory='An experienced manager who keeps a close eye on all machine operations and production metrics.',
    verbose=True,
    allow_delegation=False
)

InventoryAgent = Agent(
    role='Inventory Specialist',
    goal='Monitor inventory levels of raw materials and finished goods, and flag critical levels.',
    backstory='A meticulous specialist who ensures the supply chain is never a bottleneck.',
    verbose=True,
    allow_delegation=False
)

MaintenanceAgent = Agent(
    role='Maintenance Engineer',
    goal='Monitor machine health, predict failures from alerts, and schedule maintenance.',
    backstory='A proactive engineer who prevents breakdowns before they happen.',
    verbose=True,
    allow_delegation=False
)



def create_monitoring_tasks():
    """Creates tasks for the agents based on the current factory_state."""

    production_description = f"""
    Analyze the current production floor status and report any anomalies.
    Current machine states: {factory_state['machines']}.
    Pay close attention to utilization and status.
    Log your findings in the 'agent_logs'.
    """
    production_task = Task(
        description=production_description,
        expected_output="A summary report of machine status and any production anomalies.",
        agent=ProductionAgent
    )

    inventory_description = f"""
    Check the current inventory levels and flag if raw materials are running low (below 200).
    Current inventory: {factory_state['inventory']}.
    Log your findings in the 'agent_logs'.
    """
    inventory_task = Task(
        description=inventory_description,
        expected_output="A status report on inventory levels, with a clear warning if restocking is needed.",
        agent=InventoryAgent
    )

    maintenance_description = f"""
    Review the current system alerts and determine if any maintenance is required.
    Current alerts: {factory_state['alerts']}.
    If an 'overheating' alert exists, recommend immediate inspection.
    Log your findings in the 'agent_logs'.
    """
    maintenance_task = Task(
        description=maintenance_description,
        expected_output="A maintenance report based on system alerts, with action recommendations.",
        agent=MaintenanceAgent
    )

    return [production_task, inventory_task, maintenance_task]

def run_crew_tasks():
    """Initializes and runs the CrewAI crew with the latest tasks."""
    tasks = create_monitoring_tasks()
    factory_crew = Crew(
        agents=[ProductionAgent, InventoryAgent, MaintenanceAgent],
        tasks=tasks,
        verbose=True
    )
    result = factory_crew.kickoff()
    factory_state["agent_logs"].append({"crew_result": result})
    return result
