import os
import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000/agent"

st.set_page_config(page_title="Autonomous AI Agent", page_icon="🤖")

st.title("🤖 Autonomous AI Agent")
st.write(
    "Type a request. The agent will plan the sections by itself, write each "
    "one, and produce a professional Word document."
)

examples = {
    "— choose an example —": "",
    "Business proposal (AI Resume Screening System)":
        "Create a business proposal for an AI Resume Screening System.",
    "Project plan (Inventory Management System)":
        "Create a project plan for an Inventory Management System. "
        "Budget is not provided, so choose a reasonable timeline and "
        "clearly mention any assumptions.",
}

chosen_example = st.selectbox("Quick examples", list(examples.keys()))

default_text = examples[chosen_example]

user_request = st.text_area(
    "Your request",
    value=default_text,
    height=120,
    placeholder="e.g. Create a business proposal for an AI Resume Screening System.",
)

if st.button("Run Query", type="primary"):

    if not user_request.strip():
        st.warning("Please type a request first.")
    else:
        with st.spinner("The agent is planning and writing your document..."):
            try:
                response = requests.post(
                    BACKEND_URL,
                    json={"request": user_request},
                    timeout=180,
                )
                data = response.json()

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not reach the backend. Make sure FastAPI is running:\n\n"
                    "`uvicorn main:app --reload`"
                )
                st.stop()

            except Exception as error:
                st.error(f"Unexpected error: {error}")
                st.stop()

        if data.get("status") == "success":
            st.success(data.get("message", "Done!"))

            st.subheader("📋 Generated Plan")
            for i, section in enumerate(data.get("generated_plan", []), start=1):
                st.write(f"{i}. {section}")

            file_path = data.get("output_file_path")
            if file_path and os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Word Document",
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime="application/vnd.openxmlformats-officedocument."
                             "wordprocessingml.document",
                    )
            else:
                st.info(f"Document saved on the server at: {file_path}")

        else:
            st.error(data.get("message", "The agent failed."))