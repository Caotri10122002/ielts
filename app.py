import streamlit as st
import json
import os
import pandas as pd
import matplotlib.pyplot as plt

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
    st.title("IELTS Score Monitor")

    st.sidebar.header("Input User Data")

    # User Inputs
    name = st.sidebar.text_input("Enter your name", "")
    skill = st.sidebar.selectbox("Select Skill", ["Listening", "Reading"])
    correct_answers = st.sidebar.number_input("Number of Correct Answers", min_value=0, max_value=40, step=1)

    if st.sidebar.button("Submit"):
        if not name:
            st.sidebar.error("Please enter your name.")
        else:
            band_score = get_band_score(skill, correct_answers)
            if band_score is not None:
                # Load existing data
                data = load_data()
                # Append new entry
                data.append({
                    "name": name,
                    "skill": skill,
                    "correct_answers": correct_answers,
                    "band_score": band_score
                })
                # Save data
                save_data(data)
                st.success(f"Data saved successfully for {name} - {skill} - Band {band_score}")
            else:
                st.sidebar.error("Invalid number of correct answers.")

    st.header("IELTS Scores")

    # Load and display data
    data = load_data()
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)

        st.sidebar.header("Visualization Options")
        visualize_skill = st.sidebar.selectbox("Select Skill to Visualize", ["Listening", "Reading"])

        # Filter data based on user's choice
        filtered_df = df[df["skill"] == visualize_skill]
        if not filtered_df.empty:
            st.header(f"{visualize_skill} Band Scores Visualization")
            plt.figure(figsize=(10, 6))
            plt.bar(filtered_df["name"], filtered_df["band_score"], color='skyblue')
            plt.xlabel("User Name")
            plt.ylabel("Band Score")
            plt.title(f"{visualize_skill} Band Scores")
            plt.ylim(0, 9.5)
            plt.xticks(rotation=45)

            # Annotate bars with band scores
            for index, value in enumerate(filtered_df["band_score"]):
                plt.text(index, value + 0.1, str(value), ha='center')

            st.pyplot(plt)
        else:
            st.info(f"No {visualize_skill} data to display.")
    else:
        st.info("No data available. Please submit user data.")

if __name__ == "__main__":
    main()
