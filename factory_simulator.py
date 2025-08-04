import time
import random

factory_state = {
    "machines": {
        "M001": {"status": "running", "temperature_celsius": 75.2, "utilization": 0.85},
        "M002": {"status": "running", "temperature_celsius": 68.5, "utilization": 0.70},
        "M003": {"status": "maintenance", "temperature_celsius": 45.0, "utilization": 0.0},
    },
    "inventory": {
        "raw_materials": 1200,
        "finished_goods": 650,
    },
    "alerts": [],
    "agent_logs": [] 
}

def simulate_factory():
    """
    A simulation loop that updates the factory_state in real-time.
    This function is intended to be run in a separate thread or process.
    """
    print("🚀 Starting factory simulation...")
    while True:
        for machine_id, data in factory_state["machines"].items():
            if data["status"] == "running":
                data["temperature_celsius"] += random.uniform(-1.5, 1.5)
                if data["temperature_celsius"] > 90.0 and f"Machine {machine_id} overheating" not in factory_state["alerts"]:
                    alert_msg = f"Alert: Machine {machine_id} is overheating at {data['temperature_celsius']:.2f}°C"
                    factory_state["alerts"].append(alert_msg)
                    print(alert_msg)

        factory_state["inventory"]["raw_materials"] -= random.randint(5, 15)
        factory_state["inventory"]["finished_goods"] += random.randint(3, 10)

        if random.random() < 0.1 and factory_state["alerts"]:
             resolved_alert = factory_state["alerts"].pop(0)
             print(f"✅ Alert resolved: {resolved_alert}")


        time.sleep(5)
