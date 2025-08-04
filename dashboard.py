import streamlit as st
import requests
import json
import time
import hashlib

API_URL = "http://127.0.0.1:8000/ask-factory"
STATE_URL = "http://127.0.0.1:8000/"


proxies = {
   "http": None,
   "https": None,
}

st.set_page_config(page_title="AgentMesh Factory Assistant", layout="wide")

st.title("🏭 AgentMesh Smart Factory Assistant")
st.caption("Your AI-powered interface to the factory floor.")

query = st.text_input("Ask the Factory a Question:", placeholder="e.g., Summarize today's production issues.")

if st.button("Get Answer"):
    if query:
        with st.spinner("Asking the factory AI..."):
            try:
                response = requests.post(API_URL, json={"query": query}, proxies=proxies)
                response.raise_for_status()
                answer = response.json().get("answer", "No answer found.")
                st.info("💡 **AI Assistant's Answer:**")
                st.markdown(answer)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the factory API: {e}")
    else:
        st.warning("Please enter a question.")

st.divider()

st.header("📊 Live Factory Dashboard")
state_placeholder = st.empty()

while True:
    try:
        response = requests.get(STATE_URL, proxies=proxies)
        response.raise_for_status()
        factory_state = response.json()

        with state_placeholder.container():
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Machine Status")
                for machine_id, data in factory_state.get("machines", {}).items():
                    status_color = "green" if data['status'] == 'running' else "orange"
                    st.markdown(f"**{machine_id}**: :{status_color}[{data['status']}] | Temp: `{data['temperature_celsius']:.1f}°C` | Util: `{data['utilization']*100:.0f}%`")

                st.subheader("Inventory Levels")
                inventory = factory_state.get("inventory", {})
                st.metric(label="Raw Materials", value=inventory.get("raw_materials", 0))
                st.metric(label="Finished Goods", value=inventory.get("finished_goods", 0))


            with col2:
                st.subheader("🚨 Active Alerts")
                alerts = factory_state.get("alerts", [])
                if alerts:
                    for alert in alerts:
                        st.warning(alert)
                else:
                    st.success("No active alerts.")

                st.subheader("📝 Latest Agent Logs")
                logs = factory_state.get("agent_logs", [])
                if logs:
                    last_log = logs[-1].get('crew_result', 'No result found.')
                    log_hash = hashlib.md5(str(last_log).encode()).hexdigest()
                    unique_key = f"crew_log_area_{log_hash}_{int(time.time())}"
                    st.text_area(
                        "Last Crew Analysis:",
                        value=last_log,
                        height=200,
                        key=unique_key
                    )

                else:
                    st.info("No agent logs yet.")

    except requests.exceptions.RequestException as e:
        st.error(f"Could not fetch live factory state. Is the backend running? (Error: {e})")
        print(f"ERROR in dashboard loop: {e}")


    time.sleep(5) 
