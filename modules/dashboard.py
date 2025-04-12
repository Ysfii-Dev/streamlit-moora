import streamlit as st
import pandas as pd
import altair as alt


def show():
    st.title("📊 Dashboard SPK MOORA")
    st.write("Sistem Pendukung Keputusan untuk Pemilihan Bibit Padi Terbaik")

    # --- Load data dari file CSV ---
    try:
        df_ranking = pd.read_csv("data/hasil_rangking.csv")
        df_bibit = pd.read_csv("data/data_bibit.csv")
        df_kriteria = pd.read_csv("data/bobot_kriteria.csv")
    except FileNotFoundError as e:
        st.warning(f"❗ File tidak ditemukan: {e.filename}")
        return

    # --- Penjelasan singkat ---
    with st.expander("📘 Apa itu MOORA?"):
        st.markdown("""
        **MOORA (Multi-Objective Optimization on the basis of Ratio Analysis)** adalah metode pengambilan keputusan multikriteria.
        Setiap alternatif dievaluasi terhadap beberapa kriteria yang dinormalisasi, lalu dihitung skor total (`Yi`) dan dirangking.
        """)

    # --- Kartu Statistik Ringkas (Custom Markdown) ---
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
        <div style='text-align:center; padding:15px; background-color:#f8f9fa; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.1);'>
            <div style='font-size:22px; font-weight:bold;'>📦 Jumlah Bibit</div>
            <div style='font-size:36px; color:#198754; font-weight:bold;'>{df_bibit.shape[0]}</div>
        </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
        <div style='text-align:center; padding:15px; background-color:#f8f9fa; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.1);'>
            <div style='font-size:22px; font-weight:bold;'>📋 Jumlah Kriteria</div>
            <div style='font-size:36px; color:#0d6efd; font-weight:bold;'>{df_kriteria.shape[0]}</div>
        </div>
    """, unsafe_allow_html=True)

    best = df_ranking.sort_values("Ranking").iloc[0]
    col3.markdown(f"""
        <div style='text-align:center; padding:15px; background-color:#f8f9fa; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.1);'>
            <div style='font-size:22px; font-weight:bold;'>🏅 Bibit Terbaik</div>
            <div style='font-size:28px; color:#d63384; font-weight:bold;'>{best["Nama Bibit"]}</div>
        </div>
    """, unsafe_allow_html=True)

    # --- Visualisasi Top 5 ---
    st.subheader("📈 5 Bibit Terbaik Berdasarkan Skor Yi")
    top5 = df_ranking.sort_values("Yi", ascending=False).head(5)
    chart = alt.Chart(top5).mark_bar(size=40).encode(
        x=alt.X("Nama Bibit:N", sort='-y'),
        y=alt.Y("Yi:Q"),
        color="Nama Bibit:N",
        tooltip=["Nama Bibit", "Yi", "Ranking"]
    ).properties(height=400)
    st.altair_chart(chart, use_container_width=True)

    # --- Tabel Hasil Lengkap ---
    st.subheader("📋 Tabel Hasil Ranking Lengkap")
    st.dataframe(df_ranking.sort_values("Ranking").reset_index(
        drop=True), use_container_width=True, hide_index=True)
