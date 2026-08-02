import streamlit as st
import requests
import pandas as pd

API_URL = "https://leadme-backend.onrender.com/api/v1"

st.set_page_config(page_title="LeadMe Admin Console", layout="wide", page_icon="📈")

st.sidebar.title("LeadMe Settings")
client_id = st.sidebar.text_input("Client ID", "demo_client_1")

# Health Check
try:
    res = requests.get(f"{API_URL}/leads/")
    if res.status_code == 200:
        st.sidebar.success("Backend API: Online 🟢")
    else:
        st.sidebar.warning(f"Backend API Error: {res.status_code} 🟡")
except Exception:
    st.sidebar.error("Backend API: Offline 🔴")

st.title("LeadMe Admin Dashboard")
st.markdown("Manage your AI agent's knowledge, view captured leads, and resolve open tickets.")

tab1, tab2, tab3 = st.tabs(["📊 Leads & Analytics", "🎫 Ticket Manager", "🧠 Knowledge Base"])

with tab1:
    st.header("Captured Leads")
    try:
        res = requests.get(f"{API_URL}/leads/")
        if res.status_code == 200:
            leads = res.json().get("data", [])
            
            # Fetch open tickets for metrics
            tickets_res = requests.get(f"{API_URL}/tickets/open")
            open_tickets_count = 0
            if tickets_res.status_code == 200:
                open_tickets_count = len(tickets_res.json().get("data", []))

            col1, col2 = st.columns(2)
            col1.metric("Total Leads Captured", len(leads))
            col2.metric("Open Tickets", open_tickets_count)
            
            if leads:
                df = pd.DataFrame(leads)
                # Keep interesting columns
                if "id" in df.columns:
                    df = df[["id", "client_id", "session_id", "email", "created_at"]]
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No leads captured yet.")
        else:
            st.error("Failed to fetch leads.")
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")

with tab2:
    st.header("Human-in-the-Loop Ticket Manager")
    st.write("When the AI cannot answer a question, a ticket is created here. Answering it will notify the user and teach the AI for next time!")
    
    try:
        res = requests.get(f"{API_URL}/tickets/open")
        if res.status_code == 200:
            tickets = res.json().get("data", [])
            
            # Filter by client_id
            tickets = [t for t in tickets if t["client_id"] == client_id]
            
            if not tickets:
                st.success("No open tickets! You're all caught up. 🎉")
            else:
                for t in tickets:
                    with st.expander(f"Ticket #{t['id']} from {t['lead_email']} (Pending)", expanded=True):
                        st.markdown(f"**Question:** {t['question']}")
                        st.caption(f"Created At: {t['created_at']}")
                        
                        answer = st.text_area("Your Answer (will be sent to the lead and saved to Vector DB):", key=f"answer_{t['id']}")
                        if st.button("Resolve & Teach AI", key=f"btn_{t['id']}"):
                            if not answer.strip():
                                st.warning("Please provide an answer before resolving.")
                            else:
                                resolve_res = requests.post(f"{API_URL}/tickets/resolve", json={
                                    "ticket_id": t['id'],
                                    "answer": answer
                                })
                                if resolve_res.status_code == 200:
                                    st.success(f"Ticket #{t['id']} resolved successfully!")
                                    st.rerun()
                                else:
                                    st.error(f"Failed to resolve: {resolve_res.text}")
        else:
            st.error("Failed to fetch tickets.")
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")

with tab3:
    st.header("Knowledge Base Manager")
    st.write("Feed data into your agent's Vector Database.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Website Scraper")
        with st.form("scrape_form"):
            url = st.text_input("Website URL to scrape:")
            scrape_submit = st.form_submit_button("Scrape & Ingest")
            if scrape_submit:
                if url:
                    with st.spinner("Scraping and generating embeddings..."):
                        res = requests.post(f"{API_URL}/knowledge/scrape", json={
                            "url": url,
                            "client_id": client_id
                        })
                        if res.ok:
                            st.success(f"Successfully ingested {url}!")
                        else:
                            st.error(f"Failed: {res.text}")
                else:
                    st.warning("Please enter a URL.")
                    
    with col2:
        st.subheader("Manual FAQ Entry")
        with st.form("faq_form"):
            q = st.text_input("Question")
            a = st.text_area("Answer")
            faq_submit = st.form_submit_button("Add FAQ")
            if faq_submit:
                if q and a:
                    with st.spinner("Ingesting FAQ..."):
                        res = requests.post(f"{API_URL}/knowledge/faq", json={
                            "question": q,
                            "answer": a,
                            "client_id": client_id
                        })
                        if res.ok:
                            st.success("FAQ added successfully!")
                        else:
                            st.error(f"Failed: {res.text}")
                else:
                    st.warning("Please fill out both question and answer.")
