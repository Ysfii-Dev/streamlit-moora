def render_sidebar(menu_items: list, logo_path: str = "./assets/Logo.png", app_title: str = "SPK MOORA"):
    import streamlit as st
    import time
    from utils.auth import logout_user

    # Simpan menu aktif sebelumnya untuk mendeteksi perubahan
    if "last_page" not in st.session_state:
        st.session_state.last_page = st.session_state.page

    st.sidebar.image(logo_path, width=120)
    st.sidebar.markdown(f"### {app_title}")
    st.sidebar.markdown(
        f"Hai, **{st.session_state.username}**! ")
    st.sidebar.markdown(
        "Selamat datang di aplikasi Sistem Pendukung Keputusan untuk pemilihan bibit padi menggunakan metode MOORA.")
    st.sidebar.markdown("---")

    active_index = menu_items.index(st.session_state.page)

    # === Custom CSS untuk highlight berdasarkan index
    st.sidebar.markdown(f"""
        <style>
        .stRadio > label {{
            display: none;
        }}
        .custom-label {{
            font-size: 20px;
            font-weight: bold;
            margin-top: 0px;
            margin-bottom: 10px;
        }}
        .stRadio > div > label > div:first-child {{
            display: none;
        }}
        .stRadio > div > label {{
            display: block;
            width: 100%;
            padding: 0.6rem 1rem;
            cursor: pointer;
            border-radius: 0.5rem;
            transition: all 0.3s ease;
            text-align: left;
            box-sizing: border-box;
            color: #333;
        }}
        .stRadio > div > label:hover {{
            background-color: #ffcccc;
        }}
        .stRadio > div > label:nth-child({active_index + 1}) {{
            background-color: #ff4d4d;
            color: white !important;
            font-weight: bold;
        }}
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(
        '<div class="custom-label">🧭 Menu Navigasi:</div>', unsafe_allow_html=True)

    selected_menu = st.sidebar.radio("", menu_items, index=active_index)
    st.session_state.page = selected_menu

    # Jika menu berubah, rerun untuk mempercepat respon perubahan style
    if st.session_state.last_page != selected_menu:
        st.session_state.last_page = selected_menu
        st.rerun()

    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        logout_user()
        st.success("Berhasil logout.")
        time.sleep(0.5)
        st.rerun()
