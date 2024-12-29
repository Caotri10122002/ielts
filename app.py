import streamlit as st
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Define the band score tables
READING_BAND_TABLE = [
    {"min": 40, "max": 39, "band": 9},
    {"min": 38, "max": 37, "band": 8.5},
    {"min": 36, "max": 35, "band": 8},
    {"min": 34, "max": 33, "band": 7.5},
    {"min": 32, "max": 30, "band": 7},
    {"min": 29, "max": 27, "band": 6.5},
    {"min": 26, "max": 23, "band": 6},
    {"min": 22, "max": 19, "band": 5.5},
    {"min": 18, "max": 15, "band": 5},
    {"min": 14, "max": 13, "band": 4.5},
    {"min": 12, "max": 10, "band": 4},
    {"min": 9,  "max": 8,  "band": 3.5},
    {"min": 7,  "max": 6,  "band": 3},
    {"min": 5,  "max": 4,  "band": 2.5},
]

LISTENING_BAND_TABLE = [
    {"min": 40, "max": 39, "band": 9},
    {"min": 38, "max": 37, "band": 8.5},
    {"min": 36, "max": 35, "band": 8},
    {"min": 34, "max": 32, "band": 7.5},
    {"min": 31, "max": 30, "band": 7},
    {"min": 29, "max": 26, "band": 6.5},
    {"min": 25, "max": 23, "band": 6},
    {"min": 22, "max": 18, "band": 5.5},
    {"min": 17, "max": 16, "band": 5},
    {"min": 15, "max": 13, "band": 4.5},
    {"min": 12, "max": 11, "band": 4},
]

# File to store data
DATA_FILE = "ielts_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_band_score(skill, correct_answers):
    table = READING_BAND_TABLE if skill == "Reading" else LISTENING_BAND_TABLE
    for entry in table:
        if entry["min"] >= correct_answers >= entry["max"]:
            return entry["band"]
    return None  # Return None if no match found

def main():
    st.set_page_config(page_title="IELTS Score Monitor", layout="wide")
    st.title("📊 IELTS Score Monitor")

    st.sidebar.header("🔍 Input User Data")

    # User Inputs
    name = st.sidebar.text_input("👤 Enter your name", "")
    skill = st.sidebar.selectbox("📚 Select Skill", ["Listening", "Reading"])
    correct_answers = st.sidebar.number_input("✅ Number of Correct Answers", min_value=0, max_value=40, step=1)

    if st.sidebar.button("📥 Submit"):
        if not name.strip():
            st.sidebar.error("❌ Please enter your name.")
        else:
            band_score = get_band_score(skill, correct_answers)
            if band_score is not None:
                # Load existing data
                data = load_data()
                # Append new entry with timestamp
                data.append({
                    "name": name.strip(),
                    "skill": skill,
                    "correct_answers": correct_answers,
                    "band_score": band_score,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                # Save data
                save_data(data)
                st.sidebar.success(f"✅ Data saved successfully for **{name}** - **{skill}** - Band **{band_score}**")
            else:
                st.sidebar.error("❌ Invalid number of correct answers.")

    st.header("📋 IELTS Scores Overview")

    # Load and display data
    data = load_data()
    if data:
        df = pd.DataFrame(data)
        # Convert timestamp to datetime for sorting
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        # Sort data by timestamp
        df = df.sort_values(by='timestamp')
        st.dataframe(df)

        st.header("📈 Visualization")

        # Sidebar options for visualization
        st.sidebar.header("🎨 Visualization Options")
        unique_names = sorted(df['name'].unique())
        selected_name = st.sidebar.selectbox("👤 Select User for Visualization", unique_names)
        selected_skill = st.sidebar.selectbox("📚 Select Skill to Visualize", ["Listening", "Reading"])

        # Filter data based on selections
        user_df = df[(df['name'] == selected_name) & (df['skill'] == selected_skill)].copy()

        if not user_df.empty:
            # Sort by timestamp
            user_df = user_df.sort_values(by='timestamp')
            user_df.reset_index(drop=True, inplace=True)
            user_df['exam_number'] = user_df.index + 1  # Assign exam numbers

            st.subheader(f"📊 {selected_skill} Band Scores for **{selected_name}**")

            # Plotting
            plt.figure(figsize=(12, 6))
            plt.plot(user_df['exam_number'], user_df['band_score'], marker='o', linestyle='-', color='green')
            plt.title(f"{selected_name}'s {selected_skill} Band Score Progression", fontsize=16)
            plt.xlabel("Exam Attempt", fontsize=14)
            plt.ylabel("Band Score", fontsize=14)
            plt.ylim(0, 10)  # Scale y-axis from 0 to 10
            plt.xticks(user_df['exam_number'])  # Set x-ticks to exam numbers
            plt.yticks(range(0, 11))  # y-axis from 0 to 10 with step 1
            plt.grid(True, which='both', linestyle='--', linewidth=0.5)

            # Annotate each point with band score
            for idx, row in user_df.iterrows():
                plt.text(row['exam_number'], row['band_score'] + 0.05, str(row['band_score']),
                         ha='center', va='bottom', fontsize=12, fontweight='bold')

            st.pyplot(plt)
            plt.close()
        else:
            st.info(f"No data available for **{selected_name}** in **{selected_skill}**.")
    else:
        st.info("📥 No data available. Please submit user data.")

if __name__ == "__main__":
    main()
