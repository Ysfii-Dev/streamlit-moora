import streamlit as st
import time
import pandas as pd
import os

# ==========================
# KONFIGURASI FILE DATA BIBIT
# ==========================
DATA_FILE = "./data/data_bibit.csv"

columns = [
    "Kode", "Nama Bibit", "C1 - Produktivitas panen", "C2 - Ketahanan hama/penyakit",
    "C3 - Waktu panen", "C4 - Kebutuhan air", "C5 - Kualitas gabah",
    "C6 - Adaptasi musim tanam", "C7 - Curah hujan", "C8 - pH tanah",
    "C9 - Kemudahan perawatan", "C10 - Ketersediaan di pasaran"
]

# Buat file kosong jika belum ada
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=columns).to_csv(DATA_FILE, index=False)


def generate_kode(index):
    return f"A{index+1}"


def reset_kode(df):
    df = df.copy()
    df["Kode"] = [generate_kode(i) for i in range(len(df))]
    return df


def show():
    st.title("🌾 Data Bibit Padi")

    # Baca file
    df = pd.read_csv(DATA_FILE)
    df = reset_kode(df)

    role = st.session_state.get("role", "")

    # ===============================
    # Hanya ADMIN yang boleh ubah data
    # ===============================
    if role == "admin":
        st.subheader("➕ Tambah / Edit Data Bibit")
        selected_bibit = st.selectbox(
            "Pilih bibit untuk diedit (atau biarkan kosong untuk tambah baru)",
            [""] + df["Nama Bibit"].tolist()
        )

        if selected_bibit:
            bibit_row = df[df["Nama Bibit"] == selected_bibit].iloc[0]
            is_editing = True
        else:
            bibit_row = pd.Series([None] * len(columns), index=columns)
            is_editing = False

        nama_bibit = st.text_input(
            "Nama Bibit", value=bibit_row["Nama Bibit"], disabled=is_editing)
        c1 = st.number_input("C1 - Produktivitas panen",
                             value=bibit_row["C1 - Produktivitas panen"] or 0.0)
        c2 = st.number_input("C2 - Ketahanan hama/penyakit", 1, 10, int(
            bibit_row["C2 - Ketahanan hama/penyakit"]) if bibit_row["C2 - Ketahanan hama/penyakit"] else 5)
        c3 = st.number_input("C3 - Waktu panen",
                             value=bibit_row["C3 - Waktu panen"] or 0)
        c4 = st.number_input("C4 - Kebutuhan air",
                             value=bibit_row["C4 - Kebutuhan air"] or 0)
        c5 = st.number_input("C5 - Kualitas gabah",
                             value=bibit_row["C5 - Kualitas gabah"] or 0.0)
        c6 = st.number_input("C6 - Adaptasi musim tanam", 1, 10, int(
            bibit_row["C6 - Adaptasi musim tanam"]) if bibit_row["C6 - Adaptasi musim tanam"] else 5)
        c7 = st.number_input("C7 - Curah hujan",
                             value=bibit_row["C7 - Curah hujan"] or 0.0)
        c8 = st.number_input("C8 - pH tanah", 1.0, 14.0, float(
            bibit_row["C8 - pH tanah"]) if bibit_row["C8 - pH tanah"] else 7.0)
        c9 = st.number_input("C9 - Kemudahan perawatan", 1, 10, int(
            bibit_row["C9 - Kemudahan perawatan"]) if bibit_row["C9 - Kemudahan perawatan"] else 5)
        c10 = st.number_input("C10 - Ketersediaan di pasaran", 1, 10, int(
            bibit_row["C10 - Ketersediaan di pasaran"]) if bibit_row["C10 - Ketersediaan di pasaran"] else 5)

        if st.button("💾 Simpan Data"):
            if not nama_bibit:
                st.warning("⚠️ Nama bibit tidak boleh kosong.")
            else:
                new_data = {
                    "Nama Bibit": nama_bibit,
                    "C1 - Produktivitas panen": c1,
                    "C2 - Ketahanan hama/penyakit": c2,
                    "C3 - Waktu panen": c3,
                    "C4 - Kebutuhan air": c4,
                    "C5 - Kualitas gabah": c5,
                    "C6 - Adaptasi musim tanam": c6,
                    "C7 - Curah hujan": c7,
                    "C8 - pH tanah": c8,
                    "C9 - Kemudahan perawatan": c9,
                    "C10 - Ketersediaan di pasaran": c10,
                }

                if is_editing:
                    df.loc[df["Nama Bibit"] == selected_bibit,
                           new_data.keys()] = new_data.values()
                    st.success("✅ Data berhasil diperbarui.")
                else:
                    if nama_bibit in df["Nama Bibit"].values:
                        st.warning(
                            "⚠️ Nama bibit sudah ada. Gunakan fitur edit.")
                    else:
                        new_data["Kode"] = generate_kode(len(df))
                        df = pd.concat(
                            [df, pd.DataFrame([new_data])], ignore_index=True)
                        st.success("✅ Data baru ditambahkan.")

                df = reset_kode(df)
                df.to_csv(DATA_FILE, index=False)
                time.sleep(0.5)
                st.rerun()

        st.subheader("🗑️ Hapus Data Bibit")
        hapus_bibit = st.selectbox(
            "Pilih bibit yang ingin dihapus", df["Nama Bibit"].tolist())
        if st.button("🗑️ Hapus"):
            df = df[df["Nama Bibit"] != hapus_bibit]
            df = reset_kode(df)
            df.to_csv(DATA_FILE, index=False)
            st.success("🧹 Data berhasil dihapus.")
            time.sleep(0.5)
            st.rerun()

    # ===============================
    # Semua user bisa lihat tabel
    # ===============================
    st.subheader("📋 Data Bibit Saat Ini")
    st.dataframe(df, use_container_width=True, hide_index=True)

    if role == "user":
        st.info("👷 Anda login sebagai *petani*. Fitur edit & hapus tidak tersedia.")


