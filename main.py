import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🚗 자동차 성능 비교 대시보드")

@st.cache_data
def load_data():
    df = pd.read_csv("Cars Datasets 2025.csv", encoding="cp1252")
    def extract_numeric(value, unit=None):
        import numpy as np
        if pd.isnull(value):
            return np.nan
        if isinstance(value, str):
            value = value.lower().replace(",", "").replace("$", "")
            if unit:
                value = value.replace(unit, "")
            if "-" in value:
                parts = value.split("-")
                try:
                    return (float(parts[0]) + float(parts[1])) / 2
                except:
                    return np.nan
            try:
                return float("".join([ch for ch in value if ch.isdigit() or ch == "."]))
            except:
                return np.nan
        return value
    df["CC"] = df["CC/Battery Capacity"].apply(lambda x: extract_numeric(x, "cc"))
    df["HorsePower"] = df["HorsePower"].apply(lambda x: extract_numeric(x, "hp"))
    df["Total Speed"] = df["Total Speed"].apply(lambda x: extract_numeric(x, "km/h"))
    df["Performance"] = df["Performance(0 - 100 )KM/H"].apply(lambda x: extract_numeric(x, "sec"))
    df["Torque"] = df["Torque"].apply(lambda x: extract_numeric(x, "nm"))
    df["Price"] = df["Cars Prices"].apply(extract_numeric)
    df["Model"] = df["Company Names"] + " " + df["Cars Names"]
    return df

df = load_data()

tab1, tab2, tab3, tab4 = st.tabs(["🏁 마력 Top 30", "⚡ 제로백 Top 30", "💲 성능 vs 가격", "📊 배기량 vs 마력"])

with tab1:
    st.subheader("마력 기준 상위 30개 차량")
    top_hp = df.dropna(subset=["HorsePower"]).sort_values(by="HorsePower", ascending=False).head(30)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(y="Model", x="HorsePower", data=top_hp, palette="Blues_r", ax=ax)
    ax.set_xlabel("마력 (HP)")
    ax.set_ylabel("")
    st.pyplot(fig)

with tab2:
    st.subheader("제로백 기준 상위 30개 차량 (낮을수록 빠름)")
    top_acc = df.dropna(subset=["Performance"]).sort_values(by="Performance", ascending=True).head(30)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(y="Model", x="Performance", data=top_acc, palette="Oranges_r", ax=ax)
    ax.set_xlabel("제로백 (초)")
    ax.set_ylabel("")
    st.pyplot(fig)

with tab3:
    st.subheader("가격 대비 마력 & 제로백 비교")
    col1, col2 = st.columns(2)
    with col1:
        fig1, ax1 = plt.subplots(figsize=(6, 5))
        sns.scatterplot(data=df, x="Price", y="HorsePower", hue="Fuel Types", alpha=0.7, ax=ax1)
        ax1.set_xlabel("가격 ($)")
        ax1.set_ylabel("마력 (HP)")
        st.pyplot(fig1)
    with col2:
        fig2, ax2 = plt.subplots(figsize=(6, 5))
        sns.scatterplot(data=df, x="Price", y="Performance", hue="Fuel Types", alpha=0.7, ax=ax2)
        ax2.set_xlabel("가격 ($)")
        ax2.set_ylabel("제로백 (초)")
        st.pyplot(fig2)

with tab4:
    st.subheader("배기량(CC) 대비 마력 (HP)")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x="CC", y="HorsePower", hue="Fuel Types", alpha=0.7, ax=ax)
    ax.set_xlabel("배기량 (cc)")
    ax.set_ylabel("마력 (HP)")
    st.pyplot(fig)
