import pandas as pd
import streamlit as st
import os

USER_FILE = "./data/users.csv"


def login_user(username, password):
    if not os.path.exists(USER_FILE):
        st.error("⚠️ File users.csv tidak ditemukan.")
        return False, None

    try:
        users = pd.read_csv(USER_FILE)

        if "username" not in users.columns or "password" not in users.columns or "role" not in users.columns:
            st.error("❌ Struktur file users.csv tidak valid.")
            return False, None

        user = users[(users["username"] == username) &
                     (users["password"] == password)]

        if not user.empty:
            return True, user.iloc[0]["role"]
        return False, None

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file users.csv: {e}")
        return False, None


def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""


def check_login():
    return st.session_state.get("logged_in", False)
