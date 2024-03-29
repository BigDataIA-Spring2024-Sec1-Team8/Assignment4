import streamlit as st
from kafka_helper_functions import consume_message
from snowflake_interface import fetch_data, fetch_meta_data
from airflow_helper_functions import process_pdf, process_pdf_files_concurrently, fetch_updates
   
def batch_upload_ui():
    uploaded_file = st.file_uploader("Upload zip file", type=["zip"])
    if uploaded_file:
        process_pdf_files_concurrently(uploaded_zip_file=uploaded_file)
    
def consume_trigger():
    if st.button('consume messages'):
        consume_message()
def check_status_ui():
    run_id = st.text_input('run_id')
    if run_id:
        fetch_updates(run_id)

def single_file_ui():
    st.title("Single File DAG Trigger")

    st.title("Upload File to S3")

    # File uploader
    uploaded_file = st.file_uploader("Upload a file")

    # Check if a file is uploaded
    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        process_pdf(uploaded_file=uploaded_file)


# Display data using Streamlit
def data_ui():
    st.write("Topics Data")
    data=[]
    search_topic = st.text_input("Search for a topic:")
    if search_topic:
        data = fetch_data(search_topic=search_topic)
        st.table(data)
    st.write("Meta Data")
    metadata = fetch_meta_data()
    st.table(metadata)

pages = {
    "Single File handler": single_file_ui,
    "Snowflake Data": data_ui,
    "Batch upload hanfler": batch_upload_ui,
    "Kafka Consume Triggerer": consume_trigger,
    "Dag Status": check_status_ui
}
def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    pages[selection]()

if __name__ == "__main__":
    main()
