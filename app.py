import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Namibia Economic Risk Platform - Enterprise Edition",
    layout="wide",
)

st.title(
    "🇳🇦 Namibia Integrated Economic & Supply Chain Risk Intelligence System"
)
st.markdown(
    "**Enterprise Risk Edition**: Real-time multi-sector macro-stress testing,"
    " historical trend analysis, and integrated conversational risk advisor."
)

DB_NAME = "namibia_risk_platform.db"


@st.cache_data
def load_data():
  conn = sqlite3.connect(DB_NAME)
  df = pd.read_sql_query("SELECT * FROM economic_nodes_log", conn)
  conn.close()
  return df


df_nodes = load_data()

if df_nodes.empty:
  st.warning(
      "No data found in database. Please run your ingestion script first!"
  )
else:
  # TAB LAYOUT INCLUDING INTERACTIVE CHAT ASSISTANT
  tab1, tab2, tab3, tab4 = st.tabs([
      "📊 Live Node Data",
      "📈 Historical Charts",
      "🧠 AI Reasoning & Interactive Chat Advisor",
      "📄 Executive PDF Report",
  ])

  with tab1:
    st.subheader("Live Ingested Economic Node Data")
    st.dataframe(df_nodes, width="stretch")

    st.subheader("Macroeconomic & Sector Risk Simulator")
    col1, col2, col3 = st.columns(3)
    with col1:
      sim_temp = st.slider(
          "Simulate Temperature (°C)",
          min_value=0.0,
          max_value=50.0,
          value=25.0,
      )
    with col2:
      sim_humidity = st.slider(
          "Simulate Humidity (%)", min_value=0.0, max_value=100.0, value=40.0
      )
    with col3:
      sim_precip = st.slider(
          "Simulate Precipitation (mm)",
          min_value=0.0,
          max_value=50.0,
          value=0.0,
      )

    temp_stress = abs(sim_temp - 22.0)
    water_stress = 10.0 if sim_precip == 0.0 else 1.0
    predicted_risk = (
        (temp_stress * 2.5) + (water_stress * 4.0) + (sim_humidity * 0.1)
    )

    st.metric(
        label="Calculated Sector Vulnerability Index (SVI)",
        value=f"{predicted_risk:.2f} / 100",
    )

  with tab2:
    st.subheader("📈 Historical Trends & Multi-Node Analytics")
    fig = px.bar(
        df_nodes,
        x="node",
        y="temperature_celsius",
        color="primary_sector",
        title="Current Temperature Comparison Across Economic Nodes",
        labels={
            "temperature_celsius": "Temperature (°C)",
            "node": "Economic Node",
        },
    )
    st.plotly_chart(fig, width="stretch")

  with tab3:
    st.subheader("🧠 Enterprise AI Reasoning & Interactive Risk Advisor")
    st.write(
        "Inspect automated node reasoning below, or type your own opinions and"
        " questions directly into the chat assistant."
    )

    selected_node = st.selectbox(
        "Select Node for Deep-Dive Audit", df_nodes["node"], key="reasoning_node"
    )
    node_record = df_nodes[df_nodes["node"] == selected_node].iloc[0]

    r_temp_stress = abs(node_record["temperature_celsius"] - 22.0)
    r_water_stress = (
        10.0 if node_record["precipitation_mm"] == 0.0 else 1.0
    )
    r_score = (
        (r_temp_stress * 2.5)
        + (r_water_stress * 4.0)
        + (node_record["humidity_percent"] * 0.1)
    )

    col_a, col_b = st.columns([1, 2])
    with col_a:
      st.metric(
          label=f"Current SVI for {selected_node}",
          value=f"{r_score:.2f} / 100",
      )
      if r_score > 65:
        st.error("Status: High Vulnerability State")
      elif r_score > 50:
        st.warning("Status: Elevated Stress State")
      else:
        st.success("Status: Normal Nominal State")

    with col_b:
      st.markdown("### 🔍 Root-Cause Reasoning Audit")
      st.markdown(
          f"- **Thermal Deviation**: Recorded at"
          f" **{node_record['temperature_celsius']}°C** (Delta:"
          f" **{r_temp_stress:.1f}°C**)."
      )
      st.markdown(
          f"- **Hydrological Stress**: Precipitation at"
          f" **{node_record['precipitation_mm']} mm**."
      )

    st.markdown("---")
    st.markdown("### 💬 Interactive Namibia Risk Assistant")
    st.write(
        "Ask questions about this node's sector, test opinions, or request"
        " custom mitigation plans right here:"
    )

    # Initialize chat history in Streamlit session state
    if "messages" not in st.session_state:
      st.session_state.messages = [{
          "role": "assistant",
          "content": (
              f"Hello! I am your Namibian Economic Risk Advisor. I am currently"
              f" auditing **{selected_node}** ({node_record['primary_sector']})."
              " Ask me anything about its risk profile, credit exposure, or"
              " mitigation strategies!"
          ),
      }]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
      with st.chat_message(message["role"]):
        st.markdown(message["content"])

    # React to user input
    if user_prompt := st.chat_input(
        f"Type your question or opinion regarding {selected_node}..."
    ):
      # Add user message to session state
      st.session_state.messages.append(
          {"role": "user", "content": user_prompt}
      )
      with st.chat_message("user"):
        st.markdown(user_prompt)

      # Generate contextual assistant response
      with st.chat_message("assistant"):
        user_lower = user_prompt.lower()
        if (
            "agriculture" in user_lower
            or "maize" in user_lower
            or "drought" in user_lower
        ):
          ai_reply = (
              f"Based on current telemetry for **{selected_node}**, agricultural"
              " vulnerability is heavily tied to precipitation deficits. If"
              " zero rainfall persists, rural credit defaults in regional"
              " financial institutions typically spike by 15-20% within two"
              " quarters. Recommending targeted drought-relief credit"
              " restructuring."
          )
        elif "mining" in user_lower or "water" in user_lower:
          ai_reply = (
              f"For mining and industrial nodes like **{selected_node}**, water"
              " allocation bottlenecks present the highest operational risk."
              " Partnering with NamWater on contingency boreholes or recycling"
              " facilities is critical to prevent output curtailment."
          )
        elif "bank" in user_lower or "loan" in user_lower or "credit" in user_lower:
          ai_reply = (
              f"From a banking sector perspective in **{selected_node}**, loan"
              " portfolios exposed to commercial transport or farming require"
              " immediate macro-prudential stress testing against these"
              " environmental parameters."
          )
        else:
          ai_reply = (
              f"That is a insightful point regarding **{selected_node}** ("
              f"{node_record['primary_sector']}). Given the SVI score of"
              f" **{r_score:.2f} / 100**, the primary directive for risk"
              " officers is balancing operational continuity with liquidity"
              " reserves. Is there a specific financial or supply chain scenario"
              " you'd like me to simulate?"
          )

        st.markdown(ai_reply)
        st.session_state.messages.append(
            {"role": "assistant", "content": ai_reply}
        )

  with tab4:
    st.subheader("📄 Generate Executive Risk Report")
    selected_rep_node = st.selectbox(
        "Select Economic Node for Export", df_nodes["node"], key="report_node"
    )
    node_data = df_nodes[df_nodes["node"] == selected_rep_node].iloc[0]

    report_html = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; border: 2px solid #1e3a8a; border-radius: 8px;">
            <h1 style="color: #1e3a8a;">🇳🇦 NAMIBIA RISK INTELLIGENCE REPORT</h1>
            <p><strong>Generated Timestamp:</strong> {node_data['timestamp']}</p>
            <hr>
            <h3>Node Information</h3>
            <p><strong>Location:</strong> {node_data['node']} ({node_data['region']} Region)</p>
            <p><strong>Target Sector:</strong> {node_data['primary_sector']}</p>
            <h3>Environmental Parameters & Reasoning Audit</h3>
            <ul>
                <li>Temperature: {node_data['temperature_celsius']} °C</li>
                <li>Humidity: {node_data['humidity_percent']} %</li>
                <li>Precipitation: {node_data['precipitation_mm']} mm</li>
            </ul>
        </div>
        """
    st.components.v1.html(report_html, height=350)
    st.download_button(
        label="📥 Download Printable HTML/PDF Report",
        data=report_html,
        file_name=f"{selected_rep_node}_executive_risk_report.html",
        mime="text/html",
    )