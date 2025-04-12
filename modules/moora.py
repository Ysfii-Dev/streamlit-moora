import streamlit as st
import pandas as pd
import numpy as np


def show():
    st.title("🔢 Perhitungan MOORA")
    st.info("Halaman ini menampilkan proses normalisasi, perhitungan Yi, dan hasil perangkingan alternatif bibit padi.")

    # Load data
    data = pd.read_csv("./data/data_bibit.csv")
    bobot_df = pd.read_csv("./data/bobot_kriteria.csv")
    kriteria_df = pd.read_csv("./data/data_kriteria.csv")

    # Siapkan data alternatif & kriteria
    alternatif = data['Nama Bibit']
    kriteria_cols = [col for col in data.columns if col.startswith("C")]
    matriks_keputusan = data[kriteria_cols].copy()

    # Rename kolom C1-C10 saja
    matriks_keputusan.columns = [
        f"C{i+1}" for i in range(len(matriks_keputusan.columns))]
    matriks_keputusan.insert(
        0, "Alt", [f"A{i+1}" for i in range(len(matriks_keputusan))])

    # === KONVERSI SKALA MOORA untuk C7 dan C8 ===
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

    # Terapkan konversi ke data asli
    matriks_keputusan['C7'] = matriks_keputusan['C7'].apply(
        konversi_curah_hujan)
    matriks_keputusan['C8'] = matriks_keputusan['C8'].apply(konversi_ph)

    # Tampilkan Data Alternatif terhadap Kriteria
    st.subheader("📊 Data Alternatif terhadap Kriteria")
    st.info("Data ini menunjukkan nilai dari setiap alternatif (bibit) terhadap kriteria yang telah ditentukan.")
    st.markdown("Sudah dilakukan konversi skala MOORA untuk C7 dan C8")
    st.dataframe(matriks_keputusan, use_container_width=True, hide_index=True)

    # === Tabel Bobot Tiap Kriteria ===
    st.markdown("### ⚖️ Bobot Tiap Kriteria")

    # Gabungkan data dari bobot_kriteria.csv dan data_kriteria.csv
    bobot_df = pd.read_csv("data/bobot_kriteria.csv")
    kriteria_df = pd.read_csv("data/data_kriteria.csv")

    # Gabungkan berdasarkan kolom 'Kode'
    bobot_kriteria = pd.merge(
        bobot_df, kriteria_df[['Kode', 'Jenis Atribut']], on="Kode")

    # Ganti nama kolom agar sesuai tampilan
    bobot_kriteria = bobot_kriteria[[
        'Kode', 'Kriteria', 'Bobot', 'Jenis Atribut', 'Alasan Pemberian Bobot']]
    bobot_kriteria.columns = ['Kode', 'Kriteria',
                              'Bobot', 'Jenis Atribut', 'Alasan Pemberian Bobot']

    # Tampilkan tabel
    st.dataframe(bobot_kriteria, use_container_width=True, hide_index=True)

    # 1. Normalisasi Matriks Keputusan
    st.subheader("📐📝 1. Normalisasi Matriks Keputusan")
    st.markdown("**Rumus:**")
    st.latex(r"r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{i=1}^{n} x_{ij}^2}}")

    st.markdown("**Dimana:**")
    st.markdown(r"- $x_{ij}$ = nilai kriteria ke-$j$ pada alternatif ke-$i$")
    st.markdown(r"- $r_{ij}$ = nilai setelah dinormalisasi")

    # Copy hanya kolom kriteria
    norm_matriks = matriks_keputusan.drop(columns=["Alt"]).copy()

    # Terapkan rumus normalisasi: r_ij = x_ij / sqrt(sum_i(x_ij^2))
    for col in norm_matriks.columns:
        pembagi = np.sqrt((norm_matriks[col] ** 2).sum())
        norm_matriks[col] = norm_matriks[col] / pembagi

    # Tambahkan kembali kolom alternatif ke posisi awal
    norm_matriks.insert(0, "Alt", matriks_keputusan["Alt"])
    # Hanya terapkan format angka ke kolom numerik saja
    format_dict = {col: "{:.4f}" for col in norm_matriks.select_dtypes(
        include='number').columns}

    # Tampilkan hasil normalisasi dengan format hanya untuk angka
    st.subheader("📊 Tabel Hasil Normalisasi Matriks Keputusan (rᵢⱼ)")
    st.dataframe(norm_matriks.style.format(
        format_dict), use_container_width=True, hide_index=True)

    # Rumus Yi
    st.subheader("📐📝 2. Perhitungan Nilai Yi (Optimasi MOORA)")
    st.markdown("Setelah matriks keputusan dinormalisasi, langkah selanjutnya adalah menghitung nilai optimasi (Yi) untuk setiap alternatif.")
    st.markdown("**Rumus:**")
    st.latex(r"""
    Y_i = \sum (w_j \cdot r_{ij})_{\text{benefit}} - \sum (w_j \cdot r_{ij})_{\text{cost}}
    """)
    st.markdown("""
    **Kriteria Benefit:** C1, C2, C5, C6, C7, C8, C9, C10  
    **Kriteria Cost:** C3, C4
    """)

    st.markdown(r"- $w_j$ = bobot kriteria ke-$j$")
    st.markdown("- Pisahkan penjumlahan kriteria benefit dan cost")

    # Buat mapping bobot dan jenis atribut
    bobot_map = dict(zip(bobot_kriteria["Kode"], bobot_kriteria["Bobot"]))
    tipe_map = dict(
        zip(bobot_kriteria["Kode"], bobot_kriteria["Jenis Atribut"]))

    benefit_cols = [kode for kode,
                    tipe in tipe_map.items() if "Benefit" in tipe]
    cost_cols = [kode for kode, tipe in tipe_map.items() if "Cost" in tipe]

    def hitung_Yi(row):
        benefit = sum(row[k] * bobot_map[k] for k in benefit_cols)
        cost = sum(row[k] * bobot_map[k] for k in cost_cols)
        return benefit - cost, benefit, cost

    result = norm_matriks.copy()
    result[["Yi", "Benefit", "Cost"]] = result.apply(
        hitung_Yi, axis=1, result_type='expand')
    result["Nama Bibit"] = alternatif

    st.subheader("📊 Tabel Nilai Yi Setiap Alternatif")

    # Tambahkan kolom bantu Alt_num untuk mengurutkan secara numerik
    result["Alt_num"] = result["Alt"].str.extract("(\d+)").astype(int)

    # Sort berdasarkan angka di Alt_num, lalu tampilkan dataframe tanpa Alt_num
    st.dataframe(
        result[["Alt", "Nama Bibit", "Benefit", "Cost", "Yi", "Alt_num"]]
        .sort_values(by="Alt_num")
        .drop(columns="Alt_num")
        .reset_index(drop=True)
        .style.format({'Benefit': '{:.4f}', 'Cost': '{:.4f}', 'Yi': '{:.4f}'}),
        use_container_width=True,
        hide_index=True
    )

    # === Ranking ===
    st.subheader("🏆 Hasil Perangkingan Alternatif")
    result["Ranking"] = result["Yi"].rank(ascending=False).astype(int)
    st.dataframe(
        result[["Alt", "Nama Bibit", "Yi", "Ranking"]]
        .sort_values("Ranking"),
        use_container_width=True,
        hide_index=True

    )

    # # Ambil bobot dan tipe
    # kode_bobot = bobot_kriteria['Kode']
    # bobot_dict = dict(zip(kode_bobot, bobot_kriteria['Bobot']))
    # tipe_dict = dict(zip(kode_bobot, bobot_kriteria['Jenis Atribut']))

    # benefit_cols = [
    #     f"C{i+1}" for i in range(10) if tipe_dict.get(f"C{i+1}", "Benefit") == "Benefit"]
    # cost_cols = [
    #     f"C{i+1}" for i in range(10) if tipe_dict.get(f"C{i+1}", "Benefit") == "Cost"]

    # def hitung_Yi(row):
    #     benefit = sum(row[k] * bobot_dict[k] for k in benefit_cols)
    #     cost = sum(row[k] * bobot_dict[k] for k in cost_cols)
    #     return benefit - cost, benefit, cost

    # result = norm_matriks.copy()
    # result[['Yi', 'Benefit Total', 'Cost Total']] = result.apply(
    #     hitung_Yi, axis=1, result_type='expand')
    # result['Nama Bibit'] = alternatif

    # st.subheader("📊 Tabel Nilai Yi Setiap Alternatif")
    # st.dataframe(
    #     result[['Alt', 'Nama Bibit', 'Benefit Total', 'Cost Total', 'Yi']]
    #     .sort_values(by='Yi', ascending=False)
    #     .reset_index(drop=True)
    #     .style.format({
    #         'Benefit Total': '{:.4f}',
    #         'Cost Total': '{:.4f}',
    #         'Yi': '{:.4f}'
    #     }),
    #     use_container_width=True
    # )

    # st.subheader("🏆 Hasil Perangkingan Alternatif")
    # result['Ranking'] = result['Yi'].rank(ascending=False).astype(int)
    # ranking = result[['Alt', 'Nama Bibit', 'Yi',
    #                   'Ranking']].sort_values(by='Ranking')
    # st.dataframe(ranking, use_container_width=True)
