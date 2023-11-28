import pandas as pd
import openai
import tabula  # for reading PDF files
import os

from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def load_transactions(file_path):
    """
    Load transactions from a CSV file.
    """
    return pd.read_csv(file_path)


def categorize_transaction(merchant):
    """
    Categorize a transaction based on its merchant.
    """
    groceries_keywords = ["walmart", "supermarket", "grocery"]
    utilities_keywords = ["electric", "water", "utility", "gas"]
    entertainment_keywords = ["cinema", "movie", "netflix", "concert"]
    transportation_keywords = ["uber", "taxi", "lyft"]

    merchant = merchant.lower()
    if any(keyword in merchant for keyword in groceries_keywords):
        return "Groceries"
    elif any(keyword in merchant for keyword in utilities_keywords):
        return "Utilities"
    elif any(keyword in merchant for keyword in entertainment_keywords):
        return "Entertainment"
    elif any(keyword in merchant for keyword in transportation_keywords):
        return "Ride Share"
    else:
        return "Other"


def categorize_transactions(df):
    """
    Categorize transactions in a DataFrame based on the Merchant column.
    """
    df["Category"] = df["Merchant"].apply(categorize_transaction)
    return df


def prepare_data_for_analysis(df):
    """
    Prepare a text summary of the financial data for analysis.
    """
    total_spending = df["Amount"].sum()
    spending_by_category = df.groupby("Category")["Amount"].sum().to_dict()
    average_spending = df["Amount"].mean()

    # Prepare a text summary
    summary = f"Total spending: {total_spending}\n"
    summary += f"Average spending: {average_spending}\n"
    summary += "Spending by category:\n"
    for category, amount in spending_by_category.items():
        summary += f" - {category}: {amount}\n"

    return summary


def get_financial_insights(data_summary):
    """
    Get financial insights from OpenAI based on the data summary.
    """
    response = openai.Completion.create(
        model="text-davinci-003",  # or the latest available model
        prompt=f"Analyze the following financial data and provide insights on spending habits, areas where the budget is being overrun, and suggestions for saving money:\n\n{data_summary}",
        temperature=0.7,
        max_tokens=150,
    )
    return response.choices[0].text.strip()


def analyze_finances_with_openai(file_path):
    """
    Analyze finances from a file using OpenAI.
    """
    transactions_df = load_transactions(file_path)
    categorized_df = categorize_transactions(transactions_df)
    data_summary = prepare_data_for_analysis(categorized_df)
    insights = get_financial_insights(data_summary)

    return categorized_df, insights
