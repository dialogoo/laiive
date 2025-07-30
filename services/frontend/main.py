import streamlit as st
import requests
from datetime import date

API_URL = "http://localhost:8000/chat"

st.title("🫦laiive")

# Sidebar for filters
with st.sidebar:
    st.header("SQL Filters")

    # Place filter
    places = ["All", "Bergamo", "Barcelona", "Boston", "Milano"]
    selected_place = st.selectbox("PLACE FILTER:", places)

    # Date filter
    date_option = st.radio("DATE FILTER:", ["All Dates", "Specific Date", "Date Range"])

    if date_option == "Specific Date":
        selected_date = st.date_input("Select Date:", value=date(2025, 8, 1))
        date_range = None
    elif date_option == "Date Range":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From:", value=date(2025, 8, 1))
        with col2:
            end_date = st.date_input("To:", value=date(2025, 12, 31))
        date_range = (start_date, end_date)
        selected_date = None
    else:
        selected_date = None
        date_range = None

    # Display current filters
    st.subheader("Current Filters")
    st.write(f"**Place:** {selected_place}")
    if date_option == "Specific Date":
        st.write(f"**Date:** {selected_date}")
    elif date_option == "Date Range" and date_range is not None:
        st.write(f"**Date Range:** {date_range[0]} to {date_range[1]}")
    else:
        st.write("**Date:** All Dates")

if "messages" not in st.session_state:
    st.session_state.messages = []


def get_laiive_response(
    user_message, place_filter=None, date_filter=None, date_range=None
):
    try:
        # Prepare the request payload with filters
        payload = {
            "message": user_message,
            "filters": {
                "place": place_filter if place_filter != "All" else None,
                "date": date_filter.isoformat() if date_filter else None,
                "date_range": {
                    "start": date_range[0].isoformat(),
                    "end": date_range[1].isoformat(),
                }
                if date_range is not None
                else None,
            },
        }

        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            return response.json().get(
                "response", "No field named response in the response from retriever."
            )
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Connection error: {e}"


# Main chat interface
st.header("Chat search engine")

user_input = st.text_input("You:", key="user_input")

if st.button("Send") and user_input:
    st.session_state.messages.append(("user", user_input))

    # Pass filters to the API
    bot_reply = get_laiive_response(
        user_input,
        place_filter=selected_place,
        date_filter=selected_date,
        date_range=date_range,
    )

    st.session_state.messages.append(("bot", bot_reply))

# Display chat history
for sender, msg in st.session_state.messages:
    if sender == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**laiive:** {msg}")
