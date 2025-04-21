import streamlit as st
import pandas as pd

# Load cleaned credentials dataset
credentials_file = "cleaned_credentials.csv"

# Function to check if user input exists in leaked credentials
def check_leaked_credentials(user_input):
    try:
        df = pd.read_csv(credentials_file, dtype=str)  # Ensure all data is treated as string
        
        if "email" not in df.columns or "phone_number" not in df.columns or "password" not in df.columns:
            return "Dataset Error"

        # Normalize data: Remove spaces and lowercase for better matching
        df = df.apply(lambda x: x.str.strip().str.lower() if x.dtype == "object" else x)
        user_input = user_input.strip().lower()

        if user_input in df["email"].values:
            return "Email Found"
        elif user_input in df["phone_number"].values:
            return "Phone Found"
        elif user_input in df["password"].values:
            return "Password Found"
        return None  # No leak found
    except FileNotFoundError:
        return "Dataset Missing"

# Streamlit UI
st.title("🕵️ Dark Web Monitoring Tool")
st.write("Check if your **email, phone number, or password** has been leaked.")

# User Input
user_input = st.text_input("🔍 Enter email, phone number, or password:")

if st.button("Check Dark Web"):
    if user_input:
        # Check in credentials dataset
        leaked_found = check_leaked_credentials(user_input)

        # Handle dataset errors
        if leaked_found == "Dataset Missing":
            st.error("⚠️ Credentials dataset not found! Please check the file.")
        elif leaked_found == "Dataset Error":
            st.error("⚠️ Dataset format error! Check column names (email, phone_number, password).")
        elif leaked_found:
            st.error(f"🚨 Alert! Your {leaked_found} was found in dark web leaks!")
        else:
            st.success("✅ No leaks found. Your data is safe.")
    else:
        st.warning("⚠️ Please enter something to check.")
