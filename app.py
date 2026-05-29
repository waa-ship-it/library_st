import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================

st.set_page_config(
    page_title="Libraverse",
    page_icon="📚",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #F5F7FB;
}

.header-box {
    background: linear-gradient(to right, #667eea, #764ba2);
    padding: 35px;
    border-radius: 25px;
    color: white;
    margin-bottom: 30px;
}

.book-card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# DATABASE
# =====================================================

conn = sqlite3.connect(
    "library.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =====================================================
# TABEL BUKU
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (

    kode TEXT PRIMARY KEY,
    judul TEXT,
    penulis TEXT,
    kategori TEXT,
    tahun INTEGER,
    status TEXT

)
""")

# =====================================================
# TABEL PEMINJAMAN
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS peminjaman (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    kode_buku TEXT,
    judul TEXT,
    tanggal_pinjam TEXT,
    batas_kembali TEXT,
    tanggal_kembali TEXT,
    status TEXT,
    denda INTEGER

)
""")

conn.commit()

# =====================================================
# DATA BUKU AWAL
# =====================================================

cursor.execute("SELECT COUNT(*) FROM books")

if cursor.fetchone()[0] == 0:

    books = [

        ("BK001", "Atomic Habits", "James Clear", "Self Improvement", 2018, "Tersedia"),
        ("BK002", "Harry Potter", "J.K Rowling", "Fantasi", 2001, "Tersedia"),
        ("BK003", "Laskar Pelangi", "Andrea Hirata", "Pendidikan", 2005, "Tersedia"),
        ("BK004", "Bumi", "Tere Liye", "Fantasi", 2014, "Tersedia"),
        ("BK005", "Sherlock Holmes", "Arthur Conan Doyle", "Misteri", 1892, "Tersedia"),
        ("BK006", "Dilan 1990", "Pidi Baiq", "Romance", 2014, "Tersedia"),
        ("BK007", "Filosofi Teras", "Henry Manampiring", "Self Improvement", 2019, "Tersedia"),
        ("BK008", "One Piece Vol 1", "Eiichiro Oda", "Komik", 1997, "Tersedia"),
        ("BK009", "Naruto Vol 1", "Masashi Kishimoto", "Komik", 1999, "Tersedia"),
        ("BK010", "Laut Bercerita", "Leila S. Chudori", "Fiksi", 2017, "Tersedia"),
        ("BK011", "Negeri 5 Menara", "Ahmad Fuadi", "Pendidikan", 2009, "Tersedia"),
        ("BK012", "The Psychology of Money", "Morgan Housel", "Bisnis", 2020, "Tersedia"),
        ("BK013", "Rich Dad Poor Dad", "Robert Kiyosaki", "Bisnis", 1997, "Tersedia"),
        ("BK014", "Ayat Ayat Cinta", "Habiburrahman", "Religi", 2004, "Tersedia"),
        ("BK015", "Cantik Itu Luka", "Eka Kurniawan", "Fiksi", 2002, "Tersedia")

    ]

    cursor.executemany(
        "INSERT INTO books VALUES (?, ?, ?, ?, ?, ?)",
        books
    )

    conn.commit()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown("""
# 📚 Libraverse

### Digital Library System ✨

Kelola buku favoritmu dengan mudah 📖
""")

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "📌 Pilih Menu",
    [

        "🏠 Home",
        "📚 Koleksi Buku",
        "🔍 Cari Buku",
        "📖 Pinjam Buku",
        "✏️ Perpanjang Peminjaman",
        "📥 Kembalikan Buku",
        "📋 Riwayat Peminjaman",
        "🗑️ Hapus Riwayat"

    ]
)

st.sidebar.markdown("---")

st.sidebar.info("""
📖 Quotes Hari Ini

"Books are a uniquely portable magic."
— Stephen King
""")

# =====================================================
# HOME
# =====================================================

