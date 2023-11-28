import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai
import os

# Import necessary functions from your main script
from main import analyze_finances_with_openai

from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Function to format insights into bullet points
def format_insights_to_bullets(insights_text):
    lines = insights_text.split("\n")
    lines = [line.strip() for line in lines if line.strip()]
    return lines


# Streamlit page configuration
st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")


# Streamlit app main function
def main():
    st.title("Personal Finance Dashboard")

    # File uploader
    uploaded_file = st.sidebar.file_uploader(
        "Upload your transaction file (CSV or PDF)", type=["csv", "pdf"]
    )
    if uploaded_file is not None:
        try:
            if uploaded_file.type == "application/pdf":
                st.error("PDF file processing is not yet implemented.")
            else:
                transactions, openai_insights = analyze_finances_with_openai(
                    uploaded_file
                )

                # Display transaction data
                st.write("## Transaction Data")
                st.dataframe(transactions)

                # Display insights from OpenAI
                st.write("## Insights from OpenAI")
                formatted_insights = format_insights_to_bullets(openai_insights)
                for insight in formatted_insights:
                    st.markdown(f"- {insight}")

                # Visualization: Spending by Category
                st.write("## Spending by Category")
                category_data = transactions.groupby("Category")["Amount"].sum()
                fig, ax = plt.subplots()
                category_data.plot(kind="bar", ax=ax)
                st.pyplot(fig)

        except Exception as e:
            st.error(f"An error occurred: {e}")


# Run the app
if __name__ == "__main__":
    main()
