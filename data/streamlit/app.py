import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------
# App Title
# ----------------------------
st.set_page_config(page_title="Crime Data Analysis", layout="wide")
st.title("📊 Crime Data Analysis App")

# ----------------------------
# Load Dataset
# ----------------------------
@st.cache_data
def load_data():
    return pd.read_csv(r"E:\New folder\WIE\streamlit\data\crime_dataset.csv")

df = load_data()

# ----------------------------
# Sidebar Navigation
# ----------------------------
st.sidebar.title("🔎 Navigation")
page = st.sidebar.radio("Go to", ["Dataset Overview", "EDA"])

# ----------------------------
# Page 1: Dataset Overview
# ----------------------------
if page == "Dataset Overview":
    st.header("📂 Dataset Preview")
    st.write(df.head())

    st.subheader("📊 Dataset Info")
    st.write("**Shape:**", df.shape)
    st.write("**Columns:**", df.columns.tolist())

    st.write("**Missing Values:**")
    st.write(df.isnull().sum())

    st.write("**Summary Statistics:**")
    st.write(df.describe(include="all"))

# ----------------------------
# Page 2: EDA
# ----------------------------
elif page == "EDA":
    st.header("🔍 Exploratory Data Analysis")

    col = st.selectbox("Select column to analyze", df.columns)

    if col:
        st.write(f"Value Counts for **{col}**:")
        st.write(df[col].value_counts())

        fig, ax = plt.subplots()
        sns.countplot(data=df, x=col, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)