# def show():
#     st.title("📥 Kelola Data Bibit Padi")

#     df = pd.read_csv(DATA_FILE)

#     # Reset kode jika data berubah jumlahnya
#     df = reset_kode(df)

#     st.subheader("➕ Tambah / Edit Data Bibit")
#     selected_bibit = st.selectbox(
#         "Pilih bibit untuk diedit (atau biarkan kosong untuk tambah baru)",
#         [""] + df["Nama Bibit"].tolist()
#     )

#     if selected_bibit:
#         bibit_row = df[df["Nama Bibit"] == selected_bibit].iloc[0]
#         is_editing = True
#     else:
#         bibit_row = pd.Series([None] * len(columns), index=columns)
#         is_editing = False

#     nama_bibit = st.text_input(
#         "Nama Bibit", value=bibit_row["Nama Bibit"], disabled=is_editing)
#     c1 = st.number_input("C1 - Produktivitas panen (ton/ha)",
#                          value=bibit_row["C1 - Produktivitas panen"] or 0.0)
#     c2 = st.number_input("C2 - Ketahanan hama/penyakit (1–10)", min_value=1, max_value=10, step=1,
#                          value=int(bibit_row["C2 - Ketahanan hama/penyakit"]) if bibit_row["C2 - Ketahanan hama/penyakit"] else 5)
#     c3 = st.number_input("C3 - Waktu panen (hari)",
#                          value=bibit_row["C3 - Waktu panen"] or 0)
#     c4 = st.number_input("C4 - Kebutuhan air (liter/ha)",
#                          value=bibit_row["C4 - Kebutuhan air"] or 0)
#     c5 = st.number_input("C5 - Kualitas gabah (%)",
#                          value=bibit_row["C5 - Kualitas gabah"] or 0.0)
#     c6 = st.number_input("C6 - Adaptasi musim tanam (1–10)", min_value=1, max_value=10, step=1,
#                          value=int(bibit_row["C6 - Adaptasi musim tanam"]) if bibit_row["C6 - Adaptasi musim tanam"] else 5)
#     c7 = st.number_input("C7 - Curah hujan (mm/bulan)",
#                          value=bibit_row["C7 - Curah hujan"] or 0.0)
#     c8 = st.number_input("C8 - pH tanah (1.0–14.0)", min_value=1.0, max_value=14.0,
#                          value=float(bibit_row["C8 - pH tanah"]) if bibit_row["C8 - pH tanah"] else 7.0)
#     c9 = st.number_input("C9 - Kemudahan perawatan (1–10)", min_value=1, max_value=10, step=1,
#                          value=int(bibit_row["C9 - Kemudahan perawatan"]) if bibit_row["C9 - Kemudahan perawatan"] else 5)
#     c10 = st.number_input("C10 - Ketersediaan di pasaran (1–10)", min_value=1, max_value=10, step=1,
#                           value=int(bibit_row["C10 - Ketersediaan di pasaran"]) if bibit_row["C10 - Ketersediaan di pasaran"] else 5)

#     if st.button("💾 Simpan Data"):
#         if not nama_bibit:
#             st.warning("⚠️ Nama bibit tidak boleh kosong.")
#         else:
#             new_data = {
#                 "Nama Bibit": nama_bibit,
#                 "C1 - Produktivitas panen": c1,
#                 "C2 - Ketahanan hama/penyakit": c2,
#                 "C3 - Waktu panen": c3,
#                 "C4 - Kebutuhan air": c4,
#                 "C5 - Kualitas gabah": c5,
#                 "C6 - Adaptasi musim tanam": c6,
#                 "C7 - Curah hujan": c7,
#                 "C8 - pH tanah": c8,
#                 "C9 - Kemudahan perawatan": c9,
#                 "C10 - Ketersediaan di pasaran": c10,
#             }

#             if is_editing:
#                 df.loc[df["Nama Bibit"] == selected_bibit,
#                        new_data.keys()] = new_data.values()
#                 st.success("✅ Data berhasil diperbarui.")
#             else:
#                 if nama_bibit in df["Nama Bibit"].values:
#                     st.warning("⚠️ Nama bibit sudah ada. Gunakan fitur edit.")
#                 else:
#                     new_data["Kode"] = generate_kode(len(df))
#                     df = pd.concat(
#                         [df, pd.DataFrame([new_data])], ignore_index=True)
#                     st.success("✅ Data baru ditambahkan.")

#             df = reset_kode(df)
#             df.to_csv(DATA_FILE, index=False)
#             time.sleep(0.5)
#             st.rerun()

#     st.subheader("📋 Data Bibit Saat Ini")
#     st.dataframe(df, use_container_width=True)

#     st.subheader("🗑️ Hapus Data Bibit")
#     hapus_bibit = st.selectbox(
#         "Pilih bibit yang ingin dihapus", df["Nama Bibit"].tolist())

#     if st.button("Hapus"):
#         df = df[df["Nama Bibit"] != hapus_bibit]
#         df = reset_kode(df)
#         df.to_csv(DATA_FILE, index=False)
#         st.success("🗑️ Data berhasil dihapus.")
#         time.sleep(0.5)
#         st.rerun()
