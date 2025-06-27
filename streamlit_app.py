import streamlit as st
import pandas as pd
import json
from pathlib import Path

# --- Constants ---
DATA_FILE = "travel_data.json"  # For local data persistence
DEFAULT_DATA = [
    ["VIA Rail (Econ)", "Train", 75, "5h", 4.0, "Good"],
    ["VIA Rail (Business)", "Train", 150, "5h", 5.0, "Excellent"],
    ["FlixBus", "Bus", 45, "6h", 3.0, "Fair"],
    ["Megabus", "Bus", 40, "6.5h", 2.0, "Basic"],
    ["Porter Airlines", "Plane", 180, "1h", 4.0, "Good"]
]

# --- Data Management ---
def load_data():
    """Load data from JSON file or use defaults."""
    if Path(DATA_FILE).exists():
        with open(DATA_FILE) as f:
            return pd.DataFrame(json.load(f))
    return pd.DataFrame(DEFAULT_DATA, columns=["Provider", "Mode", "Price (CAD)", "Travel Time", "Comfort", "Value"])

def save_data(df):
    """Save DataFrame to JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(df.to_dict('records'), f)

# --- UI ---
st.set_page_config(page_title="Travel Planner", layout="wide")
st.title("🚂 Toronto-Montreal Travel Planner")

# Sidebar for filters
with st.sidebar:
    st.header("Filters")
    max_price = st.slider("Max Price (CAD)", 0, 300, 300, 10)
    min_comfort = st.slider("Minimum Comfort Rating", 1.0, 5.0, 3.0, 0.5)

# Main content
df = load_data()

# Apply filters
filtered = df[
    (df["Price (CAD)"] <= max_price) & 
    (df["Comfort"] >= min_comfort)
]

# Display results
st.subheader(f"Found {len(filtered)} options")
st.dataframe(
    filtered.style.format({
        "Price (CAD)": "${:.0f}",
        "Comfort": "{:.1f} ★"
    }),
    height=400,
    use_container_width=True
)

# Data management section
with st.expander("Advanced Options"):
    st.write("**Add/Edit Travel Options**")
    new_entry = st.text_input("New Provider Name")
    if new_entry:
        if st.button("Add to Data"):
            new_row = pd.DataFrame([[new_entry, "Custom", 0, "0h", 3.0, "Good"]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success("Added new provider!")
            st.rerun()

    if st.button("Reset to Default Data"):
        df = pd.DataFrame(DEFAULT_DATA, columns=df.columns)
        save_data(df)
        st.rerun()

# --- Optional Cloud Integration ---
# Uncomment to enable Firebase (requires firebase_admin package)
# if st.secrets.get("firebase"):
#     from firebase_admin import firestore
#     db = firestore.client()
#     # Add your Firebase sync logic here
