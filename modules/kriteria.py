import streamlit as st
import time
import pandas as pd
import os

# =========================
# File CSV
# =========================
KRI_FILE = "./data/data_kriteria.csv"
KONVERSI_FILE = "./data/konversi_kriteria.csv"
BOBOT_FILE = "./data/bobot_kriteria.csv"

# =========================
# Inisialisasi Data
# =========================


def init_data():
    if not os.path.exists(KRI_FILE):
        df_kriteria = pd.DataFrame([
            {"Kode": "C1", "Kriteria": "Produktivitas panen",
                "Jenis Atribut": "Benefit (+)", "Skala/Satuan": "Ton/hektar", "Cara Ukur Praktis": "Data lapangan"},
            {"Kode": "C2", "Kriteria": "Ketahanan terhadap hama/penyakit",
                "Jenis Atribut": "Benefit (+)", "Skala/Satuan": "Skala 1–10", "Cara Ukur Praktis": "Pengamatan petani"},
            {"Kode": "C3", "Kriteria": "Waktu panen",
                "Jenis Atribut": "Cost (−)", "Skala/Satuan": "Hari", "Cara Ukur Praktis": "Informasi dari label bibit"},
            {"Kode": "C4", "Kriteria": "Kebutuhan air fase pembibitan",
                "Jenis Atribut": "Cost (−)", "Skala/Satuan": "Liter/hektar", "Cara Ukur Praktis": "Estimasi pengalaman"},
            {"Kode": "C5", "Kriteria": "Kualitas gabah",
                "Jenis Atribut": "Benefit (+)", "Skala/Satuan": "% Gabah berkualitas", "Cara Ukur Praktis": "Hasil giling"},
            {"Kode": "C6", "Kriteria": "Adaptasi terhadap musim tanam",
                "Jenis Atribut": "Benefit (+)", "Skala/Satuan": "Skala 1–10", "Cara Ukur Praktis": "Kesesuaian saat musim"},
            {"Kode": "C7", "Kriteria": "Curah hujan",
                "Jenis Atribut": "Benefit (+)", "Skala/Satuan": "mm/bulan", "Cara Ukur Praktis": "Estimasi dari BMKG lokal"},
            {"Kode": "C8", "Kriteria": "pH tanah",
                "Jenis Atribut": "Benefit (+)", "Skala/Satuan": "Skala 1–14", "Cara Ukur Praktis": "Kertas lakmus"},
            {"Kode": "C9", "Kriteria": "Kemudahan perawatan",
                "Jenis Atribut": "Benefit (+)", "Skala/Satuan": "Skala 1–10", "Cara Ukur Praktis": "Wawancara petani"},
            {"Kode": "C10", "Kriteria": "Ketersediaan bibit di pasaran",
                "Jenis Atribut": "Benefit (+)", "Skala/Satuan": "Skala 1–10", "Cara Ukur Praktis": "Observasi pasar"}
        ])
        df_kriteria.to_csv(KRI_FILE, index=False)

    if not os.path.exists(KONVERSI_FILE):
        df_konversi = pd.DataFrame([
            {"Kode": "C7", "Kriteria": "Curah hujan", "Satuan/Skala Asli": "mm/bulan", "Alasan Konversi": "Nilainya tidak linier – terlalu rendah/tinggi bisa buruk",
                "Aturan Konversi ke Skala MOORA (1–10)": "- 10 jika 150–200 mm (ideal)\n- 8 jika 100–149 mm atau 201–250 mm\n- 6 jika <100 mm atau >250 mm"},
            {"Kode": "C8", "Kriteria": "pH tanah", "Satuan/Skala Asli": "Skala 1–14", "Alasan Konversi": "Ideal di kisaran 5.5–7.0 – makin jauh makin buruk",
                "Aturan Konversi ke Skala MOORA (1–10)": "- 10 jika 5.5–7.0 (ideal)\n- 8 jika 5.0–5.4 atau 7.1–7.5\n- 6 jika 4.5–4.9 atau 7.6–8.0\n- 4 jika <4.5 atau >8.0"}
        ])
        df_konversi.to_csv(KONVERSI_FILE, index=False)

    if not os.path.exists(BOBOT_FILE):
        df_bobot = pd.DataFrame([
            {"Kode": "C1", "Kriteria": "Produktivitas", "Bobot": 0.15,
                "Alasan Pemberian Bobot": "Produktivitas (hasil panen) adalah tujuan utama, jadi bobot tertinggi"},
            {"Kode": "C2", "Kriteria": "Ketahanan hama/penyakit", "Bobot": 0.10,
                "Alasan Pemberian Bobot": "Serangan hama bisa sangat merusak, jadi penting dipertimbangkan"},
            {"Kode": "C3", "Kriteria": "Waktu panen", "Bobot": 0.10,
                "Alasan Pemberian Bobot": "Petani cenderung memilih bibit dengan masa panen cepat"},
            {"Kode": "C4", "Kriteria": "Kebutuhan air fase pembibitan", "Bobot": 0.10,
                "Alasan Pemberian Bobot": "Di musim kemarau, bibit hemat air lebih disukai"},
            {"Kode": "C5", "Kriteria": "Kualitas gabah", "Bobot": 0.10,
                "Alasan Pemberian Bobot": "Kualitas gabah memengaruhi harga jual di pasaran"},
            {"Kode": "C6", "Kriteria": "Adaptasi musim tanam", "Bobot": 0.10,
                "Alasan Pemberian Bobot": "Bibit yang fleksibel bisa ditanam sepanjang musim"},
            {"Kode": "C7", "Kriteria": "Curah hujan", "Bobot": 0.10,
                "Alasan Pemberian Bobot": "Kesesuaian dengan curah hujan penting untuk pertumbuhan"},
            {"Kode": "C8", "Kriteria": "pH tanah", "Bobot": 0.05,
                "Alasan Pemberian Bobot": "Meski penting, tapi biasanya bisa diatasi lewat pemupukan"},
            {"Kode": "C9", "Kriteria": "Kemudahan perawatan", "Bobot": 0.10,
                "Alasan Pemberian Bobot": "Bibit yang tidak ribet dipelihara sangat membantu petani"},
            {"Kode": "C10", "Kriteria": "Ketersediaan bibit", "Bobot": 0.10,
                "Alasan Pemberian Bobot": "Bibit harus mudah didapat di pasaran agar bisa dibeli kapan saja"}
        ])
        df_bobot.to_csv(BOBOT_FILE, index=False)

