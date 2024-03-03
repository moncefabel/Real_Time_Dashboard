#!/bin/bash 
# Specify the DISPLAY environment variable
export DISPLAY=:0

# Kill any existing Streamlit processes that are running on the specified port
pkill -f "/path/to/streamlit run --server.port 8501"

# Build and run the Streamlit app
/path/to/streamlit run --server.port 8501 /path/to/script/streamlit_script.py & 
 # Wait for the app to start (adjust the sleep duration as needed) 
 sleep 10 
 # Open the app in a web browser 
 firefox http://localhost:8501