if menu == "🏠 Home":

    st.markdown("""
    <div class="header-box">

    <h1>📚 Libraverse</h1>

    <p>
    Sistem Perpustakaan Digital Modern
    </p>

    </div>
    """, unsafe_allow_html=True)

    total_buku = pd.read_sql_query(
        "SELECT * FROM books",
        conn
    )

    tersedia = pd.read_sql_query(
        "SELECT * FROM books WHERE status='Tersedia'",
        conn
    )

    dipinjam = pd.read_sql_query(
        "SELECT * FROM books WHERE status='Dipinjam'",
        conn
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📚 Total Buku",
            len(total_buku)
        )

    with col2:
        st.metric(
            "🟢 Tersedia",
            len(tersedia)
        )

    with col3:
        st.metric(
            "📕 Dipinjam",
            len(dipinjam)
        )

    st.markdown("---")

    st.subheader("✨ Tentang Libraverse")

    st.write("""
    Libraverse adalah aplikasi perpustakaan digital
    sederhana untuk mencari dan meminjam buku 📖
    """)

# =====================================================
# KOLEKSI BUKU
# =====================================================

elif menu == "📚 Koleksi Buku":

    st.title("📚 Koleksi Buku")

    data = pd.read_sql_query(
        "SELECT * FROM books",
        conn
    )

    kategori_db = pd.read_sql_query(
        "SELECT DISTINCT kategori FROM books",
        conn
    )

    list_kategori = ["Semua"] + kategori_db["kategori"].tolist()

    kategori = st.selectbox(
        "📚 Filter Kategori",
        list_kategori
    )

    if kategori != "Semua":

        data = data[
            data["kategori"] == kategori
        ]

    for _, buku in data.iterrows():

        warna = "🟢" if buku["status"] == "Tersedia" else "🔴"

        st.markdown(f"""
        <div class="book-card">

        <h3>📖 {buku['judul']}</h3>

        <p>✍️ Penulis : {buku['penulis']}</p>

        <p>📚 Kategori : {buku['kategori']}</p>

        <p>📅 Tahun : {buku['tahun']}</p>

        <p>{warna} {buku['status']}</p>

        <p>🆔 {buku['kode']}</p>

        </div>
        """, unsafe_allow_html=True)

# =====================================================
# CARI BUKU
# =====================================================

elif menu == "🔍 Cari Buku":

    st.title("🔍 Cari Buku")

    keyword = st.text_input(
        "Masukkan judul buku"
    )

    if keyword:

        query = f"""
        SELECT * FROM books
        WHERE judul LIKE '%{keyword}%'
        """

        data = pd.read_sql_query(
            query,
            conn
        )

        if len(data) > 0:

            for _, buku in data.iterrows():

                st.markdown(f"""
                <div class="book-card">

                <h3>📖 {buku['judul']}</h3>

                <p>✍️ {buku['penulis']}</p>

                <p>📚 {buku['kategori']}</p>

                </div>
                """, unsafe_allow_html=True)

        else:
            st.error("❌ Buku tidak ditemukan")

# =====================================================
# PINJAM BUKU
# =====================================================