# =========================
# Fungsi Utama Streamlit
# =========================


def show():
    st.title("📊 Data Kriteria")
    init_data()

    role = st.session_state.get("role", "")

    # ===== TABEL 1: Data Kriteria =====
    st.subheader("📌 Tabel Data Kriteria")
    df_kri = pd.read_csv(KRI_FILE)
    edited_kri = st.data_editor(
        df_kri, use_container_width=True, key="kri_edit", hide_index=True)

    if role == "admin":

        if st.button("💾 Simpan Perubahan Kriteria"):
            edited_kri.to_csv(KRI_FILE, index=False)
            st.success("Data kriteria berhasil disimpan.")
            time.sleep(0.5)  # Delay untuk memberi waktu pada pengguna
            st.rerun()
    else:
        st.info("Hanya admin yang bisa mengedit data kriteria.")
        st.warning(
            "Jika ada kesalahan data, silakan hubungi admin untuk memperbaiki.")

    st.markdown("""
    - **Benefit (+)**: Semakin besar nilainya, semakin baik (menguntungkan).
    - **Cost (−)**: Semakin kecil nilainya, semakin baik (efisien).
    
    Semua kriteria akan digunakan dalam proses normalisasi dan pembobotan dalam metode MOORA.
    """)

    st.divider()

    # ===== TABEL 2: Konversi Skor MOORA =====
    st.subheader("📋 Tabel Kriteria yang Harus Dikonversi ke Skor MOORA")
    df_konversi = pd.read_csv(KONVERSI_FILE)
    edited_konv = st.data_editor(
        df_konversi, use_container_width=True, key="konv_edit", hide_index=True)

    if role == "admin":
        if st.button("💾 Simpan Perubahan Konversi"):
            edited_konv.to_csv(KONVERSI_FILE, index=False)
            st.success("Data konversi berhasil disimpan.")
            time.sleep(0.5)
            st.rerun()
    else:
        st.info("Hanya admin yang bisa mengedit data konversi.")
        st.warning(
            "Jika ada kesalahan data, silakan hubungi admin untuk memperbaiki.")

    st.divider()

    # ===== TABEL 3: Bobot Kriteria =====
    st.subheader("📈 Bobot Tiap Kriteria")
    df_bobot = pd.read_csv(BOBOT_FILE)
    edited_bobot = st.data_editor(
        df_bobot, use_container_width=True, key="bobot_edit", hide_index=True)

    if role == "admin":

        if st.button("💾 Simpan Perubahan Bobot"):
            edited_bobot.to_csv(BOBOT_FILE, index=False)
            st.success("Data bobot berhasil disimpan.")
            time.sleep(0.5)
            st.rerun()
    else:
        st.info("Hanya admin yang bisa mengedit data bobot.")
        st.warning(
            "Jika ada kesalahan data, silakan hubungi admin untuk memperbaiki.")
