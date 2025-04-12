# main.py
import streamlit as st
import time
from utils.auth import login_user, logout_user, check_login
from components.sidebar import render_sidebar
from modules import dashboard, data_bibit, kriteria, moora, rangking

st.set_page_config(page_title="SPK MOORA Bibit Padi", layout="wide")

# ================
# INIT SESSION VAR
# ================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
if "page" not in st.session_state:
    st.session_state.page = ""  # halaman kosong sebelum login

# ================
# FORM LOGIN
# ================
if not st.session_state.logged_in:
    st.title("🔐 Login Sistem SPK MOORA")
    st.subheader("Silakan login terlebih dahulu.")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            success, role = login_user(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.session_state.page = "Dashboard"
                st.success("Login berhasil!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Username atau password salah!")

# ================
# HALAMAN UTAMA
# ================
else:
    menu_items = ["Dashboard", "Kriteria", "Data Bibit",
                  "Perhitungan MOORA", "Hasil Rangking"]
    render_sidebar(menu_items)

    if st.session_state.page == "Dashboard":
        dashboard.show()
    elif st.session_state.page == "Kriteria":
        kriteria.show()
    elif st.session_state.page == "Data Bibit":
        data_bibit.show()
    elif st.session_state.page == "Perhitungan MOORA":
        moora.show()
    elif st.session_state.page == "Hasil Rangking":
        rangking.show()
