import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(
    page_title="Hospital Bed Capacity Dashboard",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Hospital Bed Capacity Dashboard")
st.markdown("Real-time monitoring of ward occupancy and bed availability.")

# 2. Create Dummy Data for 3 Wards
@st.cache_data
def get_hospital_data():
    # Fixed data for consistency, but structured as a DataFrame
    data = {
        "Ward": ["ICU", "General Medicine", "Maternity"],
        "Total Beds": [50, 150, 60],
        "Occupied Beds": [42, 112, 30]
    }
    df = pd.DataFrame(data)
    
    # Calculate available beds and occupancy rate
    df["Available Beds"] = df["Total Beds"] - df["Occupied Beds"]
    df["Occupancy Rate (%)"] = round((df["Occupied Beds"] / df["Total Beds"]) * 100, 1)
    return df

df_wards = get_hospital_data()

# 3. Sidebar Filter (Slider)
st.sidebar.header("Filters")
max_occupancy = st.sidebar.slider(
    "Filter by Maximum Occupancy Rate (%)",
    min_value=0,
    max_value=100,
    value=100,
    step=5
)

# Filter the dataframe based on the slider input
filtered_df = df_wards[df_wards["Occupancy Rate (%)"] <= max_occupancy]

# 4. Key Metrics Display
if not filtered_df.empty:
    total_occupied = int(filtered_df["Occupied Beds"].sum())
    total_beds = int(filtered_df["Total Beds"].sum())
    overall_rate = round((total_occupied / total_beds) * 100, 1) if total_beds > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Occupied Beds", total_occupied)
    col2.metric("Total Available Beds", int(filtered_df["Available Beds"].sum()))
    col3.metric("Average Occupancy Rate", f"{overall_rate}%")
    
    st.markdown("---")

    # 5. Display a Bar Chart of Occupancy
    st.subheader("Bed Occupancy Comparison")
    
    # We alter the dataframe view slightly to make a clean side-by-side bar chart
    chart_data = filtered_df.set_index("Ward")[["Occupied Beds", "Available Beds"]]
    st.bar_chart(chart_data, color=["#ff4b4b", "#00f0c2"]) # Red for occupied, teal for available

    # 6. Detailed Data Table
    st.subheader("Detailed Ward Breakdown")
    st.dataframe(
        filtered_df,
        column_config={
            "Occupancy Rate (%)": st.column_config.ProgressColumn(
                "Occupancy Rate (%)",
                help="Percentage of beds currently occupied",
                format="%f%%",
                min_value=0,
                max_value=100,
            ),
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.warning("No wards match the selected occupancy filters. Try adjusting the slider!")
