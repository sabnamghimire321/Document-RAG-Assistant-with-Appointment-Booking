import streamlit as st
from pathlib import Path
from backend.ingest import build_or_update_index
from backend.agent import agent_tool

st.set_page_config(page_title="Document Chatbot + Booking", layout="wide")
st.title("Document Chatbot + Appointment Booking")

st.sidebar.header("Upload Documents")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDF or TXT files", type=["pdf", "txt"], accept_multiple_files=True
)

if uploaded_files:
    Path("docs").mkdir(exist_ok=True)
    saved_paths = []
    for file in uploaded_files:
        save_path = Path("docs") / file.name
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())
        saved_paths.append(str(save_path))

    with st.spinner("Processing documents..."):
        build_or_update_index(saved_paths)
    st.success("Documents processed and indexed.")

tabs = st.tabs(["Chat", "Book Appointment"])

with tabs[0]:
    st.subheader("Chat with your documents")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    chat_history = st.session_state["chat_history"]

    for item in chat_history:
        st.markdown(f"**You:** {item['query']}")
        st.markdown(f"**Bot:** {item['answer']}")

    with st.form("chat_form", clear_on_submit=True):
        query = st.text_input("Ask a question:")
        submitted = st.form_submit_button("Send")

        if submitted and query:
            with st.spinner("Generating answer..."):
                answer = agent_tool(query)
            chat_history.append({"query": query, "answer": answer})
            st.session_state["chat_history"] = chat_history

with tabs[1]:
    st.subheader("Book an Appointment")

    if "booking_info" not in st.session_state:
        st.session_state["booking_info"] = {"name": "", "phone": "", "email": "", "date": ""}

    booking_state = st.session_state["booking_info"]

    name = st.text_input("Name", value=booking_state.get("name", ""), key="name_input")
    phone = st.text_input("Phone", value=booking_state.get("phone", ""), key="phone_input")
    email = st.text_input("Email", value=booking_state.get("email", ""), key="email_input")
    date_text = st.text_input("Preferred Date (e.g., next Monday)", value=booking_state.get("date", ""), key="date_input")

    st.session_state["booking_info"] = {
        "name": name,
        "phone": phone,
        "email": email,
        "date": date_text,
    }

    if st.button("Book Appointment"):
        if not name or not phone or not email or not date_text:
            st.error("Please fill in all fields.")
        elif "@" not in email or "." not in email:
            st.error("Invalid email format.")
        elif not phone.isdigit() or len(phone) < 7:
            st.error("Invalid phone number.")
        else:
            response = agent_tool("book appointment", st.session_state["booking_info"])
            st.success(response)
