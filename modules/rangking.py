# modules/rangking.py

import streamlit as st
import pandas as pd
import numpy as np


def show():
    # ========================
    # HALAMAN HASIL RANGKING
    # ========================
    st.title("🏆 Hasil Rangking Bibit")
    st.info("Halaman ini menampilkan hasil akhir perangkingan metode MOORA berdasarkan nilai Yi.")

    # Load data
    data = pd.read_csv("./data/data_bibit.csv")
    bobot_df = pd.read_csv("./data/bobot_kriteria.csv")
    kriteria_df = pd.read_csv("./data/data_kriteria.csv")

    alternatif = data['Nama Bibit']
    kriteria_cols = [col for col in data.columns if col.startswith("C")]
    matriks = data[kriteria_cols].copy()
    matriks.columns = [f"C{i+1}" for i in range(len(matriks.columns))]
    matriks.insert(0, "Alt", [f"A{i+1}" for i in range(len(matriks))])

    # Konversi untuk C7 dan C8
    def konversi_curah_hujan(val):
        if 150 <= val <= 200:
            return 10
        elif (100 <= val < 150) or (200 < val <= 250):
            return 8
        else:
            return 6

    def konversi_ph(val):
        if 5.5 <= val <= 7.0:
            return 10
        elif (5.0 <= val < 5.5) or (7.0 < val <= 7.5):
            return 8
        elif (4.5 <= val < 5.0) or (7.5 < val <= 8.0):
            return 6
        else:
            return 4

    matriks['C7'] = matriks['C7'].apply(konversi_curah_hujan)
    matriks['C8'] = matriks['C8'].apply(konversi_ph)

    # Normalisasi
    norm = matriks.drop(columns=["Alt"]).copy()
    for col in norm.columns:
        norm[col] = norm[col] / np.sqrt((norm[col]**2).sum())
    norm.insert(0, "Alt", matriks["Alt"])

    # Bobot dan jenis atribut
    bobot_map = dict(zip(bobot_df["Kode"], bobot_df["Bobot"]))
    tipe_map = dict(zip(kriteria_df["Kode"], kriteria_df["Jenis Atribut"]))

    benefit_cols = [kode for kode,
                    tipe in tipe_map.items() if "Benefit" in tipe]
    cost_cols = [kode for kode, tipe in tipe_map.items() if "Cost" in tipe]

    def hitung_Yi(row):
        benefit = sum(row[k] * bobot_map[k] for k in benefit_cols)
        cost = sum(row[k] * bobot_map[k] for k in cost_cols)
        return benefit - cost

    result = norm.copy()
    result["Yi"] = result.apply(hitung_Yi, axis=1)
    result["Nama Bibit"] = alternatif
    result["Ranking"] = result["Yi"].rank(ascending=False).astype(int)

    final_rank = result[["Ranking", "Alt",
                         "Nama Bibit", "Yi"]].sort_values("Ranking")

    # Tambahkan kolom keterangan
    final_rank["Keterangan"] = final_rank["Ranking"].apply(
        lambda x: "Terbaik" if x == 1 else f"Alternatif {x-1}"
    )

    # Tampilkan tabel ranking
    st.subheader("📊 Tabel Hasil Rangking Bibit Padi")
    st.dataframe(
        final_rank[["Ranking", "Nama Bibit", "Yi", "Keterangan"]]
        .style.format({'Yi': '{:.4f}'}),
        use_container_width=True,
        hide_index=True
    )

    # visualisasi hasil
    st.subheader("📈 Visualisasi Hasil Rangking")
    import altair as alt

    chart = alt.Chart(final_rank).mark_line(point=True).encode(
        x=alt.X("Nama Bibit", sort="-y", axis=alt.Axis(labelAngle=-45)),
        y="Yi",
        tooltip=["Nama Bibit", "Yi"]
    ).properties(title="Visualisasi Nilai Yi Setiap Bibit")

    st.altair_chart(chart, use_container_width=True)
    with st.expander("ℹ️ Penjelasan Singkat Hasil"):
        st.write("""
        Dari visualisasi di atas, kita dapat melihat perbandingan nilai Yi dari setiap bibit padi.
        Bibit Sidenok (Rambutan) dengan nilai Yi tertinggi menunjukkan performa terbaik berdasarkan kriteria yang telah ditentukan.
        Nilai Yi merupakan hasil perhitungan berdasarkan metode MOORA, yang memperhitungkan bobot dan jenis kriteria bibit padi.
        Bibit dengan nilai Yi tertinggi dianggap paling sesuai atau unggul berdasarkan kriteria yang ditentukan.
        """)

    # simpan hasil rangking ke file CSV
    result.to_csv("./data/hasil_rangking.csv", index=False)
