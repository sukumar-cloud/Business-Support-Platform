import streamlit as st
import requests

st.set_page_config(page_title="Multi-Agent Platform", layout="centered", page_icon="🤖")

st.markdown("""
<style>
body {
    background-color: #18191A;
}
.big-title {
    font-size:2.5rem;
    font-weight:700;
    color:#4F8BF9;
    margin-bottom:0.5em;
}
.agent-tab {
    background: #23272F;
    border-radius: 12px;
    padding: 2em 2em 1em 2em;
    margin-bottom: 2em;
    box-shadow: 0 2px 8px rgba(79,139,249,0.08);
}
.stTextInput>div>div>input {
    background-color: #18191A;
    color: #fff;
    border-radius: 8px;
    border: 1px solid #4F8BF9;
    font-size: 1.1rem;
    padding: 0.75em 1em;
}
.stButton>button {
    background-color: #4F8BF9;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 0.5em 2em;
    font-size: 1.1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🤖 Business Support Platform </div>', unsafe_allow_html=True)

st.markdown("""
Welcome! This app lets you interact with:
- <b>Support Agent</b>: Service queries, order/payment status, client enquiries<br>
- <b>Dashboard Agent</b>: Business analytics and metrics
""", unsafe_allow_html=True)

if "support_qa_map" not in st.session_state:
    st.session_state["support_qa_map"] = {}
if "dashboard_qa_map" not in st.session_state:
    st.session_state["dashboard_qa_map"] = {}

API_URL = "https://backend-platform-lgd9.onrender.com"

tab1, tab2 = st.tabs([" Support Agent", " Dashboard Agent"])

with tab1:
    st.markdown('<div class="agent-tab">', unsafe_allow_html=True)
    st.header("Support Agent")
    user_query = st.text_input(
        "Ask a support question:",
        placeholder="E.g. What classes are available this week?",
        key="support_input"
    )
    if st.button("Submit Support Query", key="support_btn"):
        if user_query:
            try:
                with st.spinner('Waiting for Support Agent response:'):
                    response = requests.post(f"{API_URL}/ask-support", json={"prompt": user_query})
                    if response.status_code == 200:
                        result = response.json().get("response", "No response from agent.")
                        st.success(f"Support Agent Response: {result}")
                        st.session_state["support_qa_map"][user_query] = result
                    else:
                        st.error(f"Error: {response.text}")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
        else:
            st.warning("Please enter a question before submitting.")
    if st.session_state["support_qa_map"]:
        st.markdown("**Support Query History:**")
        qa_list = list(st.session_state["support_qa_map"].items())
        for idx, (q, a) in enumerate(reversed(qa_list)):
            st.write(f"- **Q:** {q}")
            if idx == 0:
                st.markdown(f'<div style="background-color:#222b4f;padding:10px;border-radius:8px;color:#fff;">  <b>A:</b> {a}</div>', unsafe_allow_html=True)
            else:
                st.write(f"  - **A:** {a}")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="agent-tab">', unsafe_allow_html=True)
    st.header("Dashboard Agent")
    dashboard_query = st.text_input(
        "Ask a dashboard question:",
        placeholder="E.g. How much revenue did we generate this month?",
        key="dashboard_input"
    )
    if st.button("Submit Dashboard Query", key="dashboard_btn"):
        if dashboard_query:
            try:
                with st.spinner('Waiting for Dashboard Agent response:'):
                    response = requests.post(f"{API_URL}/ask-dashboard", json={"prompt": dashboard_query})
                    if response.status_code == 200:
                        result = response.json().get("response", "No response from agent.")
                        st.info(f"Dashboard Agent Response: {result}")
                        st.session_state["dashboard_qa_map"][dashboard_query] = result
                    else:
                        st.error(f"Error: {response.text}")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
        else:
            st.warning("Please enter a question before submitting.")
    if st.session_state["dashboard_qa_map"]:
        st.markdown("**Dashboard Query History:**")
        for q, a in reversed(list(st.session_state["dashboard_qa_map"].items())):
            st.write(f"- **Q:** {q}")
            st.write(f"  - **A:** {a}")
    st.markdown('</div>', unsafe_allow_html=True)
