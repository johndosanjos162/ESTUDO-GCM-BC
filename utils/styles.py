"""CSS customizado para o Streamlit."""

import streamlit as st


def carregar_css() -> None:
    st.markdown(
        """
        <style>
        .stApp { background-color: #f5f7fa; }
        .stButton > button {
            background-color: #1e3a5f;
            color: white;
            border-radius: 8px;
            border: none;
        }
        .stButton > button:hover {
            background-color: #2c5282;
            color: #fff;
        }
        div[data-testid="stMetric"] {
            background-color: #e8f0fe;
            padding: 12px;
            border-radius: 10px;
            border-left: 4px solid #1e3a5f;
        }
        .block-container { padding-top: 2rem; }
        h1, h2, h3 { color: #1e3a5f; }
        </style>
        """,
        unsafe_allow_html=True,
    )
