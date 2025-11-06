import streamlit as st
import requests
from datetime import date
from config import settings

# Enhanced dark theme CSS
st.markdown(
    """
<style>
    /* Root background - black */
    .stApp {
        background-color: #000000;
    }

    /* Main container background */
    .main .block-container {
        background-color: #000000;
        padding-top: 2rem;
    }

    /* Title - Fuchsia Pink */
    h1 {
        color: #FF2AA0 !important;
        font-weight: bold;
    }

    /* Chat container - dark grey with border */
    div[data-testid="stContainer"] {
        background-color: #2b2b2b;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #404040;
    }

    /* Sidebar - mid grey with border */
    [data-testid="stSidebar"] {
        background-color: #333333  !important;
        border-right: 2px solid #404040 !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        background-color: #333333;
    }

    /* Sidebar labels and text - Fuchsia Pink */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stDateInput label,
    [data-testid="stSidebar"] .stRadio label p,
    [data-testid="stSidebar"] .stRadio label span,
    [data-testid="stSidebar"] .stRadio > label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #FF2AA0 !important;
    }

    /* Input fields styling (main area only) */
    .stTextInput input {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
        border: 1px solid #404040 !important;
    }

    .stTextInput input:focus {
        border-color: #FF2AA0 !important;
    }

    /* Button styling */
    button[kind="primary"] {
        background-color: #404040 !important;
        color: #ffffff !important;
        border: 1px solid #555555 !important;
    }

    button[kind="primary"]:hover {
        background-color: #555555 !important;
        border-color: #FF2AA0 !important;
    }

    /* Text color for readability (main area only) */
    .stMarkdown,
    .stMarkdown p,
    .stMarkdown strong {
        color: #e0e0e0 !important;
    }

    /* Chat message styling */
    .stMarkdown strong {
        color: #FF2AA0 !important;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #1e1e1e;
    }

    ::-webkit-scrollbar-thumb {
        background: #555555;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #666666;
    }
</style>
""",
    unsafe_allow_html=True,
)

API_URL = f"{settings.api_url}{settings.api_path}"

st.title("🫦laiive")

with st.sidebar:
    places = ["All", "Bergamo", "Barcelona", "Boston", "Milano"]
    selected_place = st.selectbox("CITY:", places)

    date_option = st.radio("DATE:", ["All Dates", "Specific Date", "Date Range"])

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


if "messages" not in st.session_state:
    st.session_state.messages = []


def get_laiive_response(
    user_message,
    place_filter=None,
    date_filter=None,
    date_range=None,
):
    try:
        # Prepare the request payload with filters
        payload = {
            "message": user_message,
            "filters": {
                "place": place_filter if place_filter != "All" else None,
                "date": date_filter.isoformat() if date_filter else None,
                "date_range": (
                    {
                        "start": date_range[0].isoformat(),
                        "end": date_range[1].isoformat(),
                    }
                    if date_range is not None
                    else None
                ),
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


# Create a scrollable container for chat messages
chat_container = st.container(height=500)  # Adjust height as needed

with chat_container:
    # Display chat history
    for sender, msg in st.session_state.messages:
        if sender == "user":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**laiive:** {msg}")

# Fixed input area at the bottom
with st.container():
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "You:",
            key="user_input",
            label_visibility="collapsed",
            placeholder="Type your message...",
        )
    with col2:
        send_button = st.button("Send", use_container_width=True)

if send_button and user_input:
    st.session_state.messages.append(("user", user_input))

    # Pass filters to the API
    bot_reply = get_laiive_response(
        user_input,
        place_filter=selected_place,
        date_filter=selected_date,
        date_range=date_range,
    )

    st.session_state.messages.append(("laiive", bot_reply))
    st.rerun()  # Refresh to show new messages