elif menu == "📖 Pinjam Buku":

    st.title("📖 Pinjam Buku")

    nama = st.text_input("Nama Peminjam")

    kode = st.text_input("Kode Buku")

    lama = st.number_input(
        "Lama Peminjaman (hari)",
        1,
        14
    )

    if st.button("Pinjam Buku"):

        cursor.execute(
            "SELECT * FROM books WHERE kode=?",
            (kode,)
        )

        buku = cursor.fetchone()

        if buku:

            if buku[5] == "Dipinjam":

                st.error("❌ Buku sedang dipinjam")

            else:

                tanggal_pinjam = datetime.now()

                batas = tanggal_pinjam + timedelta(days=lama)

                cursor.execute("""
                INSERT INTO peminjaman (

                    nama,
                    kode_buku,
                    judul,
                    tanggal_pinjam,
                    batas_kembali,
                    tanggal_kembali,
                    status,
                    denda

                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (

                    nama,
                    kode,
                    buku[1],
                    tanggal_pinjam.strftime("%Y-%m-%d"),
                    batas.strftime("%Y-%m-%d"),
                    "-",
                    "Dipinjam",
                    0

                ))

                cursor.execute("""
                UPDATE books

                SET status='Dipinjam'

                WHERE kode=?
                """, (kode,))

                conn.commit()

                st.success("✅ Buku berhasil dipinjam")

                st.info(
                    f"📅 Batas pengembalian: "
                    f"{batas.strftime('%d-%m-%Y')}"
                )

        else:
            st.error("❌ Buku tidak ditemukan")

# =====================================================
# PERPANJANG PEMINJAMAN
# =====================================================

elif menu == "✏️ Perpanjang Peminjaman":

    st.title("✏️ Perpanjang Peminjaman")

    kode = st.text_input(
        "Masukkan kode buku"
    )

    tambah_hari = st.number_input(
        "Tambah hari",
        1,
        14
    )

    if st.button("Perpanjang"):

        cursor.execute("""
        SELECT * FROM peminjaman

        WHERE kode_buku=?
        AND status='Dipinjam'
        """, (kode,))

        data = cursor.fetchone()

        if data:

            batas_lama = datetime.strptime(
                data[5],
                "%Y-%m-%d"
            )

            batas_baru = (
                batas_lama +
                timedelta(days=tambah_hari)
            )

            cursor.execute("""
            UPDATE peminjaman

            SET batas_kembali=?

            WHERE id=?
            """, (

                batas_baru.strftime("%Y-%m-%d"),
                data[0]

            ))

            conn.commit()

            st.success("✅ Peminjaman berhasil diperpanjang")

            st.info(
                f"📅 Batas baru: "
                f"{batas_baru.strftime('%d-%m-%Y')}"
            )

        else:
            st.error("❌ Data tidak ditemukan")

# =====================================================
# KEMBALIKAN BUKU
# =====================================================

elif menu == "📥 Kembalikan Buku":

    st.title("📥 Kembalikan Buku")

    kode = st.text_input(
        "Masukkan kode buku"
    )

    if st.button("Kembalikan Buku"):

        cursor.execute("""
        SELECT * FROM peminjaman

        WHERE kode_buku=?
        AND status='Dipinjam'
        """, (kode,))

        data = cursor.fetchone()

        if data:

            batas = datetime.strptime(
                data[5],
                "%Y-%m-%d"
            )

            hari_ini = datetime.now()

            telat = (
                hari_ini - batas
            ).days

            denda = 0

            if telat > 0:
                denda = telat * 5000

            cursor.execute("""
            UPDATE peminjaman

            SET

                tanggal_kembali=?,
                status='Dikembalikan',
                denda=?

            WHERE id=?
            """, (

                hari_ini.strftime("%Y-%m-%d"),
                denda,
                data[0]

            ))

            cursor.execute("""
            UPDATE books

            SET status='Tersedia'

            WHERE kode=?
            """, (kode,))

            conn.commit()

            st.success("✅ Buku berhasil dikembalikan")

            if denda > 0:

                st.error(
                    f"⚠️ Denda: Rp {denda}"
                )

            else:

                st.success("🎉 Tidak ada denda")

        else:
            st.error("❌ Data tidak ditemukan")

# =====================================================
# RIWAYAT PEMINJAMAN
# =====================================================

elif menu == "📋 Riwayat Peminjaman":

    st.title("📋 Riwayat Peminjaman")

    data = pd.read_sql_query(
        "SELECT * FROM peminjaman",
        conn
    )

    st.dataframe(
        data,
        use_container_width=True
    )

# =====================================================
# HAPUS RIWAYAT
# =====================================================

elif menu == "🗑️ Hapus Riwayat":

    st.title("🗑️ Hapus Riwayat")

    id_hapus = st.number_input(
        "Masukkan ID Riwayat",
        1,
        100000
    )

    if st.button("Hapus"):

        cursor.execute(
            "DELETE FROM peminjaman WHERE id=?",
            (id_hapus,)
        )

        conn.commit()

        st.success("✅ Riwayat berhasil dihapus")

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">

📚 Libraverse — Digital Library System

</div>
""", unsafe_allow_html=True)
